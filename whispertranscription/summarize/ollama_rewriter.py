"""
ollama_rewriter.py — Abstractive Rewriter menggunakan Ollama (LLM Lokal)
=========================================================================
Menerima kalimat-kalimat extractive dari LexRank → menulis ulang menjadi
ringkasan paragraf yang bersih, koheren, dan profesional.

Requires:
  - Ollama running locally (https://ollama.ai)
  - Model sudah di-pull, misal: ollama pull llama3.2:3b
"""

from __future__ import annotations

import json
import re
import urllib.request
import urllib.error

from .config import SummaryConfig


class OllamaRewriter:
    """
    Menulis ulang kalimat extractive menjadi ringkasan abstraktif
    menggunakan Ollama API (lokal, gratis, tanpa API key).
    """

    def __init__(self, cfg: SummaryConfig | None = None):
        self.cfg = cfg or SummaryConfig()

    def is_available(self) -> bool:
        """Cek apakah Ollama server sedang berjalan."""
        try:
            url = f"{self.cfg.ollama_base_url}/api/tags"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except Exception:
            return False

    def rewrite(self, extractive_sentences: list[str], full_context: str = "") -> str:
        """
        Tulis ulang kalimat extractive menjadi ringkasan koheren.

        Args:
            extractive_sentences: Kalimat-kalimat yang dipilih LexRank.
            full_context: (Opsional) Potongan teks asli untuk konteks tambahan.

        Returns:
            Ringkasan paragraf yang bersih, atau string kosong jika gagal.
        """
        if not extractive_sentences:
            return ""

        prompt = self._build_prompt(extractive_sentences, full_context)

        try:
            response = self._call_ollama(prompt)
            if response:
                return self._clean_response(response)
        except Exception as e:
            print(f"[OllamaRewriter] ✗ Error: {e}", flush=True)

        return ""

    def _build_prompt(self, sentences: list[str], context: str = "") -> str:
        """Bangun prompt yang optimal untuk summarization Bahasa Indonesia."""

        joined = "\n".join(f"- {s}" for s in sentences)

        # Berikan konteks seluas mungkin agar LLM bisa menangkap detail spesifik
        # seperti tugas, nama, angka, keputusan yang mungkin tidak ter-ekstrak LexRank
        context_section = ""
        if context:
            max_ctx = 12000  # ~3000 token, cukup untuk llama3.2:3b (context 8k)
            if len(context) <= max_ctx:
                # Teks cukup pendek — berikan seluruhnya
                context_section = f"""

TRANSKRIP LENGKAP RAPAT (gunakan ini sebagai sumber utama):
{context}
"""
            else:
                # Teks terlalu panjang — ambil awal, tengah, dan akhir
                chunk = max_ctx // 3
                ctx_start = context[:chunk].strip()
                mid_point = len(context) // 2
                ctx_mid = context[mid_point - chunk//2 : mid_point + chunk//2].strip()
                ctx_end = context[-chunk:].strip()
                context_section = f"""

TRANSKRIP RAPAT (potongan awal, tengah, dan akhir):

Bagian awal:
{ctx_start}

Bagian tengah:
{ctx_mid}

Bagian akhir:
{ctx_end}
"""

        prompt = f"""Anda adalah sekretaris profesional yang merangkum notulensi rapat atau catatan kuliah.

LANGKAH 1 — IDENTIFIKASI TOPIK UTAMA:
Sebelum menulis, baca seluruh transkrip dan tentukan: Apa TOPIK UTAMA yang paling banyak dibahas?
Contoh: Jika topik utama adalah "LexRank" atau "Sistem Notulensi", maka SELURUH ringkasan harus berfokus pada topik itu.

LANGKAH 2 — TULIS RINGKASAN BERDASARKAN TOPIK UTAMA:
Buat ringkasan notulensi yang KOMPREHENSIF, PADAT, dan AKURAT berdasarkan topik utama yang Anda identifikasi.

FORMAT ADAPTIF:
- Jika KULIAH/PRESENTASI: Jelaskan materi, konsep, cara kerja, dan contoh yang diajarkan secara detail.
- Jika RAPAT PROYEK: Fokus pada keputusan, action items, dan kendala.
- Jika DISKUSI: Fokus pada ide-ide pokok dan kesepakatan.

ATURAN KRITIS (WAJIB DIPATUHI):
1. FOKUS pada TOPIK UTAMA. Jika ada 10 menit membahas LexRank dan 1 menit menyebut install software, RINGKASAN harus didominasi LexRank, bukan install software.
2. Hal yang hanya DISEBUTKAN SEKILAS (bukan topik utama) TIDAK PERLU dimasukkan ke ringkasan.
3. JANGAN mengarang. Hanya tulis yang ada di transkrip.
4. JANGAN tulis kalimat generik seperti "Rapat ini membahas...", "Tujuan rapat adalah...". Langsung ke isi.
5. Setiap poin harus SPESIFIK dan INFORMATIF (nama algoritma, cara kerja, langkah-langkah, dll).
6. Gunakan Bahasa Indonesia baku. Hapus filler (ya, gitu, nah, kan, sih).

ATURAN FORMAT OUTPUT (WAJIB):
1. DILARANG markdown (**, ##, *, _). Jangan gunakan tanda bintang.
2. Judul bagian: HURUF KAPITAL diikuti baris baru.
3. Daftar: gunakan tanda strip (- item) atau angka (1. item).
4. Pisahkan bagian dengan baris kosong.
5. Langsung sajikan ringkasan. Jangan jelaskan proses analisis Anda.

POIN-POIN KUNCI HASIL EKSTRAKSI:
{joined}
{context_section}
NOTULENSI RAPAT:"""

        return prompt

    def _call_ollama(self, prompt: str) -> str:
        """Panggil Ollama API untuk generate teks."""
        url = f"{self.cfg.ollama_base_url}/api/generate"

        payload = json.dumps({
            "model": self.cfg.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.25,      # Lebih rendah untuk akurasi
                "top_p": 0.85,
                "num_predict": 3072,       # Lebih banyak token untuk detail
                "num_ctx": 8192,           # Context window penuh
                "repeat_penalty": 1.2,     # Lebih tinggi, hindari pengulangan
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        print(f"[OllamaRewriter] Memanggil Ollama ({self.cfg.ollama_model})...", flush=True)

        with urllib.request.urlopen(req, timeout=self.cfg.ollama_timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("response", "")

    def _clean_response(self, text: str) -> str:
        """Bersihkan output LLM dari artefak markdown dan formatting."""
        # Hapus tag HTML yang mungkin muncul
        text = re.sub(r'<[^>]+>', '', text)

        # Hapus "Ringkasan:" atau header serupa di awal
        text = re.sub(
            r'^(ringkasan|summary|hasil|berikut|di bawah ini)[:\s]*',
            '', text, flags=re.IGNORECASE
        )

        # ── Hapus semua formatting markdown ──
        # Hapus **bold** dan __bold__
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)

        # Hapus *italic* dan _italic_
        text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text)
        text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'\1', text)

        # Hapus heading markdown (## Header → Header)
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)

        # Hapus backtick code formatting
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Bersihkan bullet point markdown (  * item → - item)
        text = re.sub(r'^\s*\*\s+', '- ', text, flags=re.MULTILINE)

        # Hapus tanda bintang yang tersisa tanpa pasangan
        text = re.sub(r'\*', '', text)

        # Normalisasi whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        return text.strip()
