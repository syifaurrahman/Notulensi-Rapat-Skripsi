"""
audio_capture.py — Mic stream, buffer audio, dan VAD
=====================================================
Kelas AudioCapture mengelola:
  - Pemilihan mikrofon dari daftar
  - Membuka/menutup sounddevice InputStream
  - Akumulasi audio ke buffer internal
  - Voice Activity Detection (VAD) via perhitungan RMS
"""

from __future__ import annotations

import queue
from typing import Optional, TYPE_CHECKING

import numpy as np
import sounddevice as sd
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from config import Config


class AudioCapture:
    """
    Mengelola mic stream, buffer audio, dan VAD.

    Cara pakai:
      cap = AudioCapture(cfg, console)
      cap.select_mic()   # tampilkan daftar & minta input user
      cap.start()        # buka stream

      # Di dalam loop:
      cap.drain_queue()           # pindah audio dari queue ke buffer
      rms = cap.get_rms()         # cek apakah ada suara
      buf = cap.get_buffer()      # ambil salinan buffer
      cap.clear_buffer()          # kosongkan buffer

      cap.stop()         # tutup stream & bersihkan
    """

    def __init__(self, cfg: "Config", console: Console):
        self._cfg     = cfg
        self._console = console

        self._queue  : queue.Queue                 = queue.Queue()
        self._buffer : np.ndarray                  = np.zeros(0, dtype=np.float32)
        self._stream : Optional[sd.InputStream]    = None

        self.device_id : Optional[int] = None
        self.mic_sr    : int           = cfg.whisper_samplerate

    # ── Pilih mikrofon ─────────────────────────────────

    def select_mic(self) -> None:
        """Tampilkan tabel daftar mic dan minta user memasukkan ID."""
        table = Table(title="🎤 Daftar Mikrofon Tersedia", show_lines=True)
        table.add_column("ID",                  style="cyan",    no_wrap=True)
        table.add_column("Nama Device",         style="magenta")
        table.add_column("Sample Rate Default", justify="right", style="green")

        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                table.add_row(str(i), dev["name"], f"{int(dev['default_samplerate'])} Hz")

        self._console.print(table)
        try:
            choice         = int(self._console.input("[bold yellow]Masukkan ID Mic: [/bold yellow]"))
            info           = sd.query_devices(choice, "input")
            self.device_id = choice
            self.mic_sr    = int(info["default_samplerate"])
        except Exception as e:
            self._console.print(f"[yellow]⚠ {e} — Menggunakan mikrofon default.[/yellow]")
            self.device_id = None
            self.mic_sr    = self._cfg.whisper_samplerate

    # ── Stream lifecycle ───────────────────────────────

    def start(self) -> None:
        """Buka dan mulai mic stream."""
        self._stream = sd.InputStream(
            device=self.device_id,
            channels=1,
            samplerate=self.mic_sr,
            dtype=np.float32,
            callback=self._callback,
            blocksize=int(self.mic_sr * 0.1),  # 100ms per block
        )
        self._stream.start()

    def stop(self) -> None:
        """Hentikan dan tutup mic stream."""
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    # ── Buffer management ──────────────────────────────

    def drain_queue(self) -> None:
        """Pindahkan semua chunk audio dari queue ke buffer internal."""
        while not self._queue.empty():
            chunk = self._queue.get()
            self._buffer = np.concatenate((self._buffer, chunk.flatten()))

    def get_buffer(self) -> np.ndarray:
        """Kembalikan salinan buffer saat ini."""
        return self._buffer.copy()

    def clear_buffer(self) -> None:
        """Kosongkan buffer."""
        self._buffer = np.zeros(0, dtype=np.float32)

    def trim_buffer(self, max_sec: float) -> None:
        """Potong buffer agar tidak melebihi max_sec detik audio."""
        max_samples = int(self.mic_sr * max_sec)
        if len(self._buffer) > max_samples:
            self._buffer = self._buffer[-max_samples:]

    def buffer_duration_sec(self) -> float:
        """Kembalikan durasi audio dalam buffer dalam satuan detik."""
        return len(self._buffer) / self.mic_sr if self.mic_sr > 0 else 0.0

    # ── VAD ────────────────────────────────────────────

    def get_rms(self) -> float:
        """
        Hitung RMS (volume) dari 1 detik terakhir buffer.
        Digunakan untuk mendeteksi apakah ada suara (Voice Activity Detection).
        """
        latest = self._buffer[-int(self.mic_sr):]
        if len(latest) == 0:
            return 0.0
        return float(np.sqrt(np.mean(latest ** 2)))

    # ── Callback internal ──────────────────────────────

    def _callback(self, indata, frames, time_info, status) -> None:
        """Callback sounddevice — masukkan audio ke queue saat data tiba."""
        if status:
            self._console.log(f"[yellow]{status}[/yellow]")
        self._queue.put(indata.copy())
