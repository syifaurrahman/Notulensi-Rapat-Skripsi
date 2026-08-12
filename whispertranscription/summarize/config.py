"""
config.py — Konfigurasi LexRank Summarizer (Enhanced 6-Step Pipeline)
=====================================================================
Edit nilai di sini untuk menyesuaikan perilaku ringkasan.
"""

import os
from dataclasses import dataclass, field


@dataclass
class SummaryConfig:
    # ── Step 4: LexRank Core (Dynamic Adaptation) ─────────
    # Rasio kompresi (0.20 = 20% dari total pembicaraan akan diekstrak)
    compression_ratio: float = 0.25
    
    # Batas minimum kalimat hasil ekstraksi agar ringkasan tidak terlalu pendek
    min_sentences: int = 8
    
    # Batas maksimum kalimat hasil ekstraksi agar tidak terlalu panjang/melebar
    max_sentences: int = 25


    # Minimum similarity antar kalimat untuk dianggap terhubung (edge di graf)
    similarity_threshold: float = 0.08

    # Toleransi konvergensi power iteration
    convergence_threshold: float = 1e-6

    # Maks iterasi power iteration
    max_iter: int = 200

    # Damping factor (seperti PageRank) — 0.85 standar
    damping: float = 0.85

    # ── Step 2: Sentence Segmentation ─────────────────────
    # Maksimum kata per segmen sebelum dipecah
    max_words_per_segment: int = 60

    # Minimum jumlah kata per kalimat (kalimat terlalu pendek diabaikan)
    min_words_per_sentence: int = 8

    # ── Step 3: Sentence Filtering ────────────────────────
    # Threshold Jaccard overlap untuk deduplikasi kalimat
    dedup_threshold: float = 0.65

    # Minimum karakter informatif per kalimat
    min_informative_chars: int = 30

    # ── Step 5: Reorganization ────────────────────────────
    # Jumlah kalimat per paragraf di output
    sentences_per_paragraph: int = 3

    # ── Step 1: Text Cleaning ─────────────────────────────
    # Whisper artifact patterns to remove (tambahan dari hardcoded)
    extra_whisper_artifacts: list = field(default_factory=lambda: [
        "terima kasih telah menonton",
        "terima kasih kerana menonton",
        "subscribe", "like dan subscribe",
        "recording in progress", "recording stop",
    ])

    # ── Step 6: Abstractive Rewriting (Ollama) ────────────
    # URL default Ollama — Docker-aware (env var OLLAMA_HOST)
    ollama_base_url: str = os.getenv('OLLAMA_HOST', 'http://ollama:11434')

    # Model yang direkomendasikan: llama3.2:3b atau gemma2:9b
    ollama_model: str = "llama3.2:3b"

    # Timeout (detik) untuk menunggu response Ollama
    # Ollama butuh waktu untuk load model dan generate teks
    ollama_timeout: int = 300

