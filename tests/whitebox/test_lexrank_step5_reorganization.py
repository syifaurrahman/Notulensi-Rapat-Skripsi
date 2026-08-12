"""
test_lexrank_step5_reorganization.py — Whitebox Test: Step 5 Reorganization
=============================================================================
Menguji semua jalur internal _step5_reorganize().

Teknik whitebox:
  - Branch Coverage: len <= 3, grouping ke pembukaan/isi/penutup
  - Path Coverage: berbagai distribusi indeks
"""

import pytest


class TestStep5Reorganization:
    """Whitebox testing untuk Step 5: Reorganization."""

    # ── TC-5.1: Input <= 3 kalimat (jalur shortcut) ───────────────

    def test_shortcut_three_or_less_sentences(self, summarizer):
        """Menguji jalur shortcut: <= 3 kalimat dikembalikan langsung tanpa reorganisasi."""
        sentences = [
            "Kalimat pembukaan rapat hari ini tentang keselamatan.",
            "Kalimat isi tentang penggunaan APD di lapangan.",
            "Kalimat penutup tentang komitmen bersama.",
        ]
        indices = [0, 5, 10]
        total = 15
        result = summarizer._step5_reorganize(sentences, indices, total)
        assert result == sentences  # Tidak berubah

    # ── TC-5.2: Distribusi merata ke tiga zona ────────────────────

    def test_even_distribution_three_zones(self, summarizer):
        """Menguji jalur normal: kalimat terdistribusi ke pembukaan, isi, penutup."""
        sentences = [
            "Rapat dimulai dengan pembahasan agenda hari ini yang sangat penting.",
            "Topik pertama adalah evaluasi kinerja tim selama semester ini.",
            "Topik kedua tentang rencana strategis perusahaan tahun depan.",
            "Diskusi tentang alokasi anggaran untuk proyek baru.",
            "Kesimpulan rapat bahwa semua target harus tercapai tepat waktu.",
        ]
        # Total 15 kalimat, third = 5
        # Indeks: 1 (opening), 6 (body), 8 (body), 11 (closing), 14 (closing)
        indices = [1, 6, 8, 11, 14]
        total = 15
        result = summarizer._step5_reorganize(sentences, indices, total)
        # Harus ada 5 kalimat, diurutkan: opening → body → closing
        assert len(result) == 5

    # ── TC-5.3: Semua kalimat dari zona awal ──────────────────────

    def test_all_from_opening_zone(self, summarizer):
        """Menguji jalur: semua kalimat terpilih dari 1/3 awal."""
        sentences = [
            "Kalimat pertama tentang pembukaan acara oleh moderator.",
            "Kalimat kedua tentang perkenalan peserta rapat.",
            "Kalimat ketiga tentang agenda pembahasan utama.",
            "Kalimat keempat tentang latar belakang masalah.",
        ]
        indices = [0, 1, 2, 3]
        total = 15
        result = summarizer._step5_reorganize(sentences, indices, total)
        # Semua masuk opening, body dan closing kosong
        assert len(result) == 4

    # ── TC-5.4: Semua kalimat dari zona akhir ─────────────────────

    def test_all_from_closing_zone(self, summarizer):
        """Menguji jalur: semua kalimat terpilih dari 1/3 akhir."""
        sentences = [
            "Kalimat kesimpulan pertama tentang hasil evaluasi kinerja.",
            "Kalimat kesimpulan kedua tentang rencana tindak lanjut.",
            "Kalimat penutup rapat tentang jadwal pertemuan berikutnya.",
            "Kalimat terakhir ucapan terima kasih dari ketua rapat.",
        ]
        indices = [12, 13, 14, 15]
        total = 15
        result = summarizer._step5_reorganize(sentences, indices, total)
        assert len(result) == 4
