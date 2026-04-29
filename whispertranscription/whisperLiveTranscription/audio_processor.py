"""
audio_processor.py — Pemrosesan audio: resample, noise reduction, normalisasi
=============================================================================
Kelas AudioProcessor menyediakan pipeline pemrosesan audio yang digunakan
sebelum audio dikirim ke Whisper untuk transkripsi.
"""

from __future__ import annotations

from math import gcd
from typing import TYPE_CHECKING

import numpy as np
from scipy import signal as scipy_signal

from noise_filter import NoiseFilter

if TYPE_CHECKING:
    from config import Config


class AudioProcessor:
    """
    Utilitas pemrosesan audio.

    Pipeline utama (method prepare):
      audio mentah → resample → noise reduction → normalisasi → siap untuk Whisper
    """

    def __init__(self, cfg: "Config"):
        self.noise_filter = NoiseFilter(
            stationary=cfg.nr_stationary,
            prop_decrease=cfg.nr_prop_decrease
        )

    # ── Pipeline utama ─────────────────────────────────

    def prepare(self, audio: np.ndarray, from_sr: int, to_sr: int) -> np.ndarray:
        """
        Jalankan pipeline lengkap:
          resample → noise reduction → normalisasi
        """
        audio = self.resample(audio, from_sr, to_sr)
        audio = self.noise_filter.apply(audio, to_sr)
        audio = self.normalize(audio)
        return audio

    # ── Tahapan individual ──────────────────────────────

    def resample(self, audio: np.ndarray, from_sr: int, to_sr: int) -> np.ndarray:
        """
        Resample audio menggunakan scipy.signal.resample_poly.
        Lebih akurat dibanding metode np.linspace + integer index.
        """
        if from_sr == to_sr:
            return audio
        common = gcd(from_sr, to_sr)
        up     = to_sr   // common
        down   = from_sr // common
        return scipy_signal.resample_poly(audio, up, down).astype(np.float32)

    def normalize(self, audio: np.ndarray) -> np.ndarray:
        """Normalisasi amplitude audio ke rentang [-1, 1]."""
        peak = np.max(np.abs(audio))
        if peak > 0:
            return (audio / peak).astype(np.float32)
        return audio
