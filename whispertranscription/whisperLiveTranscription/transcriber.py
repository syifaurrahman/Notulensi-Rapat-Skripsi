"""
transcriber.py — Transkripsi Whisper + Auto-Correct LanguageTool
================================================================
Kelas Transcriber mengelola:
  - Load Whisper model
  - Load LanguageTool (auto-correct Bahasa Indonesia)
  - Background thread untuk transkripsi non-blocking
  - submit() untuk kirim audio, get_result() untuk ambil hasil
"""

from __future__ import annotations

import queue
import threading
from typing import Optional, TYPE_CHECKING

import numpy as np
import whisper
from rich.console import Console

if TYPE_CHECKING:
    from config import Config
    from audio_processor import AudioProcessor


class Transcriber:
    """
    Mengelola Whisper model + LanguageTool dalam satu background thread.

    Cara pakai:
      t = Transcriber(cfg, processor, console)
      t.load_model()
      t.load_autocorrect()
      t.start()

      t.submit(audio, mic_sr)          # non-blocking, untuk mode bicara
      t.submit_and_wait(audio, mic_sr) # blocking, untuk trailing flush
      hasil = t.get_result()
      t.stop()
    """

    def __init__(self, cfg: "Config", processor: "AudioProcessor", console: Console):
        self._cfg       = cfg
        self._processor = processor
        self._console   = console

        self._model    = None
        self._lt_tool  = None
        self._use_fp16 = False

        self._queue  : queue.Queue       = queue.Queue(maxsize=1)
        self._result : dict              = {"text": ""}
        self._lock   : threading.Lock    = threading.Lock()
        self._done   : threading.Event   = threading.Event()
        self._thread : Optional[threading.Thread] = None

    # ── Inisialisasi ───────────────────────────────────

    def load_model(self) -> None:
        """Load Whisper model ke GPU atau CPU dengan fallback otomatis."""
        cfg    = self._cfg
        device = "cuda" if cfg.use_gpu else "cpu"
        self._console.print(
            f"\n[bold green]Memuat model Whisper '{cfg.model_size}' ke {device.upper()}...[/bold green]"
        )
        try:
            self._model = whisper.load_model(cfg.model_size).to(device)
        except Exception as e:
            self._console.print(f"[yellow]⚠ Fallback ke CPU: {e}[/yellow]")
            self._model = whisper.load_model(cfg.model_size)
            device      = "cpu"
        self._use_fp16 = (device == "cuda")

    def load_autocorrect(self) -> None:
        """Inisialisasi LanguageTool untuk auto-correct Bahasa Indonesia."""
        if not self._cfg.use_autocorrect:
            return
        self._console.print(
            "[bold green]Memuat LanguageTool (auto-correct Bahasa Indonesia)...[/bold green]"
        )
        self._console.print("[dim]Pertama kali: download ~200MB, berikutnya dari cache.[/dim]")
        try:
            import language_tool_python
            self._lt_tool = language_tool_python.LanguageTool("id")
            self._console.print("[bold green]✓ LanguageTool siap.[/bold green]")
        except Exception as e:
            self._console.print(f"[yellow]⚠ Auto-correct tidak tersedia: {e}[/yellow]")
            self._lt_tool = None

    # ── Thread lifecycle ───────────────────────────────

    def start(self) -> None:
        """Mulai background transcription thread."""
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Kirim sinyal stop (poison pill) ke thread."""
        try:
            self._queue.put_nowait((None, None))
        except queue.Full:
            pass

    # ── Submit audio ───────────────────────────────────

    def submit(self, audio: np.ndarray, mic_sr: int) -> bool:
        """
        Kirim audio ke thread jika tidak sedang sibuk (non-blocking).
        Return True jika audio berhasil dikirim.
        """
        if self._queue.full():
            return False
        self._done.clear()
        self._queue.put((audio.copy(), mic_sr))
        return True

    def submit_and_wait(
        self, audio: np.ndarray, mic_sr: int, timeout: float = 5.0
    ) -> None:
        """
        Kirim audio dan tunggu hingga transkripsi selesai (blocking).
        Digunakan saat trailing-flush ketika pembicara berhenti.
        """
        if self._queue.full():
            return
        self._done.clear()
        self._queue.put((audio.copy(), mic_sr))
        self._done.wait(timeout=timeout)

    # ── Baca hasil ────────────────────────────────────

    def get_result(self) -> str:
        """Ambil hasil transkripsi terakhir tanpa menghapusnya."""
        with self._lock:
            return self._result["text"]

    def pop_result(self) -> str:
        """Ambil dan hapus hasil transkripsi terakhir."""
        with self._lock:
            text = self._result["text"]
            self._result["text"] = ""
            return text

    # ── Worker thread (internal) ───────────────────────

    def _worker(self) -> None:
        """Loop background thread: ambil audio → transkripsi → auto-correct → simpan."""
        cfg = self._cfg
        while True:
            try:
                audio_data, sr = self._queue.get(timeout=1)
                if audio_data is None:   # poison pill — berhenti
                    break

                # 1. Siapkan audio
                prepared = self._processor.prepare(audio_data, sr, cfg.whisper_samplerate)

                # 2. Transkripsi dengan Whisper
                res = self._model.transcribe(
                    prepared,
                    language=cfg.language,
                    task="transcribe",
                    initial_prompt=cfg.initial_prompt,
                    fp16=self._use_fp16,
                    beam_size=cfg.beam_size,
                    temperature=cfg.temperature_fallback,
                    condition_on_previous_text=cfg.condition_on_previous_text,
                    compression_ratio_threshold=cfg.compression_ratio_threshold,
                    no_speech_threshold=cfg.no_speech_threshold,
                    logprob_threshold=cfg.logprob_threshold,
                    word_timestamps=False,
                )
                text = res["text"].strip()

                # 3. Auto-correct dengan LanguageTool (jika aktif)
                if self._lt_tool and text:
                    try:
                        text = self._lt_tool.correct(text).strip()
                    except Exception:
                        pass  # fallback ke teks asli jika LanguageTool gagal

                # 4. Simpan hasil & beri sinyal selesai
                with self._lock:
                    self._result["text"] = text
                self._done.set()

            except queue.Empty:
                continue
            except Exception as e:
                self._console.log(f"[red]Transcription error: {e}[/red]")
                self._done.set()   # pastikan tidak deadlock
