"""
file_picker.py — Pemilih file video/audio interaktif
=====================================================
Class FilePicker menampilkan file video/audio yang ditemukan
dan memungkinkan user memilih secara interaktif atau via path manual.
"""

from __future__ import annotations

import glob
import os
from typing import TYPE_CHECKING, List

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

if TYPE_CHECKING:
    from .config import Config


class FilePicker:
    """Pemilih file video/audio interaktif berbasis terminal."""

    def __init__(self, cfg: "Config", console: Console | None = None):
        self._cfg = cfg
        self._console = console or Console()

    def _find_files(self) -> List[str]:
        """Cari file video/audio di direktori saat ini dan subfolder."""
        found_files: List[str] = []
        for ext in self._cfg.file_extensions:
            found_files.extend(glob.glob(os.path.join(os.getcwd(), f"*.{ext}")))
            found_files.extend(
                glob.glob(os.path.join(os.getcwd(), f"**/*.{ext}"), recursive=True)
            )
        # Hapus duplikat, pertahankan urutan
        return list(dict.fromkeys(found_files))

    def _display_table(self, files: List[str]) -> None:
        """Tampilkan tabel file yang ditemukan."""
        table = Table(title="File Video/Audio Ditemukan", show_lines=True)
        table.add_column("No", style="cyan", width=4)
        table.add_column("Nama File", style="white")
        table.add_column("Ukuran", justify="right", style="green")

        for i, fp in enumerate(files):
            size_mb = os.path.getsize(fp) / (1024 * 1024)
            table.add_row(str(i + 1), os.path.basename(fp), f"{size_mb:.1f} MB")

        self._console.print(table)
        self._console.print(
            "[dim]Ketik nomor dari daftar di atas, atau ketik path lengkap file.[/dim]"
        )

    def pick(self) -> str:
        """
        Tampilkan file video/audio yang ditemukan dan biarkan user memilih,
        atau ketik path manual. Return path file yang dipilih.
        """
        self._console.print()
        self._console.rule("[bold blue]🎬 Pilih File Video/Audio[/bold blue]")

        found_files = self._find_files()

        if found_files:
            self._display_table(found_files)
        else:
            self._console.print(
                "[yellow]Tidak ada file video/audio ditemukan di folder ini.[/yellow]"
            )
            self._console.print("[dim]Ketik path lengkap ke file Anda.[/dim]")

        while True:
            answer = Prompt.ask("\n[bold yellow]Pilih No / Path file").strip()

            # Cek jika user memilih nomor
            if answer.isdigit() and found_files:
                idx = int(answer) - 1
                if 0 <= idx < len(found_files):
                    return found_files[idx]
                else:
                    self._console.print("[red]Nomor tidak valid.[/red]")
                    continue

            # Cek path langsung
            if os.path.isfile(answer):
                return answer

            self._console.print(f"[red]File tidak ditemukan: {answer}[/red]")
