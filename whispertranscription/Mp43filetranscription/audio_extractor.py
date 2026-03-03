"""
audio_extractor.py — Ekstraksi dan pengolahan audio
====================================================
Class AudioExtractor menangani:
  - Cek ketersediaan ffmpeg
  - Ekstrak audio dari video ke WAV mono 16kHz
  - Noise reduction (noisereduce)
  - Normalisasi amplitude
  - Split audio menjadi chunk
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING, List

import numpy as np
import soundfile as sf
from rich.console import Console

if TYPE_CHECKING:
    from .config import Config


class AudioExtractor:
    """Mengelola ekstraksi dan pra-pemrosesan audio dari file video/audio."""

    def __init__(self, cfg: "Config", console: Console | None = None):
        self._cfg = cfg
        self._console = console or Console()

    # ── FFmpeg ─────────────────────────────────────────

    def check_ffmpeg(self) -> bool:
        """Cek apakah ffmpeg tersedia di PATH."""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def extract_audio(self, video_path: str, output_wav: str) -> None:
        """Ekstrak audio dari video ke file WAV mono 16kHz menggunakan ffmpeg."""
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ac", "1",                                 # Mono
            "-ar", str(self._cfg.whisper_samplerate),    # 16kHz
            "-vn",                                       # Tak perlu video
            "-acodec", "pcm_s16le",                      # Format WAV standar
            output_wav,
        ]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(
                f"ffmpeg gagal mengekstrak audio:\n{result.stderr.decode('utf-8', errors='ignore')}"
            )

    # ── Audio Processing ──────────────────────────────

    def read_audio(self, wav_path: str) -> tuple[np.ndarray, int]:
        """Baca file WAV dan kembalikan (audio, sample_rate)."""
        audio, sr = sf.read(wav_path, dtype="float32")
        if audio.ndim > 1:
            audio = audio.mean(axis=1)  # Pastikan mono
        return audio, sr

    def apply_noise_reduction(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Terapkan noise reduction menggunakan noisereduce.
        Jika library tidak tersedia, kembalikan audio asli.
        """
        try:
            import noisereduce as nr
            reduced = nr.reduce_noise(
                y=audio,
                sr=sr,
                stationary=self._cfg.nr_stationary,
                prop_decrease=self._cfg.nr_prop_decrease,
            )
            return reduced.astype(np.float32)
        except ImportError:
            self._console.print(
                "[yellow]⚠ Library 'noisereduce' tidak ditemukan. Noise reduction dilewati.[/yellow]"
            )
            self._console.print("[dim]  Install dengan: pip install noisereduce[/dim]")
            return audio

    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalisasi amplitude audio ke rentang [-1, 1]."""
        peak = np.max(np.abs(audio))
        if peak > 0:
            return audio / peak
        return audio

    def split_into_chunks(self, audio: np.ndarray, sr: int) -> List[np.ndarray]:
        """Potong audio menjadi chunk-chunk dengan overlap kecil untuk konteks."""
        chunk_len = sr * self._cfg.chunk_seconds
        overlap   = sr * 2  # 2 detik overlap untuk menjaga konteks kalimat
        chunks: List[np.ndarray] = []
        start = 0

        while start < len(audio):
            end = min(start + chunk_len, len(audio))
            chunks.append(audio[start:end])
            start += chunk_len - overlap  # mundur 2 detik untuk overlap

        return chunks
