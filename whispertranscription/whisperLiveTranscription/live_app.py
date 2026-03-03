"""
live_app.py — Orchestrator utama Live Transcription
====================================================
Kelas LiveTranscriptionApp mengikat semua komponen:
  Config → AudioCapture → Transcriber → HallucinationFilter → display + simpan

Ini adalah kelas utama yang mengelola main loop, tampilan Rich Live,
mode bicara/hening, trailing-flush, dan penyimpanan hasil.
"""

from __future__ import annotations

import os
import datetime
import time
from typing import Optional

from rich.console import Console
from rich.live import Live
from rich.panel import Panel

from config import Config
from hallucination_filter import HallucinationFilter
from audio_processor import AudioProcessor
from transcriber import Transcriber
from audio_capture import AudioCapture


class LiveTranscriptionApp:
    """
    Orchestrator utama yang mengikat semua komponen.

    Cara pakai:
      app = LiveTranscriptionApp(Config())
      app.run()
    """

    def __init__(self, cfg: Config):
        self._cfg     = cfg
        self._console = Console()

        # Inisialisasi semua komponen
        self._filter      = HallucinationFilter(cfg)
        self._processor   = AudioProcessor(cfg)
        self._transcriber = Transcriber(cfg, self._processor, self._console)
        self._capture     = AudioCapture(cfg, self._console)

        # State transkripsi
        self._history_text  : str            = ""
        self._current_text  : str            = ""
        self._prev_text     : str            = ""
        self._is_speaking   : bool           = False
        self._silence_since : Optional[float] = None

    # ══════════════════════════════════════════════════
    # Entry point
    # ══════════════════════════════════════════════════

    def run(self) -> None:
        """
        Mulai aplikasi — entry point utama.
        Urutan startup:
          1. Banner
          2. Pilih mikrofon
          3. Load Whisper model
          4. Load LanguageTool (auto-correct)
          5. Start transcription thread
          6. Start mic stream
          7. Main loop
        """
        self._print_banner()
        self._capture.select_mic()
        self._transcriber.load_model()
        self._transcriber.load_autocorrect()
        self._transcriber.start()
        self._capture.start()

        cfg = self._cfg
        self._console.print(
            f"\n[bold cyan]✓ Mic aktif | VAD: {cfg.vad_threshold} | "
            f"Model: {cfg.model_size}[/bold cyan]"
        )
        self._console.print("[dim]Tekan Ctrl+C untuk berhenti dan menyimpan hasil.[/dim]\n")

        try:
            with Live(console=self._console, refresh_per_second=10) as live:
                self._main_loop(live)
        except KeyboardInterrupt:
            pass
        finally:
            self._shutdown()

    # ══════════════════════════════════════════════════
    # Main loop
    # ══════════════════════════════════════════════════

    def _main_loop(self, live: Live) -> None:
        """Loop utama: drain audio → VAD → bicara/hening → display."""
        cfg = self._cfg
        try:
            while True:
                time.sleep(0.05)                       # 50ms — anti busy-loop
                self._capture.drain_queue()            # audio queue → buffer

                # Belum cukup audio, tunggu dulu
                if self._capture.buffer_duration_sec() < cfg.min_process_sec:
                    continue

                # Hitung RMS (volume)
                rms = self._capture.get_rms()

                if cfg.debug_rms:
                    bar   = "█" * min(int(rms * 500), 30)
                    label = "SUARA" if rms >= cfg.vad_threshold else "hening"
                    self._console.log(f"[dim]RMS: {rms:.5f} | {label} | {bar}[/dim]")

                # Pilih mode berdasarkan VAD
                if rms < cfg.vad_threshold:
                    self._handle_silence(rms, live)
                else:
                    self._handle_speaking(rms, live)

        except KeyboardInterrupt:
            self._transcriber.stop()
            self._save_result(live)

    # ══════════════════════════════════════════════════
    # Mode hening
    # ══════════════════════════════════════════════════

    def _handle_silence(self, rms: float, live: Live) -> None:
        """
        Menangani mode hening (RMS < vad_threshold).

        Jika sebelumnya sedang bicara:
          - Mulai timer hening
          - Setelah silence_pause_sec → trailing flush (transkripsi sisa buffer)
          - Simpan ke history & reset state
        """
        cfg = self._cfg
        if self._is_speaking:
            # Mulai hitung durasi hening
            if self._silence_since is None:
                self._silence_since = time.monotonic()

            silent_duration = time.monotonic() - self._silence_since

            if silent_duration >= cfg.silence_pause_sec:
                # ── TRAILING FLUSH ──
                buf = self._capture.get_buffer()
                if len(buf) >= self._capture.mic_sr * 0.5:
                    self._transcriber.submit_and_wait(buf, self._capture.mic_sr, timeout=5.0)
                    tail = self._transcriber.pop_result()
                    if tail and not self._filter.is_hallucination(tail) and tail != self._prev_text:
                        self._current_text = tail
                        self._prev_text    = tail

                # Pindahkan ke history & reset
                if self._current_text:
                    self._history_text += self._current_text + " "
                    self._current_text  = ""
                    self._prev_text     = ""

                self._capture.clear_buffer()
                self._is_speaking   = False
                self._silence_since = None
        else:
            self._silence_since = None

        # Tampilkan panel hening
        display = self._history_text + "\n[dim]... (Hening / Menunggu suara) ...[/dim]"
        live.update(Panel(display, title=f"Whisper Live [RMS:{rms:.4f}]", border_style="yellow"))

        # Batasi buffer hening agar memori tidak penuh
        self._capture.trim_buffer(max_sec=1.0)

    # ══════════════════════════════════════════════════
    # Mode bicara
    # ══════════════════════════════════════════════════

    def _handle_speaking(self, rms: float, live: Live) -> None:
        """
        Menangani mode bicara (RMS >= vad_threshold).

        Mengirim audio ke Transcriber (non-blocking) dan menampilkan
        hasil transkripsi terbaru secara live.
        """
        cfg = self._cfg
        self._is_speaking   = True
        self._silence_since = None

        # Kirim audio ke background transcriber (non-blocking)
        buf = self._capture.get_buffer()
        self._transcriber.submit(buf, self._capture.mic_sr)

        # Baca hasil transkripsi terbaru
        chunk_text = self._transcriber.get_result()

        # Filter hallusinasi & duplikat
        if self._filter.is_hallucination(chunk_text):
            chunk_text = ""
        if chunk_text and chunk_text == self._prev_text:
            chunk_text = ""

        if chunk_text:
            self._current_text = chunk_text
            self._prev_text    = chunk_text

        # Tampilkan panel suara terdeteksi
        display = f"{self._history_text}[bold green]{self._current_text}[/bold green]"
        live.update(Panel(
            display,
            title=f"[bold green]🔴 Suara Terdeteksi [RMS:{rms:.4f}][/bold green]",
            border_style="green",
        ))

        # Flush buffer jika sudah terlalu panjang
        if self._capture.buffer_duration_sec() > cfg.buffer_max_sec:
            if self._current_text:
                self._history_text += self._current_text + " "
                self._current_text  = ""
                self._prev_text     = ""
            self._capture.clear_buffer()

    # ══════════════════════════════════════════════════
    # Simpan hasil
    # ══════════════════════════════════════════════════

    def _save_result(self, live: Live) -> None:
        """Tampilkan hasil final dan simpan ke file .txt di folder hasil/."""
        final = (self._history_text + self._current_text).strip()

        live.update(Panel(
            final or "[dim](Tidak ada teks)[/dim]",
            title="[bold cyan]✓ Transkripsi Selesai[/bold cyan]",
            border_style="cyan",
        ))

        if not final:
            self._console.print("\n[yellow]Tidak ada teks untuk disimpan.[/yellow]")
            return

        cfg = self._cfg
        os.makedirs(cfg.output_dir, exist_ok=True)
        ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(cfg.output_dir, f"transkrip_{ts}.txt")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("=== TRANSKRIPSI RAPAT (LIVE) ===\n")
            f.write(f"Dibuat  : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
            f.write(f"Model   : Whisper {cfg.model_size}\n")
            f.write(f"{'=' * 40}\n\n")
            f.write(final)

        self._console.print(
            f"\n[bold green]✓ Disimpan ke:[/bold green] [underline]{out_path}[/underline]"
        )

    # ══════════════════════════════════════════════════
    # Utilitas internal
    # ══════════════════════════════════════════════════

    def _shutdown(self) -> None:
        """Hentikan semua komponen dengan rapi."""
        self._capture.stop()
        self._transcriber.stop()
        self._console.print("[bold red]\nProgram dihentikan.[/bold red]")

    def _print_banner(self) -> None:
        """Tampilkan banner pembuka aplikasi."""
        self._console.print(Panel.fit(
            "[bold cyan]🎙 Whisper Live Transcription Rapat[/bold cyan]\n"
            "[dim]OOP · Realtime · Noise Reduction · Anti-Hallucination · Auto-Correct · Bahasa Indonesia[/dim]",
            border_style="cyan",
        ))
