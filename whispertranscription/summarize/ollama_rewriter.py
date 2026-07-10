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
        """Bangun prompt yang menghasilkan notulensi rapat berstruktur per bagian."""

        joined = "\n".join(f"- {s}" for s in sentences)

        context_section = ""
        if context:
            max_ctx = 4000   # ~1000 token — diperkecil agar pas dengan num_ctx 2048 tanpa out of memory
            if len(context) <= max_ctx:
                context_section = f"\n\nTRANSKRIP LENGKAP RAPAT (gunakan sebagai sumber utama):\n{context}\n"
            else:
                chunk = max_ctx // 3
                ctx_start = context[:chunk].strip()
                mid_point = len(context) // 2
                ctx_mid   = context[mid_point - chunk//2 : mid_point + chunk//2].strip()
                ctx_end   = context[-chunk:].strip()
                context_section = f"""

TRANSKRIP RAPAT (potongan awal, tengah, dan akhir):

Bagian awal:
{ctx_start}

Bagian tengah:
{ctx_mid}

Bagian akhir:
{ctx_end}
"""

        prompt = f"""Anda adalah sekretaris akademik profesional yang bertugas membuat notulensi rapat atau catatan perkuliahan yang lengkap, terstruktur, dan informatif.

TUGAS ANDA:
Baca transkrip rapat berikut dengan cermat, lalu susun NOTULENSI RAPAT yang komprehensif. Notulensi harus mampu dipahami oleh orang yang tidak hadir dalam rapat tersebut.

=== ATURAN KONTEN (WAJIB) ===
1. HANYA gunakan informasi dari transkrip yang diberikan di bawah. JANGAN mengarang atau menggunakan contoh.
2. JELASKAN SETIAP KONSEP SECARA LENGKAP dari isi transkrip. Jangan hanya menyebut nama konsep.
3. TANGKAP SEMUA POIN PENTING dari transkrip. Jangan melewatkan informasi substansial.
4. Setiap poin harus SPESIFIK dan INFORMATIF sesuai isi transkrip.
5. SINTESIS pertanyaan dan diskusi. Tulis pertanyaan apa yang diajukan dan jawaban apa yang diberikan.
6. Gunakan Bahasa Indonesia baku. Hapus kata filler (ya, gitu, nah, kan, oke, eee).

=== ATURAN FORMAT OUTPUT (WAJIB DIIKUTI PERSIS) ===
1. Mulai langsung dengan bagian pertama. JANGAN tulis pengantar seperti "Berikut notulensi..." atau "Di bawah ini adalah...".
2. Setiap JUDUL BAGIAN ditulis dengan format: **Judul Bagian:** (diapit dua bintang, diakhiri titik dua).
3. Di bawah setiap judul, tulis poin-poin menggunakan tanda strip: - poin
4. Pisahkan setiap bagian dengan SATU baris kosong.
5. HANYA tanda ** boleh digunakan — hanya untuk judul bagian. DILARANG menggunakan ##, *, _, atau ` dalam output.
6. DILARANG menggunakan angka di depan poin (1. 2. 3.) — gunakan hanya tanda strip (-).

=== STRUKTUR BAGIAN (sesuaikan dengan isi transkrip yang diberikan) ===

**Pembukaan:**
- [Isi berdasarkan transkrip: siapa yang membuka, apa agenda, siapa yang hadir]

**[Topik Utama 1 dari transkrip]:**
- [Poin penting dari transkrip terkait topik ini]
- [Poin lainnya dari transkrip]

**[Topik Utama 2 dari transkrip — jika ada]:**
- [Isi dari transkrip]

**Pertanyaan dan Diskusi:**
- Pertanyaan: [isi dari transkrip] — Jawaban: [isi dari transkrip]

**Kesimpulan:**
- [Simpulan dari transkrip]
- [Tindak lanjut dari transkrip jika disebutkan]

**Penutup:**
- [Penutupan sesuai transkrip]

=== DATA TRANSKRIP YANG HARUS DIRINGKAS (SUMBER UTAMA — WAJIB DIGUNAKAN) ===

POIN-POIN KUNCI DARI TRANSKRIP:
{joined}
{context_section}
NOTULENSI RAPAT (berdasarkan data di atas):"""

        return prompt


    def _call_ollama(self, prompt: str) -> str:
        """Panggil Ollama API untuk generate teks."""
        url = f"{self.cfg.ollama_base_url}/api/generate"

        payload = json.dumps({
            "model": self.cfg.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.15,       # Sangat rendah = format konsisten, tidak keluar jalur
                "top_p": 0.90,
                "num_predict": 1500,       # Maksimum token output
                "num_ctx": 2048,           # Diturunkan ke 2048 untuk mencegah Out-Of-Memory (OOM) 500 Error
                "repeat_penalty": 1.15,
                "top_k": 40,
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
        """
        Bersihkan output LLM.
        Format **Judul:** pada baris judul DIPERTAHANKAN (untuk render bold di frontend).
        Bold di dalam kalimat biasa dihapus.
        """
        # Hapus tag HTML yang mungkin muncul
        text = re.sub(r'<[^>]+>', '', text)

        # Hapus pengantar generik di awal (sebelum konten notulensi dimulai)
        text = re.sub(
            r'^(ringkasan|summary|hasil|berikut|di bawah ini|adalah notulensi[^:]*|'
            r'notulensi rapat[^:]*|berdasarkan transkrip[^:]*|'
            r'tentu[,\s]+berikut[^:]*|baik[,\s]+berikut[^:]*)[:\s\n]*',
            '', text, flags=re.IGNORECASE
        )

        # Hapus heading markdown (## Header → hapus, akan diganti **Judul:**)
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)

        # Hapus backtick code formatting
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Bersihkan bullet point markdown (*  item → - item)
        text = re.sub(r'^\s*\*\s+', '- ', text, flags=re.MULTILINE)

        # Proses baris per baris:
        # - Baris yang merupakan judul bagian (**Judul:**) → PERTAHANKAN bold
        # - Baris lain → hapus ** agar tidak ada bold di kalimat biasa
        cleaned_lines = []
        for line in text.split('\n'):
            stripped = line.strip()
            # Deteksi baris judul: **...: ** atau **...:** (format yang diminta)
            is_heading = bool(re.match(r'^\*\*.+:\*\*\s*$', stripped) or
                              re.match(r'^\*\*.+?\*\*\s*:?\s*$', stripped))
            if is_heading:
                # Normalisasi: pastikan format persis **Judul:**
                # Contoh: **Definisi Organisasi:** atau **Definisi Organisasi**:
                line = re.sub(r'^\*\*(.+?)\*\*:?\s*$',
                              lambda m: f'**{m.group(1).rstrip(":")}:**',
                              stripped)
            else:
                # Bukan judul → hapus bold/italic
                line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
                line = re.sub(r'__(.+?)__', r'\1', line)
                line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', line)
                line = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'\1', line)
                # Hapus * tersisa
                line = re.sub(r'\*', '', line)
            cleaned_lines.append(line)

        text = '\n'.join(cleaned_lines)

        # Normalisasi whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        return text.strip()
