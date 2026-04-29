"""
noise_filter.py — Modul khusus untuk Noise Reduction
====================================================
Menangani filter pengurangan kebisingan pada rekaman audio.
Dipisahkan secara khusus untuk kemudahan pemeliharaan dan ekstensi.
"""

from __future__ import annotations
import numpy as np

class NoiseFilter:
    """Kelas pemrosesan untuk mengurangi noise."""
    
    def __init__(self, stationary: bool = True, prop_decrease: float = 0.80):
        self._nr_stationary = stationary
        self._nr_prop_decrease = prop_decrease

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Terapkan noise reduction pada audio.
        """
        try:
            import noisereduce as nr
            reduced = nr.reduce_noise(
                y=audio,
                sr=sr,
                stationary=self._nr_stationary,
                prop_decrease=self._nr_prop_decrease,
            )
            return reduced.astype(np.float32)
        except ImportError:
            return audio
