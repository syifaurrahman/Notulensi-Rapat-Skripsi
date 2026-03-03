"""
config.py — Konfigurasi terpusat untuk Transkripsi File Video/Audio
===================================================================
Edit nilai-nilai di sini untuk menyesuaikan perilaku aplikasi.
Tidak perlu menyentuh file lain.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

import torch


@dataclass
class Config:
    """Semua konfigurasi aplikasi dalam satu dataclass."""

    # ── Model & Bahasa ────────────────────────────────
    model_size: str       = "small"    # tiny | base | small | medium | large
    language: str         = "id"       # Bahasa Indonesia
    use_gpu: bool         = field(default_factory=lambda: torch.cuda.is_available())  # Auto-detect GPU

    # ── Audio ─────────────────────────────────────────
    chunk_seconds: int      = 30       # Durasi setiap chunk transkripsi (detik)
    whisper_samplerate: int = 16000    # Sample rate wajib Whisper

    # ── Anti-Hallucination Whisper ────────────────────
    beam_size: int                     = 5
    temperature_fallback: tuple        = (0.0, 0.2, 0.4, 0.6)
    compression_ratio_threshold: float = 2.2    # Buang teks yang terlalu repetitif
    no_speech_threshold: float         = 0.6    # Abaikan segment yang kurang meyakinkan
    logprob_threshold: float           = -1.0
    condition_on_previous_text: bool   = False   # Cegah carry-over halusinasi antar chunk

    # ── Noise Reduction ───────────────────────────────
    nr_stationary: bool     = True     # Cocok untuk noise stasioner (AC, kipas)
    nr_prop_decrease: float = 0.85     # Agresivitas noise reduction (0.0–1.0)

    # ── Output ────────────────────────────────────────
    output_dir: str = field(
        default_factory=lambda: os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hasil"
        )
    )

    # ── Filter Halusinasi ────────────────────────────
    min_text_length: int = 2
    hallucination_phrases: List[str] = field(default_factory=lambda: [
        "terima kasih sudah menonton", "subscribe",
        "like dan subscribe", "semoga bermanfaat",
        "sampai jumpa di video berikutnya",
        "don't forget to", "please subscribe",
        "thank you for watching", "music",
        "[music]", "(musik)",
    ])

    # ── File Picker ──────────────────────────────────
    file_extensions: List[str] = field(default_factory=lambda: [
        "mp4", "mov", "avi", "mkv", "webm", "flv", "wmv", "m4v", "mp3",
    ])
