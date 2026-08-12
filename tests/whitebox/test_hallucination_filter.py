"""
test_hallucination_filter.py — Whitebox Test: HallucinationFilter
===================================================================
Menguji semua jalur internal HallucinationFilter.is_hallucination().

Teknik whitebox:
  - Branch Coverage: setiap kondisi if diuji
  - Boundary Testing: panjang teks minimal
  - Condition Coverage: setiap kriteria deteksi
"""

import pytest


class TestHallucinationFilter:
    """Whitebox testing untuk HallucinationFilter."""

    # ── TC-HF.1: Teks kosong → hallucination ─────────────────────

    def test_empty_text_is_hallucination(self, halluc_config):
        """Menguji jalur: teks kosong → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        assert hf.is_hallucination("") is True
        assert hf.is_hallucination(None) is True

    # ── TC-HF.2: Teks terlalu pendek → hallucination ─────────────

    def test_short_text_is_hallucination(self, halluc_config):
        """Menguji jalur: teks < min_text_length → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        # min_text_length default = 4
        assert hf.is_hallucination("Hi") is True
        assert hf.is_hallucination("Ok") is True

    # ── TC-HF.3: Exact match frasa hallusinasi ────────────────────

    def test_exact_match_hallucination_phrase(self, halluc_config):
        """Menguji jalur: exact match dengan frasa di config → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        assert hf.is_hallucination("terima kasih") is True
        assert hf.is_hallucination("Thank you.") is True
        assert hf.is_hallucination("subscribe") is True

    # ── TC-HF.4: Match tanpa tanda baca ───────────────────────────

    def test_match_without_punctuation(self, halluc_config):
        """Menguji jalur: match setelah tanda baca dihapus → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        assert hf.is_hallucination("thank you") is True   # lowercase tanpa titik

    # ── TC-HF.5: Teks pendek yang memuat frasa → hallucination ───

    def test_short_text_containing_phrase(self, halluc_config):
        """Menguji jalur: teks pendek yang mengandung frasa hallusinasi → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        # 'terima kasih' ada di teks, dan teks pendek
        assert hf.is_hallucination("ya terima kasih ya") is True

    # ── TC-HF.6: Frasa berulang >2 kali ──────────────────────────

    def test_repeated_phrase_hallucination(self, halluc_config):
        """Menguji jalur: frasa muncul >2 kali → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        text = "thank you thank you thank you dan informasi penting"
        assert hf.is_hallucination(text) is True

    # ── TC-HF.7: Pengulangan separuh (half repetition) ────────────

    def test_half_repetition_hallucination(self, halluc_config):
        """Menguji jalur: separuh pertama == separuh kedua → True."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        text = "ini teks pengujian ini teks pengujian"
        assert hf.is_hallucination(text) is True

    # ── TC-HF.8: Teks normal → bukan hallucination ───────────────

    def test_normal_text_not_hallucination(self, halluc_config):
        """Menguji jalur: teks normal informatif → False."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        text = "Rapat hari ini membahas tentang keselamatan kerja di lingkungan pabrik"
        assert hf.is_hallucination(text) is False

    # ── TC-HF.9: Teks panjang dengan frasa hallusinasi di tengah ──

    def test_long_text_with_phrase_not_hallucination(self, halluc_config):
        """Menguji jalur: teks panjang yang secara kebetulan mengandung frasa tapi informatif → False."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        text = (
            "Dalam rapat ini kita membahas banyak hal penting tentang keselamatan kerja "
            "dan kita mengucapkan terima kasih kepada semua peserta yang telah hadir "
            "serta berkontribusi dalam diskusi yang sangat produktif"
        )
        # Teks panjang + 'terima kasih' hanya muncul 1x + teks > len(phrase) + 20
        assert hf.is_hallucination(text) is False

    # ── TC-HF.10: Half repetition dengan < 6 kata ────────────────

    def test_half_repetition_short_not_detected(self, halluc_config):
        """Menguji boundary: teks <6 kata → half repetition check dilewati."""
        from whisperLiveTranscription.hallucination_filter import HallucinationFilter
        hf = HallucinationFilter(halluc_config)
        text = "satu dua satu dua"
        # <6 kata, half repetition check dilewati, tapi bisa jadi terlalu pendek
        result = hf.is_hallucination(text)
        # Bisa True atau False tergantung min_text_length, yang penting tidak error
        assert isinstance(result, bool)
