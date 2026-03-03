"""
hallucination_filter.py — Filter halusinasi Whisper
=====================================================
Class HallucinationFilter mendeteksi teks yang kemungkinan
merupakan halusinasi Whisper (frasa berulang, spam YouTube, dll.)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config


class HallucinationFilter:
    """Deteksi dan filter halusinasi Whisper."""

    def __init__(self, cfg: "Config"):
        self._cfg = cfg

    def is_hallucination(self, text: str) -> bool:
        """
        Deteksi sederhana apakah teks mengandung halusinasi Whisper.
        Return True jika teks patut dibuang.
        """
        if not text or len(text.strip()) < self._cfg.min_text_length:
            return True

        # Deteksi kalimat yang persis berulang (50% teks sama)
        words = text.strip().split()
        if len(words) >= 6:
            half = " ".join(words[: len(words) // 2])
            second_half = " ".join(words[len(words) // 2 :])
            if half.strip() == second_half.strip():
                return True

        # Deteksi frasa halusinasi umum Whisper
        lower = text.lower()
        for phrase in self._cfg.hallucination_phrases:
            if lower.count(phrase) > 2:
                return True

        return False
