"""
hallucination_filter.py — Filter output hallusinasi Whisper
===========================================================
Kelas HallucinationFilter mendeteksi teks Whisper yang merupakan
hallusinasi (teks palsu yang dihasilkan saat tidak ada suara nyata).
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Config


class HallucinationFilter:
    """
    Mendeteksi dan memfilter output hallusinasi dari Whisper.

    Hallusinasi terjadi ketika Whisper menghasilkan teks dari kebisingan
    latar atau audio yang tidak jelas, biasanya berupa frasa generik
    seperti 'Thank you.' atau 'Terima kasih.'.
    """

    def __init__(self, cfg: "Config"):
        self._phrases  = cfg.hallucination_phrases
        self._min_len  = cfg.min_text_length

    def is_hallucination(self, text: str) -> bool:
        """
        Kembalikan True jika teks dianggap hallusinasi dan harus dibuang.

        Kriteria:
          1. Teks kosong atau terlalu pendek
          2. Cocok dengan frasa hallusinasi umum (exact atau tanpa tanda baca)
          3. Mengandung pengulangan: separuh pertama == separuh kedua
        """
        if not text or len(text.strip()) < self._min_len:
            return True

        lower       = text.lower().strip()
        lower_clean = re.sub(r"[^\w\s]", "", lower).strip()

        for phrase in self._phrases:
            phrase_clean = re.sub(r"[^\w\s]", "", phrase).strip()

            # Exact match (dengan atau tanpa tanda baca)
            if lower == phrase or lower_clean == phrase_clean:
                return True

            # Teks sangat pendek yang memuat frasa tersebut
            if lower.count(phrase) >= 1 and len(lower) < len(phrase) + 20:
                return True

            # Frasa muncul lebih dari 2 kali (repetisi)
            if lower.count(phrase) > 2:
                return True

        # Deteksi pengulangan: separuh pertama == separuh kedua
        words = text.strip().split()
        if len(words) >= 6:
            mid  = len(words) // 2
            half = " ".join(words[:mid])
            rest = " ".join(words[mid:])
            if half.strip() == rest.strip():
                return True

        return False
