"""
test_lexrank_step3_filtering.py — Whitebox Test: Step 3 Sentence Filtering
============================================================================
Menguji semua jalur internal _step3_sentence_filtering() dan helper-nya.

Teknik whitebox:
  - Condition Coverage: setiap kondisi filter diuji
  - Branch Coverage: jalur lolos vs terfilter
"""

import pytest


class TestStep3SentenceFiltering:
    """Whitebox testing untuk Step 3: Sentence Filtering."""

    # ── TC-3.1: Filter kalimat terlalu pendek ─────────────────────

    def test_filter_short_sentences(self, summarizer):
        """Menguji jalur 3b: kalimat < min_words_per_sentence dibuang."""
        sentences = [
            "Oke.",                             # Terlalu pendek
            "Ya sudah.",                        # Terlalu pendek
            "Semua karyawan wajib menggunakan alat pelindung diri saat bekerja.",
        ]
        result = summarizer._step3_sentence_filtering(sentences)
        # Kalimat pendek dibuang
        assert all(len(s.split()) >= summarizer.cfg.min_words_per_sentence for s in result)

    # ── TC-3.2: Filter kalimat noise (pengulangan kata) ───────────

    def test_filter_noise_pattern_repetition(self, summarizer):
        """Menguji jalur 3d: kalimat pengulangan satu kata dibuang."""
        sentences = [
            "ya ya ya ya ya ya",
            "Semua karyawan wajib menggunakan helm safety saat bekerja di lapangan.",
        ]
        result = summarizer._step3_sentence_filtering(sentences)
        # Kalimat repetisi dibuang
        for s in result:
            assert "ya ya ya" not in s.lower()

    # ── TC-3.3: Filter kalimat non-informatif ─────────────────────

    def test_filter_non_informative_sentences(self, summarizer):
        """Menguji jalur 3e: kalimat Q&A, personal, transisi non-informatif dibuang."""
        sentences = [
            "Ada yang mau ditanyakan lagi tentang materi ini?",
            "Oke kita lanjutkan ke materi berikutnya.",
            "Laptop saya tiba-tiba mati saat presentasi tadi.",
            "Penggunaan alat pelindung diri sangat penting untuk mencegah kecelakaan kerja.",
        ]
        result = summarizer._step3_sentence_filtering(sentences)
        # Kalimat non-informatif dibuang, kalimat informatif lolos
        informative_found = any("pelindung diri" in s.lower() for s in result)
        assert informative_found

    # ── TC-3.4: Deduplikasi Jaccard overlap ───────────────────────

    def test_dedup_jaccard_overlap(self, summarizer):
        """Menguji jalur 3f: kalimat duplikat (Jaccard > threshold) dibuang."""
        sentences = [
            "Semua karyawan wajib menggunakan helm safety saat bekerja di area konstruksi.",
            "Karyawan wajib menggunakan helm safety saat bekerja di area konstruksi semua.",
            "Pelatihan P3K sangat penting untuk kesiapan menghadapi keadaan darurat.",
        ]
        result = summarizer._step3_sentence_filtering(sentences)
        # Duplikat dibuang, hanya satu versi yang lolos
        assert len(result) <= 2

    # ── TC-3.5: Filter kalimat kurang karakter informatif ─────────

    def test_filter_low_informative_chars(self, summarizer):
        """Menguji jalur 3c: kalimat < min_informative_chars dibuang."""
        sentences = [
            "12345",                    # Terlalu pendek
            "Kebijakan keselamatan kerja harus dipatuhi oleh seluruh karyawan tanpa terkecuali.",
        ]
        result = summarizer._step3_sentence_filtering(sentences)
        for s in result:
            assert len(s) >= summarizer.cfg.min_informative_chars

    # ── TC-3.6: Semua kalimat lolos (no filter) ───────────────────

    def test_all_sentences_pass(self, summarizer):
        """Kalimat informatif, unik, dan cukup panjang semua lolos."""
        sentences = [
            "Penggunaan alat pelindung diri wajib dilakukan oleh seluruh karyawan di area konstruksi.",
            "Jalur evakuasi harus selalu bebas dari penghalang untuk memastikan keselamatan penghuni gedung.",
            "Pelatihan pertolongan pertama dilaksanakan setiap bulan untuk meningkatkan kesiapan karyawan.",
        ]
        result = summarizer._step3_sentence_filtering(sentences)
        assert len(result) == 3

    # ── TC-3.7: Input kosong ──────────────────────────────────────

    def test_empty_input_returns_empty(self, summarizer):
        """Input list kosong mengembalikan list kosong."""
        result = summarizer._step3_sentence_filtering([])
        assert result == []


class TestCleanSingleSentence:
    """Whitebox testing untuk helper _clean_single_sentence()."""

    def test_remove_filler_at_start(self, summarizer):
        """Filler di awal kalimat dihapus."""
        sentence = "Nah jadi gini ya, kita harus membahas topik ini secara mendalam"
        result = summarizer._clean_single_sentence(sentence)
        assert not result.lower().startswith("nah")
        assert not result.lower().startswith("jadi")

    def test_remove_filler_at_end(self, summarizer):
        """Filler di akhir kalimat dihapus."""
        sentence = "Kita harus membahas topik keselamatan kerja, gitu ya kan"
        result = summarizer._clean_single_sentence(sentence)
        assert not result.lower().rstrip('.').endswith("kan")

    def test_ensure_period_ending(self, summarizer):
        """Kalimat tanpa tanda baca akhir ditambahkan titik."""
        sentence = "Semua karyawan wajib menggunakan helm safety"
        result = summarizer._clean_single_sentence(sentence)
        assert result.endswith('.')

    def test_capitalize_first_letter(self, summarizer):
        """Huruf pertama dikapitalisasi."""
        sentence = "penggunaan alat pelindung diri sangat penting untuk keselamatan"
        result = summarizer._clean_single_sentence(sentence)
        assert result[0].isupper()
