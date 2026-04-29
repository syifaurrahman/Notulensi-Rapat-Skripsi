"""
transcriber.py — Mesin Transkripsi File Video/Audio
=====================================================
Class FileTranscriber mengelola:
  - Load model Whisper ke GPU/CPU
  - Orchestrasi: ekstrak audio → noise reduce → chunk → transkripsi → filter
  - Simpan hasil ke file .txt bertimestamp
"""

from __future__ import annotations

import datetime
import os
import sys
import tempfile
from typing import TYPE_CHECKING

import numpy as np
import whisper
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

if TYPE_CHECKING:
    from .config import Config

from .audio_extractor import AudioExtractor
from .hallucination_filter import HallucinationFilter


class FileTranscriber:
    """
    Transkripsi file video/audio secara offline.

    Cara pakai:
        t = FileTranscriber(cfg)
        t.load_model()
        text = t.transcribe_file("video.mp4")
        path = t.save_result(text, "video.mp4")
    """

    def __init__(self, cfg: "Config", console: Console | None = None):
        self._cfg       = cfg
        self._console   = console or Console()
        self._extractor = AudioExtractor(cfg, self._console)
        self._filter    = HallucinationFilter(cfg)
        self._model     = None
        self._device    = "cpu"

    # ── Model Loading ─────────────────────────────────

    def load_model(self) -> None:
        """Load Whisper model ke GPU atau CPU dengan fallback otomatis."""
        cfg = self._cfg
        self._device = "cuda" if cfg.use_gpu else "cpu"
        self._console.print(
            f"\n[bold green]Memuat model Whisper '{cfg.model_size}' "
            f"ke {self._device.upper()}...[/bold green]"
        )
        try:
            self._model = whisper.load_model(cfg.model_size).to(self._device)
        except Exception as e:
            self._console.print(
                f"[yellow]⚠ {self._device.upper()} tidak tersedia ({e}), "
                f"fallback ke CPU...[/yellow]"
            )
            self._device = "cpu"
            self._model = whisper.load_model(cfg.model_size)

    # ── Transkripsi ───────────────────────────────────

    def transcribe_file(self, video_path: str) -> str:
        """
        Transkripsi file video/audio lengkap.
        Return teks hasil transkripsi.
        """
        cfg = self._cfg
        extractor = self._extractor

        # Cek ffmpeg
        if not extractor.check_ffmpeg():
            self._console.print("[bold red]✗ ffmpeg tidak ditemukan![/bold red]")
            self._console.print("  Install ffmpeg dan tambahkan ke PATH sistem.")
            self._console.print("  Download: https://ffmpeg.org/download.html")
            sys.exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self._console,
        ) as progress:

            # 1. Ekstrak audio
            task_extract = progress.add_task(
                "[cyan]Mengekstrak audio dari video...", total=1
            )
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_wav = tmp.name

            try:
                extractor.extract_audio(video_path, tmp_wav)
                progress.update(task_extract, completed=1)
                self._console.print("[green]✓ Audio berhasil diekstrak[/green]")
            except RuntimeError as e:
                self._console.print(f"[bold red]✗ {e}[/bold red]")
                sys.exit(1)

            # 2. Baca audio
            audio, sr = extractor.read_audio(tmp_wav)
            duration_min = len(audio) / sr / 60
            self.last_duration_sec = int(len(audio) / sr)
            self._console.print(
                f"[dim]  Durasi audio: {duration_min:.1f} menit | "
                f"Sample rate: {sr} Hz[/dim]"
            )

            # 3. Noise Reduction
            task_nr = progress.add_task(
                "[cyan]Menerapkan noise reduction...", total=1
            )
            audio = extractor.apply_noise_reduction(audio, sr)
            audio = extractor.normalize_audio(audio)
            progress.update(task_nr, completed=1)
            self._console.print("[green]✓ Noise reduction selesai[/green]")

            # 4. Split audio menjadi chunks
            chunks = extractor.split_into_chunks(audio, sr)
            total_chunks = len(chunks)
            self._console.print(
                f"[dim]  Total chunk: {total_chunks} "
                f"(@ {cfg.chunk_seconds}s dengan 2s overlap)[/dim]\n"
            )

            # 5. Transkripsi per chunk
            task_trans = progress.add_task(
                f"[bold green]Transkripsi ({total_chunks} chunk)...",
                total=total_chunks,
            )

            all_text_parts = []
            prev_segment_text = ""

            for i, chunk_audio in enumerate(chunks):
                progress.update(
                    task_trans,
                    description=f"[bold green]Chunk {i + 1}/{total_chunks}...",
                )

                # Lewati chunk yang terlalu pendek (< 0.5 detik)
                if len(chunk_audio) < sr * 0.5:
                    progress.advance(task_trans)
                    continue

                try:
                    result = self._model.transcribe(
                        chunk_audio,
                        language=cfg.language,
                        fp16=(self._device == "cuda"),
                        beam_size=cfg.beam_size,
                        temperature=cfg.temperature_fallback,
                        condition_on_previous_text=cfg.condition_on_previous_text,
                        compression_ratio_threshold=cfg.compression_ratio_threshold,
                        no_speech_threshold=cfg.no_speech_threshold,
                        logprob_threshold=cfg.logprob_threshold,
                        word_timestamps=False,
                    )

                    chunk_text = result["text"].strip()

                    # Filter halusinasi
                    if self._filter.is_hallucination(chunk_text):
                        progress.advance(task_trans)
                        continue

                    # Filter duplikat
                    if chunk_text == prev_segment_text:
                        progress.advance(task_trans)
                        continue

                    if chunk_text:
                        all_text_parts.append(chunk_text)
                        prev_segment_text = chunk_text

                except Exception as e:
                    self._console.print(
                        f"[yellow]⚠ Chunk {i + 1} gagal: {e}[/yellow]"
                    )

                progress.advance(task_trans)

        # Hapus file temp
        try:
            os.unlink(tmp_wav)
        except Exception:
            pass

        return " ".join(all_text_parts).strip()

    # ── Simpan Hasil ──────────────────────────────────

    def save_result(self, text: str, video_path: str) -> str:
        """
        Simpan teks transkripsi ke file .txt bertimestamp.
        Return path file output.
        """
        cfg = self._cfg
        os.makedirs(cfg.output_dir, exist_ok=True)

        timestamp  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        out_path   = os.path.join(cfg.output_dir, f"transkrip_{video_name}_{timestamp}.txt")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("=== TRANSKRIPSI RAPAT ===\n")
            f.write(f"File Video  : {video_path}\n")
            f.write(f"Dibuat      : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
            f.write(f"Model       : Whisper {cfg.model_size}\n")
            f.write(f"{'=' * 40}\n\n")
            f.write(text)

        return out_path
