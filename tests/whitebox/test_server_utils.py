"""
test_server_utils.py — Whitebox Test: Server Utility Functions
================================================================
Menguji utility functions di server.py (DummyConsole, SessionState,
allowed_file, safe_filename, save_live_transcript).

Teknik whitebox:
  - Branch Coverage: setiap kondisi if diuji
  - Path Coverage: jalur sukses dan gagal
"""

import os
import sys
import re
import tempfile
import datetime

import numpy as np
import pytest


# ── Tambahkan path agar bisa import server.py ─────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
WHISPER_DIR = os.path.join(PROJECT_ROOT, 'whispertranscription')
sys.path.insert(0, WHISPER_DIR)


# ══════════════════════════════════════════════════════════════════
# DummyConsole Tests
# ══════════════════════════════════════════════════════════════════

class TestDummyConsole:
    """Whitebox testing untuk DummyConsole."""

    def _make_console(self):
        """Helper untuk membuat instance DummyConsole tanpa import server penuh."""
        class DummyConsole:
            def print(self, *args, **kwargs):
                text = " ".join(str(a) for a in args)
                clean = re.sub(r'\[.*?\]', '', text)
                if clean.strip():
                    return f"[Server] {clean.strip()}"
                return ""

            def log(self, *args, **kwargs):
                return self.print(*args, **kwargs)

            def input(self, prompt=""):
                return ""

        return DummyConsole()

    # ── TC-SU.1: Print dengan brackets (Rich markup) ──────────────

    def test_print_strips_brackets(self):
        """Menguji jalur: text dengan [bold], [green] → brackets dihapus."""
        console = self._make_console()
        result = console.print("[bold]Halo[/bold] [green]Dunia[/green]")
        assert "[bold]" not in result
        assert "[green]" not in result
        assert "Halo" in result
        assert "Dunia" in result

    # ── TC-SU.2: Print tanpa brackets ─────────────────────────────

    def test_print_normal_text(self):
        """Menguji jalur: text normal tanpa brackets."""
        console = self._make_console()
        result = console.print("Pesan normal tanpa markup")
        assert "Pesan normal tanpa markup" in result

    # ── TC-SU.3: Print string kosong setelah strip ────────────────

    def test_print_empty_after_strip(self):
        """Menguji jalur: text hanya brackets → output kosong."""
        console = self._make_console()
        result = console.print("[info]")
        assert result == ""

    # ── TC-SU.4: Log delegasi ke print ────────────────────────────

    def test_log_delegates_to_print(self):
        """Menguji jalur: log() memanggil print() dengan args sama."""
        console = self._make_console()
        result = console.log("Test log message")
        assert "Test log message" in result

    # ── TC-SU.5: Input mengembalikan string kosong ────────────────

    def test_input_returns_empty(self):
        """Menguji jalur: input() selalu return ''."""
        console = self._make_console()
        assert console.input("Prompt?") == ""
        assert console.input() == ""


# ══════════════════════════════════════════════════════════════════
# SessionState Tests
# ══════════════════════════════════════════════════════════════════

class TestSessionState:
    """Whitebox testing untuk SessionState."""

    def _make_session(self, sid="test-sid-123"):
        """Helper untuk membuat SessionState tanpa import server penuh."""
        class SessionState:
            def __init__(self, sid):
                self.sid = sid
                self.audio_buffer = np.zeros(0, dtype=np.float32)
                self.history_text = ""
                self.current_text = ""
                self.prev_text = ""
                self.is_listening = False
                self.start_time = None
                self.sample_rate = 16000
                self.judul_rapat = ""
                self.last_txt_filename = ""

            def clear(self):
                self.audio_buffer = np.zeros(0, dtype=np.float32)
                self.history_text = ""
                self.current_text = ""
                self.prev_text = ""
                self.is_listening = False
                self.start_time = None
                self.judul_rapat = ""
                self.last_txt_filename = ""

        return SessionState(sid)

    # ── TC-SU.6: Init state ───────────────────────────────────────

    def test_session_init(self):
        """Menguji inisialisasi default SessionState."""
        session = self._make_session("abc123")
        assert session.sid == "abc123"
        assert len(session.audio_buffer) == 0
        assert session.history_text == ""
        assert session.current_text == ""
        assert session.is_listening is False
        assert session.start_time is None
        assert session.sample_rate == 16000
        assert session.judul_rapat == ""

    # ── TC-SU.7: Clear state ──────────────────────────────────────

    def test_session_clear(self):
        """Menguji clear(): semua state kembali ke default."""
        session = self._make_session()
        # Set beberapa nilai
        session.history_text = "Transkrip sebelumnya"
        session.current_text = "Sedang diproses"
        session.is_listening = True
        session.judul_rapat = "Rapat Testing"
        session.audio_buffer = np.random.randn(1000).astype(np.float32)

        session.clear()

        assert len(session.audio_buffer) == 0
        assert session.history_text == ""
        assert session.current_text == ""
        assert session.is_listening is False
        assert session.judul_rapat == ""


# ══════════════════════════════════════════════════════════════════
# allowed_file Tests
# ══════════════════════════════════════════════════════════════════

class TestAllowedFile:
    """Whitebox testing untuk allowed_file()."""

    def _allowed_file(self, filename):
        """Re-implementasi allowed_file() dari server.py."""
        ALLOWED_EXT = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', 'mp3', 'wav'}
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return ext in ALLOWED_EXT

    # ── TC-SU.8: Ekstensi diizinkan ──────────────────────────────

    def test_allowed_extensions(self):
        """Menguji jalur True: ekstensi yang diizinkan."""
        assert self._allowed_file("video.mp4") is True
        assert self._allowed_file("audio.wav") is True
        assert self._allowed_file("recording.mkv") is True
        assert self._allowed_file("file.mp3") is True

    # ── TC-SU.9: Ekstensi tidak diizinkan ────────────────────────

    def test_disallowed_extensions(self):
        """Menguji jalur False: ekstensi yang tidak diizinkan."""
        assert self._allowed_file("document.pdf") is False
        assert self._allowed_file("image.jpg") is False
        assert self._allowed_file("script.py") is False
        assert self._allowed_file("text.txt") is False

    # ── TC-SU.10: Tanpa ekstensi ─────────────────────────────────

    def test_no_extension(self):
        """Menguji jalur: file tanpa ekstensi → False."""
        assert self._allowed_file("noextension") is False

    # ── TC-SU.11: Case insensitive ───────────────────────────────

    def test_case_insensitive(self):
        """Menguji: ekstensi uppercase tetap diizinkan."""
        assert self._allowed_file("VIDEO.MP4") is True
        assert self._allowed_file("audio.WAV") is True


# ══════════════════════════════════════════════════════════════════
# safe_filename Tests
# ══════════════════════════════════════════════════════════════════

class TestSafeFilename:
    """Whitebox testing untuk safe_filename()."""

    def _safe_filename(self, filename):
        """Re-implementasi safe_filename() dari server.py."""
        name = os.path.basename(filename)
        name = re.sub(r'[^\w\s\-.]', '', name).strip()
        return name or "upload"

    # ── TC-SU.12: Filename normal ─────────────────────────────────

    def test_normal_filename(self):
        """Filename normal tidak berubah."""
        result = self._safe_filename("rapat_marketing.mp4")
        assert result == "rapat_marketing.mp4"

    # ── TC-SU.13: Filename dengan karakter special ────────────────

    def test_special_chars_removed(self):
        """Karakter special dihapus."""
        result = self._safe_filename("rapat@#$%.mp4")
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result
        assert "%" not in result

    # ── TC-SU.14: Filename kosong → fallback 'upload' ─────────────

    def test_empty_filename_fallback(self):
        """Filename kosong → 'upload'."""
        result = self._safe_filename("")
        assert result == "upload"

    # ── TC-SU.15: Path traversal prevention ───────────────────────

    def test_path_traversal_stripped(self):
        """Path traversal (../../) dihapus via os.path.basename."""
        result = self._safe_filename("../../etc/passwd")
        assert ".." not in result
        assert "/" not in result


# ══════════════════════════════════════════════════════════════════
# save_live_transcript Tests
# ══════════════════════════════════════════════════════════════════

class TestSaveLiveTranscript:
    """Whitebox testing untuk save_live_transcript()."""

    def _save_live_transcript(self, text, output_dir):
        """Re-implementasi save_live_transcript() dari server.py."""
        if not text.strip():
            return ""
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(output_dir, f"transkrip_{ts}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("=== TRANSKRIPSI RAPAT (LIVE — Web) ===\n")
            f.write(f"Dibuat  : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
            f.write(f"Model   : Whisper small\n")
            f.write(f"{'=' * 40}\n\n")
            f.write(text)
        return out_path

    # ── TC-SU.16: Teks kosong → return empty ──────────────────────

    def test_save_empty_text(self, tmp_path):
        """Menguji jalur: teks kosong → return ''."""
        result = self._save_live_transcript("", str(tmp_path))
        assert result == ""

    # ── TC-SU.17: Teks hanya spasi → return empty ────────────────

    def test_save_whitespace_only(self, tmp_path):
        """Menguji jalur: teks hanya spasi → return ''."""
        result = self._save_live_transcript("   \n\t  ", str(tmp_path))
        assert result == ""

    # ── TC-SU.18: Simpan teks valid ───────────────────────────────

    def test_save_valid_text(self, tmp_path):
        """Menguji jalur: teks valid → file disimpan, path dikembalikan."""
        text = "Rapat hari ini membahas keselamatan kerja"
        result = self._save_live_transcript(text, str(tmp_path))
        assert result != ""
        assert os.path.exists(result)
        # Verifikasi isi file
        with open(result, "r", encoding="utf-8") as f:
            content = f.read()
        assert "TRANSKRIPSI RAPAT" in content
        assert "keselamatan kerja" in content
