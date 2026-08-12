"""
test_audio_processor.py — Whitebox Test: AudioProcessor
=========================================================
Menguji semua jalur internal AudioProcessor.

Teknik whitebox:
  - Branch Coverage: resample same_rate/diff_rate, normalize peak>0/peak==0
  - Path Coverage: full pipeline prepare()
"""

import numpy as np
import pytest
from unittest.mock import patch, MagicMock


class TestAudioProcessorResample:
    """Whitebox testing untuk AudioProcessor.resample()."""

    # ── TC-AP.1: Same sample rate (no resample) ───────────────────

    def test_resample_same_rate(self):
        """Menguji jalur: from_sr == to_sr → audio dikembalikan langsung."""
        from whisperLiveTranscription.config import Config
        from whisperLiveTranscription.audio_processor import AudioProcessor

        cfg = Config(model_size="tiny", language="id", use_autocorrect=False)
        ap = AudioProcessor(cfg)

        audio = np.random.randn(16000).astype(np.float32)
        result = ap.resample(audio, 16000, 16000)
        np.testing.assert_array_equal(result, audio)

    # ── TC-AP.2: Different sample rate ────────────────────────────

    def test_resample_different_rate(self):
        """Menguji jalur: from_sr != to_sr → resample via scipy."""
        from whisperLiveTranscription.config import Config
        from whisperLiveTranscription.audio_processor import AudioProcessor

        cfg = Config(model_size="tiny", language="id", use_autocorrect=False)
        ap = AudioProcessor(cfg)

        # 48kHz → 16kHz
        audio = np.random.randn(48000).astype(np.float32)
        result = ap.resample(audio, 48000, 16000)
        # Output harus sekitar 1/3 panjang input
        expected_len = 16000
        assert abs(len(result) - expected_len) < 100  # toleransi kecil
        assert result.dtype == np.float32


class TestAudioProcessorNormalize:
    """Whitebox testing untuk AudioProcessor.normalize()."""

    # ── TC-AP.3: Peak > 0 (normal audio) ─────────────────────────

    def test_normalize_normal_audio(self):
        """Menguji jalur: peak > 0 → dinormalisasi ke [-1, 1]."""
        from whisperLiveTranscription.config import Config
        from whisperLiveTranscription.audio_processor import AudioProcessor

        cfg = Config(model_size="tiny", language="id", use_autocorrect=False)
        ap = AudioProcessor(cfg)

        audio = np.array([0.5, -1.0, 0.3, -0.7], dtype=np.float32)
        result = ap.normalize(audio)
        assert np.max(np.abs(result)) <= 1.0 + 1e-6
        assert result.dtype == np.float32

    # ── TC-AP.4: Peak == 0 (silence) ──────────────────────────────

    def test_normalize_silence(self):
        """Menguji jalur: peak == 0 → audio dikembalikan tanpa perubahan."""
        from whisperLiveTranscription.config import Config
        from whisperLiveTranscription.audio_processor import AudioProcessor

        cfg = Config(model_size="tiny", language="id", use_autocorrect=False)
        ap = AudioProcessor(cfg)

        audio = np.zeros(1000, dtype=np.float32)
        result = ap.normalize(audio)
        np.testing.assert_array_equal(result, audio)

    # ── TC-AP.5: Normalize preserves relative amplitude ──────────

    def test_normalize_preserves_ratio(self):
        """Normalisasi harus mempertahankan rasio antar sampel."""
        from whisperLiveTranscription.config import Config
        from whisperLiveTranscription.audio_processor import AudioProcessor

        cfg = Config(model_size="tiny", language="id", use_autocorrect=False)
        ap = AudioProcessor(cfg)

        audio = np.array([2.0, 4.0, -6.0], dtype=np.float32)
        result = ap.normalize(audio)
        # Rasio: 2/6, 4/6, -6/6 = 0.333, 0.667, -1.0
        np.testing.assert_almost_equal(result[2], -1.0, decimal=5)
        np.testing.assert_almost_equal(result[0] / result[1], 0.5, decimal=5)


class TestAudioProcessorPrepare:
    """Whitebox testing untuk AudioProcessor.prepare() full pipeline."""

    # ── TC-AP.6: Full pipeline ────────────────────────────────────

    def test_prepare_full_pipeline(self):
        """Menguji jalur lengkap: resample → noise reduction → normalize."""
        from whisperLiveTranscription.config import Config
        from whisperLiveTranscription.audio_processor import AudioProcessor

        cfg = Config(model_size="tiny", language="id", use_autocorrect=False)
        ap = AudioProcessor(cfg)

        # Mock noise_filter.apply agar tidak perlu noisereduce
        with patch.object(ap.noise_filter, 'apply', side_effect=lambda audio, sr: audio):
            audio = np.random.randn(16000).astype(np.float32) * 0.5
            result = ap.prepare(audio, from_sr=16000, to_sr=16000)
            assert isinstance(result, np.ndarray)
            assert result.dtype == np.float32
            # Harus sudah dinormalisasi
            assert np.max(np.abs(result)) <= 1.0 + 1e-6
