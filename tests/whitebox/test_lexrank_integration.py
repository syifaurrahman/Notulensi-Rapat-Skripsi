"""
test_lexrank_integration.py — Whitebox Test: LexRank End-to-End Integration
=============================================================================
Menguji pipeline end-to-end summarize() dan summarize_with_debug().

Teknik whitebox:
  - Path Coverage: semua jalur pipeline (short text, normal, fallback)
  - Integration Testing: verifikasi interaksi antar step
"""

import pytest


class TestSummarizeEndToEnd:
    """Whitebox testing end-to-end untuk summarize() dan summarize_with_debug()."""

    # ── TC-INT.1: Teks kosong ─────────────────────────────────────

    def test_summarize_empty_text(self, summarizer, sample_empty_text):
        """Menguji jalur early return: teks kosong → return langsung."""
        result = summarizer.summarize_with_debug(sample_empty_text)
        assert result['ringkasan'] == ''
        assert result['ranked_sentences'] == []
        assert result['lexrank_extractive'] == ''
        assert result['ollama_result'] is None

    # ── TC-INT.2: Teks sangat pendek (< 50 karakter) ─────────────

    def test_summarize_very_short_text(self, summarizer, sample_short_text):
        """Menguji jalur early return: teks < 50 chars → return as-is."""
        result = summarizer.summarize_with_debug(sample_short_text)
        assert result['ringkasan'] == sample_short_text.strip()
        assert result['ranked_sentences'] == []

    # ── TC-INT.3: Teks normal (Whisper transcription) ─────────────

    def test_summarize_normal_whisper_text(self, summarizer, sample_whisper_text):
        """Menguji jalur normal: teks Whisper diproses melalui semua 6 step."""
        result = summarizer.summarize_with_debug(sample_whisper_text)
        ringkasan = result['ringkasan']
        # Ringkasan harus ada dan tidak kosong
        assert len(ringkasan) > 0
        # Artefak Whisper harus sudah dibersihkan
        assert "terima kasih telah menonton" not in ringkasan.lower()
        assert "[music]" not in ringkasan
        # Filler harus sudah dihapus dari ringkasan
        assert "recording in progress" not in ringkasan.lower()

    # ── TC-INT.4: Teks panjang realistis ──────────────────────────

    def test_summarize_long_text(self, summarizer, sample_long_text):
        """Menguji jalur penuh: teks panjang → LexRank extraction → format paragraf."""
        result = summarizer.summarize_with_debug(sample_long_text)
        ringkasan = result['ringkasan']
        ranked = result['ranked_sentences']
        # Ringkasan harus ada
        assert len(ringkasan) > 0
        # Ranked sentences harus ada
        assert len(ranked) > 0
        # Setiap ranked sentence harus punya rank dan score
        for item in ranked:
            assert 'rank' in item
            assert 'score' in item
            assert 'sentence' in item
        # Rank harus dimulai dari 1
        ranks = [item['rank'] for item in ranked]
        assert min(ranks) == 1
        # Ringkasan harus lebih pendek dari teks asli
        assert len(ringkasan) < len(sample_long_text)

    # ── TC-INT.5: summarize() wrapper ─────────────────────────────

    def test_summarize_wrapper(self, summarizer, sample_long_text):
        """Menguji bahwa summarize() mengembalikan string yang sama dengan ringkasan dari summarize_with_debug()."""
        from unittest.mock import patch
        with patch.object(summarizer.ollama, 'rewrite', return_value="Ringkasan deterministik"):
            simple = summarizer.summarize(sample_long_text)
            debug = summarizer.summarize_with_debug(sample_long_text)
            assert simple == debug['ringkasan']


    # ── TC-INT.6: Output lexrank_extractive selalu ada ────────────

    def test_lexrank_extractive_always_present(self, summarizer, sample_long_text):
        """Memastikan lexrank_extractive selalu terisi (bahkan jika Ollama aktif)."""
        result = summarizer.summarize_with_debug(sample_long_text)
        assert result['lexrank_extractive'] is not None
        assert len(result['lexrank_extractive']) > 0

    # ── TC-INT.7: Filtered sentences fallback ─────────────────────

    def test_filtered_empty_fallback(self, summarizer):
        """Menguji jalur fallback: jika step 3 filter semua, gunakan raw_sentences terpanjang."""
        # Teks yang banyak noise tapi cukup panjang
        text = (
            "Oke baik ya jadi gini kan kita tuh harus ya membahas ini. "
            "Nah terus kan kita juga harus ya kan mempertimbangkan itu. "
            "Eee jadi gitu ya kan kita ini ya sudah harus mulai. "
            "Ya kan jadi gitu ya kita harus terus maju. "
            "Oke baik ya jadi kita lanjutkan saja ke topik berikutnya. "
        ) * 3  # Repeat agar >50 chars
        result = summarizer.summarize_with_debug(text)
        # Harus tetap menghasilkan sesuatu
        assert isinstance(result['ringkasan'], str)
