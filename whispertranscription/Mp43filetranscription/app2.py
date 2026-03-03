"""
app2.py — Entry Point Transkripsi File Video/Audio (Offline)
=============================================================
File ini adalah satu-satunya yang perlu dijalankan:

  python Mp43filetranscription/app2.py                    # Mode interaktif (pilih file)
  python Mp43filetranscription/app2.py "video.mp4"        # Langsung transkripsi file tertentu

Untuk mengubah konfigurasi (model, bahasa, threshold, dll),
edit parameter di dalam Config() di bawah ini.
"""

import sys
import os

# Pastikan import module Mp43filetranscription berjalan lancar walaupun file dipindah
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel

from Mp43filetranscription.config import Config
from Mp43filetranscription.file_picker import FilePicker
from Mp43filetranscription.transcriber import FileTranscriber


def main():
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]🎙 Whisper Video/Audio Transcription[/bold cyan]\n"
        "[dim]Transkripsi file video/audio rapat ke teks — offline, anti-halusinasi, noise-reduced[/dim]",
        border_style="cyan"
    ))

    # ── Konfigurasi ──────────────────────────────────
    # Edit di sini untuk mengubah perilaku aplikasi.
    # Semua opsi tersedia di Mp43filetranscription/config.py
    config = Config(
        model_size      = "small",    # tiny | base | small | medium | large
        language        = "id",       # Bahasa Indonesia
        # use_gpu otomatis: pakai GPU jika CUDA tersedia, CPU jika tidak
    )
    # ─────────────────────────────────────────────────

    # Pilih file (dari argumen CLI atau interaktif)
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        if not os.path.isfile(video_path):
            console.print(f"[bold red]✗ File tidak ditemukan: {video_path}[/bold red]")
            sys.exit(1)
        console.print(f"\n[green]✓ File dari argumen:[/green] {video_path}")
    else:
        picker = FilePicker(config, console)
        video_path = picker.pick()
        console.print(f"\n[green]✓ File dipilih:[/green] {video_path}")

    # Transkripsi
    transcriber = FileTranscriber(config, console)
    transcriber.load_model()
    final_text = transcriber.transcribe_file(video_path)

    # Tampilkan preview
    console.print()
    preview = final_text[:800] + ("..." if len(final_text) > 800 else "")
    console.print(Panel(
        preview,
        title="[bold green]✓ Hasil Transkripsi (Preview)[/bold green]",
        border_style="green"
    ))

    # Simpan
    out_path = transcriber.save_result(final_text, video_path)

    console.print(f"\n[bold green]✓ Transkripsi disimpan ke:[/bold green]")
    console.print(f"   [underline]{out_path}[/underline]")
    console.print(f"\n[dim]Total karakter: {len(final_text):,}[/dim]")
    console.print()


if __name__ == "__main__":
    main()
