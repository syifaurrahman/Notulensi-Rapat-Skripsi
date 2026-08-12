"""
test_lexrank_step4_extraction.py — Whitebox Test: Step 4 Key Point Extraction
===============================================================================
Menguji semua jalur internal _step4_lexrank_extraction() dan helper-nya.

Teknik whitebox:
  - Path Coverage: TF-IDF berhasil vs fallback
  - Branch Coverage: matrix None, target > len(sentences)
  - Boundary Testing: ukuran input minimal
"""

import numpy as np
import pytest


class TestStep4LexRankExtraction:
    """Whitebox testing untuk Step 4: Key Point Extraction (LexRank)."""

    # ── TC-4.1: Ekstraksi normal ──────────────────────────────────

    def test_normal_extraction(self, summarizer, sample_clean_sentences):
        """Menguji jalur normal: TF-IDF berhasil → LexRank scoring → top-N."""
        target = 3
        top_sentences, top_indices = summarizer._step4_lexrank_extraction(
            sample_clean_sentences, target=target
        )
        assert len(top_sentences) == target
        assert len(top_indices) == target
        # Indeks harus valid
        for idx in top_indices:
            assert 0 <= idx < len(sample_clean_sentences)
        # Indeks harus terurut (ascending — diurutkan sesuai posisi asli)
        assert top_indices == sorted(top_indices)

    # ── TC-4.2: Target lebih besar dari jumlah kalimat ────────────

    def test_target_exceeds_sentence_count(self, summarizer):
        """Menguji boundary: target > len(sentences) → ambil semua."""
        sentences = [
            "Penggunaan alat pelindung diri wajib untuk semua pekerja di area konstruksi.",
            "Pelatihan keselamatan kerja dilaksanakan secara rutin setiap bulan.",
        ]
        top_sentences, top_indices = summarizer._step4_lexrank_extraction(sentences, target=10)
        assert len(top_sentences) <= len(sentences)

    # ── TC-4.3: Input minimal (2 kalimat) ─────────────────────────

    def test_minimal_input(self, summarizer):
        """Menguji boundary: hanya 2 kalimat, target=1."""
        sentences = [
            "Keselamatan kerja merupakan prioritas utama perusahaan dalam operasional sehari-hari.",
            "Semua insiden harus dilaporkan kepada supervisor dalam waktu dua puluh empat jam.",
        ]
        top_sentences, top_indices = summarizer._step4_lexrank_extraction(sentences, target=1)
        assert len(top_sentences) == 1
        assert top_sentences[0] in sentences

    # ── TC-4.4: TF-IDF fallback (kalimat identik) ────────────────

    def test_tfidf_fallback_identical_sentences(self, summarizer):
        """Menguji jalur fallback: semua kalimat identik → TF-IDF mungkin gagal."""
        sentences = [
            "Tes kalimat yang sama persis untuk semua baris.",
            "Tes kalimat yang sama persis untuk semua baris.",
            "Tes kalimat yang sama persis untuk semua baris.",
        ]
        # Tidak boleh error
        top_sentences, top_indices = summarizer._step4_lexrank_extraction(sentences, target=2)
        assert len(top_sentences) <= 2


class TestBuildTfidfMatrix:
    """Whitebox testing untuk helper _build_tfidf_matrix()."""

    def test_successful_tfidf_build(self, summarizer, sample_clean_sentences):
        """TF-IDF matrix berhasil dibangun dari kalimat valid."""
        matrix = summarizer._build_tfidf_matrix(sample_clean_sentences)
        assert matrix is not None
        assert matrix.shape[0] == len(sample_clean_sentences)

    def test_single_sentence_tfidf(self, summarizer):
        """TF-IDF dengan 1 kalimat tetap berhasil."""
        sentences = ["Penggunaan alat pelindung diri sangat penting untuk mencegah kecelakaan kerja."]
        matrix = summarizer._build_tfidf_matrix(sentences)
        # Mungkin berhasil atau None (tergantung min_df), keduanya valid
        if matrix is not None:
            assert matrix.shape[0] == 1


class TestBuildSimilarityMatrix:
    """Whitebox testing untuk _build_similarity_matrix()."""

    def test_similarity_matrix_shape(self, summarizer, sample_clean_sentences):
        """Matrix similarity harus N×N dan row-stochastic."""
        tfidf = summarizer._build_tfidf_matrix(sample_clean_sentences)
        if tfidf is not None:
            sim = summarizer._build_similarity_matrix(tfidf)
            n = len(sample_clean_sentences)
            assert sim.shape == (n, n)
            # Diagonal harus 0
            for i in range(n):
                assert sim[i, i] == 0.0


class TestPowerIteration:
    """Whitebox testing untuk _power_iteration()."""

    def test_power_iteration_convergence(self, summarizer, sample_clean_sentences):
        """Power iteration harus konvergen dan menghasilkan skor valid."""
        tfidf = summarizer._build_tfidf_matrix(sample_clean_sentences)
        if tfidf is not None:
            sim = summarizer._build_similarity_matrix(tfidf)
            scores = summarizer._power_iteration(sim)
            assert len(scores) == len(sample_clean_sentences)
            assert all(s >= 0 for s in scores)
            # Skor tidak boleh semua nol
            assert sum(scores) > 0

    def test_power_iteration_uniform_input(self, summarizer):
        """Matrix uniform → skor seragam."""
        n = 5
        sim = np.ones((n, n)) / n
        np.fill_diagonal(sim, 0.0)
        row_sums = sim.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        sim = sim / row_sums
        scores = summarizer._power_iteration(sim)
        assert len(scores) == n
        # Skor harus hampir seragam
        assert max(scores) - min(scores) < 0.1
