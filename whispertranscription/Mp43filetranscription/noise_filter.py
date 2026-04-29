"""
noise_filter.py — Modul khusus untuk Noise Reduction
====================================================
Menangani filter pengurangan kebisingan pada rekaman audio.
Dipisahkan khusus untuk kemudahan ekstensi dan pemeliharaan.
"""

from __future__ import annotations
import numpy as np
from rich.console import Console

class NoiseFilter:
    """Kelas khusus untuk mengurangi kebisingan (noise) dari audio."""
    
    def __init__(self, stationary: bool = True, prop_decrease: float = 0.85, console: Console | None = None):
        self._nr_stationary = stationary
        self._nr_prop_decrease = prop_decrease
        self._console = console or Console()

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Terapkan noise reduction menggunakan noisereduce.
        Jika library tidak tersedia, kembalikan audio asli dengan memberi peringatan di terminal.
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
            self._console.print(
                "[yellow]⚠ Library 'noisereduce' tidak ditemukan. Noise reduction dilewati.[/yellow]"
            )
            self._console.print("[dim]  Install dengan: pip install noisereduce[/dim]")
            return audio
