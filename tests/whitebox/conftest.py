"""
conftest.py — Shared fixtures untuk Whitebox Testing Notulensi Rapat
====================================================================
Menyediakan fixtures yang digunakan oleh seluruh test module.
"""

import sys
import os
import pytest

# ── Path Setup ──────────────────────────────────────────────────────────
# Tambahkan path proyek agar bisa import modul aplikasi
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
WHISPER_DIR = os.path.join(PROJECT_ROOT, 'whispertranscription')
LIVE_DIR = os.path.join(WHISPER_DIR, 'whisperLiveTranscription')

# Insert path untuk import
for p in [PROJECT_ROOT, WHISPER_DIR, LIVE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Mock torch jika tidak ter-install di virtual environment
try:
    import torch
except ImportError:
    from unittest.mock import MagicMock
    mock_torch = MagicMock()
    mock_torch.cuda.is_available.return_value = False
    sys.modules['torch'] = mock_torch



# ══════════════════════════════════════════════════════════════════════
# Fixtures — SummaryConfig
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture
def summary_config():
    """SummaryConfig default untuk testing."""
    from summarize.config import SummaryConfig
    return SummaryConfig()


@pytest.fixture
def custom_summary_config():
    """SummaryConfig dengan parameter kustom."""
    from summarize.config import SummaryConfig
    return SummaryConfig(
        compression_ratio=0.30,
        min_sentences=5,
        max_sentences=15,
        similarity_threshold=0.10,
        min_words_per_sentence=5,
        dedup_threshold=0.70,
    )


# ══════════════════════════════════════════════════════════════════════
# Fixtures — LexRankSummarizer
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture
def summarizer(summary_config):
    """Instance LexRankSummarizer dengan config default."""
    from summarize.lexrank import LexRankSummarizer
    return LexRankSummarizer(summary_config)


@pytest.fixture
def summarizer_custom(custom_summary_config):
    """Instance LexRankSummarizer dengan config kustom."""
    from summarize.lexrank import LexRankSummarizer
    return LexRankSummarizer(custom_summary_config)


# ══════════════════════════════════════════════════════════════════════
# Fixtures — Sample Texts
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture
def sample_whisper_text():
    """Teks transkripsi Whisper tipikal dengan filler dan noise."""
    return (
        "Nah jadi gini ya, hari ini kita membahas tentang keselamatan kerja di lingkungan kantor. "
        "Eee yang pertama adalah penggunaan alat pelindung diri atau APD. "
        "Jadi ya kan semua karyawan wajib menggunakan helm safety saat memasuki area konstruksi. "
        "Terima kasih telah menonton. "
        "Oke nah kemudian kita juga harus memperhatikan jalur evakuasi di gedung ini. "
        "Jadi ada tiga pintu darurat yang bisa digunakan saat terjadi kebakaran. "
        "Terus kita juga perlu melakukan pengecekan alat pemadam kebakaran secara berkala. "
        "[music] "
        "Selain itu pelatihan P3K juga sangat penting untuk semua karyawan. "
        "Baik ya jadi kesimpulannya keselamatan kerja adalah tanggung jawab bersama. "
        "Recording in progress. "
        "Kita semua harus berkomitmen untuk menjaga keselamatan di tempat kerja."
    )


@pytest.fixture
def sample_clean_sentences():
    """Kalimat bersih (sudah diproses) untuk testing step 3-6."""
    return [
        "Hari ini kita membahas tentang keselamatan kerja di lingkungan kantor.",
        "Yang pertama adalah penggunaan alat pelindung diri atau APD.",
        "Semua karyawan wajib menggunakan helm safety saat memasuki area konstruksi.",
        "Kita juga harus memperhatikan jalur evakuasi di gedung ini.",
        "Ada tiga pintu darurat yang bisa digunakan saat terjadi kebakaran.",
        "Kita juga perlu melakukan pengecekan alat pemadam kebakaran secara berkala.",
        "Selain itu pelatihan P3K juga sangat penting untuk semua karyawan.",
        "Kesimpulannya keselamatan kerja adalah tanggung jawab bersama.",
        "Kita semua harus berkomitmen untuk menjaga keselamatan di tempat kerja.",
    ]


@pytest.fixture
def sample_short_text():
    """Teks terlalu pendek untuk diringkas."""
    return "Halo."


@pytest.fixture
def sample_empty_text():
    """Teks kosong."""
    return ""


@pytest.fixture
def sample_long_text():
    """Teks panjang realistis untuk end-to-end test."""
    paragraphs = [
        "Selamat pagi semuanya, kita mulai rapat hari ini tentang proyek pengembangan sistem informasi.",
        "Nah jadi gini ya, proyek ini sudah berjalan selama tiga bulan dan kita perlu mengevaluasi progres saat ini.",
        "Eee tim developer sudah menyelesaikan modul login dan dashboard, dan sekarang sedang mengerjakan modul laporan.",
        "Untuk backend kita menggunakan framework Laravel dengan database MySQL yang di-deploy di server lokal.",
        "Kita juga sudah mengimplementasikan fitur autentikasi menggunakan JWT token untuk keamanan API.",
        "Oke kemudian untuk frontend kita menggunakan React dengan state management Redux untuk mengelola data.",
        "Tim QA sudah melakukan pengujian unit testing dan integration testing pada modul yang sudah selesai.",
        "Jadi hasil pengujian menunjukkan bahwa 95 persen test case berhasil passed tanpa error yang signifikan.",
        "Nah ada beberapa bug minor yang ditemukan di bagian validasi form dan sudah diperbaiki minggu lalu.",
        "Terus untuk deployment kita akan menggunakan Docker container agar lebih mudah dalam scaling.",
        "Selain itu kita juga sudah menyiapkan CI/CD pipeline menggunakan GitHub Actions untuk otomatisasi build.",
        "Tim desain sudah menyelesaikan mockup untuk halaman laporan dan sedang menunggu feedback dari stakeholder.",
        "Baik jadi untuk timeline selanjutnya, minggu depan kita harus menyelesaikan modul manajemen pengguna.",
        "Terima kasih telah menonton.",
        "Kemudian sprint berikutnya akan fokus pada integrasi payment gateway dan notifikasi email.",
        "Ada pertanyaan dari tim marketing tentang fitur export data ke format Excel dan PDF.",
        "Kita akan menambahkan fitur tersebut di sprint ketiga bersamaan dengan optimasi performa database.",
        "Recording in progress.",
        "Kesimpulannya proyek berjalan sesuai jadwal dan kita perlu menjaga momentum ini.",
        "Baik sekali, terima kasih semuanya, rapat kita hari ini cukup sampai di sini.",
    ]
    return " ".join(paragraphs)


# ══════════════════════════════════════════════════════════════════════
# Fixtures — Hallucination Filter Config
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture
def halluc_config():
    """Config mock untuk HallucinationFilter."""
    from whisperLiveTranscription.config import Config
    return Config(
        model_size="tiny",
        language="id",
        use_autocorrect=False,
    )
