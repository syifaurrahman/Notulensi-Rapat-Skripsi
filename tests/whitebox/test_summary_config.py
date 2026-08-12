"""
test_summary_config.py — Whitebox Test: SummaryConfig
=======================================================
Menguji konfigurasi default dan kustom SummaryConfig.

Teknik whitebox:
  - Statement Coverage: semua field diakses
"""

import pytest


class TestSummaryConfig:
    """Whitebox testing untuk SummaryConfig dataclass."""

    # ── TC-CFG.1: Default values ──────────────────────────────────

    def test_default_values(self, summary_config):
        """Semua field memiliki nilai default yang benar."""
        assert summary_config.compression_ratio == 0.25
        assert summary_config.min_sentences == 8
        assert summary_config.max_sentences == 25
        assert summary_config.similarity_threshold == 0.08
        assert summary_config.convergence_threshold == 1e-6
        assert summary_config.max_iter == 200
        assert summary_config.damping == 0.85
        assert summary_config.max_words_per_segment == 60
        assert summary_config.min_words_per_sentence == 8
        assert summary_config.dedup_threshold == 0.65
        assert summary_config.min_informative_chars == 30
        assert summary_config.sentences_per_paragraph == 3
        assert summary_config.ollama_base_url == "http://localhost:11434"
        assert summary_config.ollama_model == "llama3.2:3b"
        assert summary_config.ollama_timeout == 300

    # ── TC-CFG.2: Custom values ───────────────────────────────────

    def test_custom_values(self, custom_summary_config):
        """Config kustom memiliki nilai yang diubah."""
        assert custom_summary_config.compression_ratio == 0.30
        assert custom_summary_config.min_sentences == 5
        assert custom_summary_config.max_sentences == 15
        assert custom_summary_config.similarity_threshold == 0.10
        assert custom_summary_config.min_words_per_sentence == 5
        assert custom_summary_config.dedup_threshold == 0.70

    # ── TC-CFG.3: Extra whisper artifacts default ─────────────────

    def test_extra_whisper_artifacts_default(self, summary_config):
        """Field extra_whisper_artifacts memiliki list default yang benar."""
        artifacts = summary_config.extra_whisper_artifacts
        assert isinstance(artifacts, list)
        assert len(artifacts) > 0
        assert "terima kasih telah menonton" in artifacts
        assert "subscribe" in artifacts

    # ── TC-CFG.4: Config independence (no shared state) ───────────

    def test_config_instances_independent(self):
        """Dua instance SummaryConfig tidak saling mempengaruhi."""
        from summarize.config import SummaryConfig
        cfg1 = SummaryConfig()
        cfg2 = SummaryConfig()
        cfg1.extra_whisper_artifacts.append("test_artifact_baru")
        # cfg2 tidak boleh terpengaruh
        assert "test_artifact_baru" not in cfg2.extra_whisper_artifacts
