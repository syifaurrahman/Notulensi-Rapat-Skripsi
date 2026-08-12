"""
test_ollama_rewriter.py — Whitebox Test: OllamaRewriter
=========================================================
Menguji semua jalur internal OllamaRewriter.

Teknik whitebox:
  - Branch Coverage: is_available(), rewrite(), _build_prompt(), _clean_response()
  - Path Coverage: context pendek/panjang, chunking
"""

import pytest
from unittest.mock import patch, MagicMock


class TestOllamaRewriterInit:
    """Whitebox testing untuk inisialisasi OllamaRewriter."""

    def test_default_config(self):
        """OllamaRewriter dengan config default."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        assert rewriter.cfg is not None
        assert rewriter.cfg.ollama_base_url == "http://localhost:11434"

    def test_custom_config(self, summary_config):
        """OllamaRewriter dengan config kustom."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter(summary_config)
        assert rewriter.cfg == summary_config


class TestIsAvailable:
    """Whitebox testing untuk is_available()."""

    def test_server_available(self):
        """Menguji jalur: server tersedia → return True."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch('urllib.request.urlopen', return_value=mock_response):
            assert rewriter.is_available() is True

    def test_server_unavailable(self):
        """Menguji jalur: server tidak tersedia → return False."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        with patch('urllib.request.urlopen', side_effect=Exception("Connection refused")):
            assert rewriter.is_available() is False


class TestBuildPrompt:
    """Whitebox testing untuk _build_prompt()."""

    def test_prompt_without_context(self):
        """Menguji jalur: tanpa context → prompt tanpa section context."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        sentences = ["Rapat membahas keselamatan kerja.", "Semua karyawan wajib menggunakan APD."]
        prompt = rewriter._build_prompt(sentences)
        assert "Rapat membahas keselamatan" in prompt
        assert "POIN-POIN KUNCI" in prompt

    def test_prompt_with_short_context(self):
        """Menguji jalur: context pendek (<4000 chars) → context penuh dimasukkan."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        sentences = ["Poin kunci satu.", "Poin kunci dua."]
        context = "Ini adalah transkrip pendek yang kurang dari 4000 karakter."
        prompt = rewriter._build_prompt(sentences, context)
        assert "TRANSKRIP LENGKAP RAPAT" in prompt
        assert context in prompt

    def test_prompt_with_long_context(self):
        """Menguji jalur: context panjang (>4000 chars) → di-chunk ke awal, tengah, akhir."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        sentences = ["Poin kunci."]
        context = "x" * 5000  # Lebih dari 4000 karakter
        prompt = rewriter._build_prompt(sentences, context)
        assert "Bagian awal" in prompt
        assert "Bagian tengah" in prompt
        assert "Bagian akhir" in prompt


class TestCleanResponse:
    """Whitebox testing untuk _clean_response()."""

    def test_preserve_heading_format(self):
        """Menguji jalur: baris **Judul:** dipertahankan."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        text = "**Pembukaan:**\n- Poin satu\n- Poin dua"
        result = rewriter._clean_response(text)
        assert "**Pembukaan:**" in result

    def test_remove_bold_in_body(self):
        """Menguji jalur: bold dalam kalimat biasa dihapus."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        text = "- Ini **teks bold** dalam kalimat biasa"
        result = rewriter._clean_response(text)
        assert "**" not in result
        assert "teks bold" in result

    def test_remove_generic_intro(self):
        """Menguji jalur: pengantar generik di awal dihapus."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        text = "Berikut ringkasan rapat:\n**Pembukaan:**\n- Rapat dimulai"
        result = rewriter._clean_response(text)
        # Pengantar generik dihapus
        assert not result.lower().startswith("berikut")

    def test_remove_markdown_headings(self):
        """Menguji jalur: heading ## dihapus."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        text = "## Pembukaan\n- Poin satu"
        result = rewriter._clean_response(text)
        assert "##" not in result

    def test_remove_html_tags(self):
        """Menguji jalur: tag HTML dihapus."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        text = "<b>Pembukaan</b>: rapat dimulai <br/> pukul 8"
        result = rewriter._clean_response(text)
        assert "<b>" not in result
        assert "<br/>" not in result

    def test_normalize_excessive_newlines(self):
        """Menguji jalur: newline >2 dinormalisasi."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        text = "Paragraf satu\n\n\n\n\nParagraf dua"
        result = rewriter._clean_response(text)
        assert "\n\n\n" not in result


class TestRewrite:
    """Whitebox testing untuk rewrite()."""

    def test_rewrite_empty_input(self):
        """Menguji jalur: input kosong → string kosong."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        result = rewriter.rewrite([])
        assert result == ""

    def test_rewrite_with_ollama_failure(self):
        """Menguji jalur: Ollama error → return string kosong."""
        from summarize.ollama_rewriter import OllamaRewriter
        rewriter = OllamaRewriter()
        with patch.object(rewriter, '_call_ollama', side_effect=Exception("Server error")):
            result = rewriter.rewrite(["Poin kunci rapat."])
            assert result == ""
