"""
test_lexrank_step1_cleaning.py — Whitebox Test: Step 1 Text Cleaning
=====================================================================
Menguji semua jalur internal _step1_text_cleaning() dan helper-nya.

Teknik whitebox:
  - Statement Coverage: setiap baris dieksekusi
  - Branch Coverage: setiap kondisi if/else diuji
  - Path Coverage: kombinasi jalur berbeda
"""

import re
import pytest


class TestStep1TextCleaning:
    """Whitebox testing untuk Step 1: Text Cleaning."""

    # ── TC-1.1: Hapus karakter non-printable ──────────────────────

    def test_remove_non_printable_chars(self, summarizer):
        """Menguji jalur 1a: karakter kontrol \x00-\x08, \x0b, \x0e-\x1f, \x7f dihapus."""
        text = "Halo\x00 dunia\x07 ini\x0b teks\x1f bersih\x7f ya"
        result = summarizer._step1_text_cleaning(text)
        # Tidak boleh ada karakter kontrol tersisa
        assert '\x00' not in result
        assert '\x07' not in result
        assert '\x0b' not in result
        assert '\x1f' not in result
        assert '\x7f' not in result
        # Kata-kata tetap ada
        assert "halo" in result.lower() or "dunia" in result.lower()

    # ── TC-1.2: Hapus artefak bracket [music], (applause) ─────────

    def test_remove_bracket_artifacts(self, summarizer):
        """Menguji jalur 1b: artefak dalam [...] dan (...) dihapus."""
        text = "Selamat pagi [music] kita mulai (applause) rapat hari ini"
        result = summarizer._step1_text_cleaning(text)
        assert "[music]" not in result
        assert "(applause)" not in result
        assert "selamat" in result.lower()
        assert "rapat" in result.lower()

    # ── TC-1.3: Hapus halusinasi Whisper (frasa panjang) ──────────

    def test_remove_whisper_hallucination_phrases(self, summarizer):
        """Menguji jalur 1c: frasa halusinasi dari config dihapus."""
        text = "Kita bahas topik ini. Terima kasih telah menonton. Lanjut ke agenda berikutnya."
        result = summarizer._step1_text_cleaning(text)
        assert "terima kasih telah menonton" not in result.lower()
        assert "topik" in result.lower()
        assert "agenda" in result.lower()

    # ── TC-1.4: Hapus filler inline (eee, aaa, uum) ───────────────

    def test_remove_inline_fillers(self, summarizer):
        """Menguji jalur 1d: bunyi filler panjang dihapus via regex."""
        text = "Jadi eee kita harus aaa membahas ini uuu segera"
        result = summarizer._step1_text_cleaning(text)
        # Filler bunyi panjang dihapus
        assert "eee" not in result.lower()
        assert "aaa" not in result.lower()
        assert "uuu" not in result.lower()
        # Kata bermakna tetap ada
        assert "membahas" in result.lower()


    # ── TC-1.5: Normalisasi tanda baca ganda ──────────────────────

    def test_normalize_duplicate_punctuation(self, summarizer):
        """Menguji jalur 1e: tanda baca berulang dinormalisasi."""
        text = "Apa ini... Bagaimana??? Hebat!!! Ya,, memang"
        result = summarizer._step1_text_cleaning(text)
        # Titik ganda → 1 titik
        assert "..." not in result
        assert "???" not in result
        assert "!!!" not in result
        assert ",," not in result

    # ── TC-1.6: Hapus pengulangan kata berturut ───────────────────

    def test_remove_word_repetition(self, summarizer):
        """Menguji jalur 1f: kata berulang >2x dikurangi jadi 1x."""
        text = "Jadi jadi jadi kita harus membahas ini"
        result = summarizer._step1_text_cleaning(text)
        # Hanya boleh muncul 1x 'jadi' setelah cleaning (filler mungkin dihapus)
        count = result.lower().split().count("jadi")
        assert count <= 1

    # ── TC-1.7: Koreksi typo Whisper ──────────────────────────────

    def test_typo_correction(self, summarizer):
        """Menguji jalur 1g: typo umum dikoreksi via _apply_typo_corrections()."""
        text = "Kita menggunakan atml dan css untuk membuat leot website"
        result = summarizer._step1_text_cleaning(text)
        assert "HTML" in result
        assert "CSS" in result
        assert "layout" in result

    # ── TC-1.8: Normalisasi spasi ─────────────────────────────────

    def test_normalize_whitespace(self, summarizer):
        """Menguji jalur 1h: spasi ganda/triple dinormalisasi."""
        text = "Kita   harus    membahas   topik   ini"
        result = summarizer._step1_text_cleaning(text)
        assert "  " not in result
        assert "kita" in result.lower()


class TestApplyTypoCorrections:
    """Whitebox testing untuk helper _apply_typo_corrections()."""

    def test_case_insensitive_correction(self, summarizer):
        """Koreksi typo case-insensitive."""
        text = "Pakai ATML bukan chess"
        result = summarizer._apply_typo_corrections(text)
        assert "HTML" in result
        assert "CSS" in result

    def test_no_false_positive_on_normal_text(self, summarizer):
        """Teks normal tanpa typo tidak diubah (kecuali kata yang ada di dict)."""
        text = "Ini teks normal tanpa typo apapun"
        result = summarizer._apply_typo_corrections(text)
        assert "normal" in result.lower()
        assert "tanpa" in result.lower()

    def test_word_boundary_respect(self, summarizer):
        """Koreksi typo menghormati batas kata (word boundary)."""
        # 'sam' ada di dict → XAMPP, tapi 'samsung' seharusnya tidak berubah
        text = "Perangkat Samsung digunakan untuk testing"
        result = summarizer._apply_typo_corrections(text)
        # 'samsung' mengandung 'sam' tapi word boundary harusnya mencegah
        # Karena regex \bsam\b hanya match kata 'sam' standalone
        assert "samsung" in result.lower() or "Samsung" in result
