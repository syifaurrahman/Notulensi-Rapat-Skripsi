"""
noise_filter.py — Modul khusus untuk Noise Reduction
====================================================
Menangani filter pengurangan kebisingan pada rekaman audio.
Dipisahkan khusus untuk kemudahan ekstensi dan pemeliharaan.

Perbaikan: Noise reduction dilakukan per-chunk (chunked NR) untuk
menghindari alokasi memori besar (OOM) pada audio berdurasi panjang.
"""

from __future__ import annotations
import numpy as np
from rich.console import Console

# Ukuran segmen untuk chunked NR (dalam detik)
_NR_CHUNK_SECONDS = 30


class NoiseFilter:
    """Kelas khusus untuk mengurangi kebisingan (noise) dari audio."""

    def __init__(
        self,
        stationary: bool = True,
        prop_decrease: float = 0.85,
        console: Console | None = None,
    ):
        self._nr_stationary = stationary
        self._nr_prop_decrease = prop_decrease
        self._console = console or Console()

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Terapkan noise reduction secara chunked (per 30 detik) untuk
        menghindari OOM pada audio panjang.

        Jika library tidak tersedia, kembalikan audio asli.
        """
        try:
            import noisereduce as nr
        except ImportError:
            self._console.print(
                "[yellow]⚠ Library 'noisereduce' tidak ditemukan. Noise reduction dilewati.[/yellow]"
            )
            self._console.print("[dim]  Install dengan: pip install noisereduce[/dim]")
            return audio

        chunk_len = sr * _NR_CHUNK_SECONDS
        total_samples = len(audio)

        # Jika audio pendek, proses sekaligus
        if total_samples <= chunk_len:
            reduced = nr.reduce_noise(
                y=audio,
                sr=sr,
                stationary=self._nr_stationary,
                prop_decrease=self._nr_prop_decrease,
            )
            return reduced.astype(np.float32)

        # Audio panjang → proses per chunk agar hemat memori
        self._console.print(
            f"[dim]  Noise reduction chunked ({_NR_CHUNK_SECONDS}s/chunk) "
            f"— total {total_samples / sr / 60:.1f} menit...[/dim]"
        )
        output_chunks: list[np.ndarray] = []
        start = 0
        while start < total_samples:
            end = min(start + chunk_len, total_samples)
            segment = audio[start:end]
            reduced_segment = nr.reduce_noise(
                y=segment,
                sr=sr,
                stationary=self._nr_stationary,
                prop_decrease=self._nr_prop_decrease,
            )
            output_chunks.append(reduced_segment.astype(np.float32))
            start = end

        return np.concatenate(output_chunks)
