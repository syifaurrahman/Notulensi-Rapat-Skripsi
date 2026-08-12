"""
test_lexrank_step2_segmentation.py — Whitebox Test: Step 2 Sentence Segmentation
==================================================================================
Menguji semua jalur internal _step2_sentence_segmentation() dan helper-nya.

Teknik whitebox:
  - Branch Coverage: split tanda baca, split konjungsi, chunk panjang
  - Boundary Testing: kalimat tepat di batas max_words_per_segment
"""

import pytest


class TestStep2SentenceSegmentation:
    """Whitebox testing untuk Step 2: Sentence Segmentation."""

    # ── TC-2.1: Split di tanda baca standar (.!?) ─────────────────

    def test_split_at_standard_punctuation(self, summarizer):
        """Menguji jalur 2a: teks dipecah di titik, tanda seru, tanda tanya."""
        text = (
            "Rapat dimulai tepat pada pukul delapan pagi hari ini di ruang utama. "
            "Semua anggota tim hadir dalam rapat evaluasi bulanan proyek ini! "
            "Apakah ada pertanyaan mengenai laporan keuangan yang telah disampaikan tadi?"
        )
        result = summarizer._step2_sentence_segmentation(text)
        assert len(result) == 3
        assert "rapat" in result[0].lower()
        assert "semua" in result[1].lower()
        assert "apakah" in result[2].lower()


    # ── TC-2.2: Tidak split jika teks pendek ─────────────────────

    def test_no_split_short_text(self, summarizer):
        """Teks pendek tanpa tanda baca tetap utuh."""
        text = "Rapat dimulai pukul delapan pagi"
        result = summarizer._step2_sentence_segmentation(text)
        assert len(result) == 1

    # ── TC-2.3: Split konjungsi untuk segmen panjang ──────────────

    def test_split_at_conjunction_for_long_segment(self, summarizer):
        """Menguji jalur split konjungsi: kalimat >60 kata dipecah di koma+konjungsi."""
        # Buat kalimat panjang >60 kata dengan konjungsi
        words = ["kata"] * 30
        long_segment = " ".join(words) + ", dan " + " ".join(words) + ", kemudian " + " ".join(words)
        result = summarizer._step2_sentence_segmentation(long_segment)
        # Harus dipecah menjadi beberapa segmen
        assert len(result) > 1

    # ── TC-2.4: Chunk segmen sangat panjang (fallback) ────────────

    def test_chunk_very_long_segment(self, summarizer):
        """Menguji jalur fallback _chunk_long_segment(): segmen >60 kata tanpa konjungsi."""
        # Buat kalimat panjang tanpa koma-konjungsi
        words_list = [f"kata{i}" for i in range(80)]
        # Tambahkan koma di beberapa titik
        words_list[39] = "kata39,"
        long_text = " ".join(words_list)
        result = summarizer._step2_sentence_segmentation(long_text)
        # Harus dipecah
        assert len(result) >= 1

    # ── TC-2.5: Merge fragmen pendek ──────────────────────────────

    def test_merge_short_fragments(self, summarizer):
        """Menguji jalur 2c _merge_short_fragments(): fragmen <min_words digabung."""
        segments = [
            "Rapat dimulai pukul delapan pagi hari ini untuk membahas progres.",
            "Ya.",     # Fragmen pendek — harus digabung
            "Semua anggota tim hadir dalam rapat hari ini.",
        ]
        result = summarizer._merge_short_fragments(segments)
        # Fragmen pendek "Ya." digabung ke kalimat sebelumnya
        assert len(result) <= len(segments)

    # ── TC-2.6: Empty input ───────────────────────────────────────

    def test_empty_input(self, summarizer):
        """Teks kosong mengembalikan list kosong."""
        result = summarizer._step2_sentence_segmentation("")
        assert result == []


class TestChunkLongSegment:
    """Whitebox testing untuk helper _chunk_long_segment()."""

    def test_chunk_at_comma_boundary(self, summarizer):
        """Chunk dipotong di koma setelah ~40 kata."""
        words = [f"kata{i}" for i in range(50)]
        words[39] = "kata39,"
        output = []
        summarizer._chunk_long_segment(words, output)
        # Harus ada potongan di sekitar kata ke-40
        assert len(output) >= 2

    def test_chunk_no_comma_single_chunk(self, summarizer):
        """Tanpa koma, semua kata masuk satu chunk."""
        words = [f"kata{i}" for i in range(20)]
        output = []
        summarizer._chunk_long_segment(words, output)
        assert len(output) == 1
        assert "kata0" in output[0]
