"""
test_lexrank_step6_format.py — Whitebox Test: Step 6 Final Summarization
==========================================================================
Menguji semua jalur internal _step6_final_format() dan helper-nya.

Teknik whitebox:
  - Statement Coverage: setiap baris format dieksekusi
  - Branch Coverage: input kosong, kalimat tunggal, multiple paragraphs
"""

import pytest


class TestStep6FinalFormat:
    """Whitebox testing untuk Step 6: Final Format."""

    # ── TC-6.1: Format normal → paragraf ──────────────────────────

    def test_format_normal_paragraphs(self, summarizer, sample_clean_sentences):
        """Menguji jalur normal: kalimat dikelompokkan per paragraf."""
        result = summarizer._step6_final_format(sample_clean_sentences)
        assert isinstance(result, str)
        assert len(result) > 0
        # Harus ada paragraf (dipisahkan \n\n)
        paragraphs = result.split('\n\n')
        assert len(paragraphs) >= 1

    # ── TC-6.2: Input kosong ──────────────────────────────────────

    def test_format_empty_input(self, summarizer):
        """Menguji jalur early return: input kosong → string kosong."""
        result = summarizer._step6_final_format([])
        assert result == ""

    # ── TC-6.3: Single sentence ───────────────────────────────────

    def test_format_single_sentence(self, summarizer):
        """Menguji jalur: hanya 1 kalimat → 1 paragraf."""
        sentences = ["Keselamatan kerja adalah tanggung jawab bersama seluruh karyawan."]
        result = summarizer._step6_final_format(sentences)
        assert "keselamatan" in result.lower()
        paragraphs = result.split('\n\n')
        assert len(paragraphs) == 1

    # ── TC-6.4: Grouping sesuai sentences_per_paragraph ───────────

    def test_grouping_by_config(self, summarizer):
        """Menguji bahwa kalimat dikelompokkan sesuai cfg.sentences_per_paragraph."""
        sentences = [
            "Kalimat satu tentang keselamatan kerja di lingkungan pabrik.",
            "Kalimat dua tentang penggunaan alat pelindung diri wajib.",
            "Kalimat tiga tentang pelatihan evakuasi bencana kebakaran.",
            "Kalimat empat tentang pengecekan berkala peralatan keselamatan.",
            "Kalimat lima tentang sistem pelaporan insiden kecelakaan.",
            "Kalimat enam tentang komitmen manajemen terhadap keselamatan.",
            "Kalimat tujuh tentang reward bagi unit kerja terbaik.",
        ]
        result = summarizer._step6_final_format(sentences)
        paragraphs = result.split('\n\n')
        group_size = summarizer.cfg.sentences_per_paragraph
        expected_paragraphs = (len(sentences) + group_size - 1) // group_size
        assert len(paragraphs) == expected_paragraphs

    # ── TC-6.5: Kalimat dengan spasi ganda di-polish ─────────────

    def test_polish_cleans_whitespace(self, summarizer):
        """Menguji _polish_sentence(): spasi ganda dan tanda baca dibersihkan."""
        sentences = [
            "kalimat  dengan   spasi   ganda dan  juga tanda baca.. yang berlebihan",
        ]
        result = summarizer._step6_final_format(sentences)
        assert "  " not in result
        assert ".." not in result


class TestPolishSentence:
    """Whitebox testing untuk helper _polish_sentence()."""

    def test_empty_sentence(self, summarizer):
        """String kosong → string kosong."""
        result = summarizer._polish_sentence("")
        assert result == ""

    def test_whitespace_only(self, summarizer):
        """String hanya spasi → string kosong."""
        result = summarizer._polish_sentence("   ")
        assert result == ""

    def test_add_period(self, summarizer):
        """Kalimat tanpa tanda baca akhir ditambahkan titik."""
        result = summarizer._polish_sentence("penggunaan helm safety wajib bagi semua pekerja")
        assert result.endswith('.')

    def test_capitalize_first_letter(self, summarizer):
        """Huruf pertama dikapitalisasi."""
        result = summarizer._polish_sentence("semua karyawan wajib mematuhi aturan keselamatan")
        assert result[0].isupper()

    def test_remove_leading_comma(self, summarizer):
        """Koma di awal kalimat dihapus."""
        result = summarizer._polish_sentence(", ini kalimat yang dimulai dengan koma tanpa alasan")
        assert not result.startswith(',')
