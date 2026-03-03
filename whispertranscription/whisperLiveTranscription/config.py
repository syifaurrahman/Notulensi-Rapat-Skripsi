"""
config.py — Konfigurasi terpusat untuk Whisper Live Transcription
=================================================================
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
    model_size: str       = "small"   # tiny | base | small | medium | large
    language: str         = "id"      # Bahasa Indonesia
    use_gpu: bool         = field(default_factory=lambda: torch.cuda.is_available())  # Auto-detect GPU
    use_autocorrect: bool = True      # LanguageTool auto-correct (Bahasa Indonesia)

    # ── Audio ─────────────────────────────────────────
    whisper_samplerate: int = 16000   # Sample rate wajib Whisper

    # ── VAD (Voice Activity Detection) ───────────────
    vad_threshold: float     = 0.01   # RMS min dianggap ada suara (0.005–0.05)
    debug_rms: bool          = True   # Tampilkan nilai RMS di log
    buffer_max_sec: float    = 20.0   # Buffer maks sebelum di-flush (detik)
    min_process_sec: float   = 2.5    # Buffer minimal sebelum diproses (detik)
    silence_pause_sec: float = 1.2    # Durasi hening sebelum trailing-flush (detik)

    # ── Anti-Hallucination Whisper ────────────────────
    beam_size: int                     = 3
    temperature_fallback: tuple        = (0.0, 0.2, 0.4)
    compression_ratio_threshold: float = 2.2
    no_speech_threshold: float         = 0.45
    logprob_threshold: float           = -1.0
    condition_on_previous_text: bool   = False
    initial_prompt: str = (
        "Rapat ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris. "
        "Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. "
        "Contoh: machine learning, deep learning, framework, update, meeting, deploy, "
        "feedback, insight, dashboard, budget, deadline, project, target, maybe, "
        "okay, yes, no, stakeholder, follow up, approval, training, model, dataset."
    )

    # ── Noise Reduction ───────────────────────────────
    nr_stationary: bool     = True    # Cocok untuk noise stasioner (AC, kipas)
    nr_prop_decrease: float = 0.80    # Agresivitas noise reduction (0.0–1.0)

    # ── Output ────────────────────────────────────────
    output_dir: str = field(
        default_factory=lambda: os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "hasil"
        )
    )

    # ── Filter Hallusinasi ────────────────────────────
    min_text_length: int = 4
    hallucination_phrases: List[str] = field(default_factory=lambda: [
        # Indonesia
        "terima kasih sudah menonton", "jangan lupa subscribe",
        "like dan subscribe", "sampai jumpa di video berikutnya",
        "semoga bermanfaat", "sampai jumpa", "terima kasih", "sampai bertemu",
        # Inggris — hallusinasi pendek umum Whisper
        "thank you", "thanks", "thank you.", "thanks.", "you.", "bye.",
        "bye bye", "goodbye", "see you", "see you later",
        "okay.", "ok.", "yes.", "no.", ".",
        "don't forget to subscribe", "please subscribe",
        "thank you for watching", "thank you for listening",
        "subscribe", "[music]", "(musik)", "[applause]", "[laughter]", "♪",
    ])
