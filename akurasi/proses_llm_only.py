"""
proses_llm_only.py — Proses ringkasan transkrip Psikologi menggunakan LLM saja (tanpa LexRank)
============================================================================================
Cara pakai:
    python proses_llm_only.py
"""

import os
import sys
import json
import urllib.request
import urllib.error

# Tambahkan root directory ke sys.path agar bisa import modul
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PARENT_DIR)

from whispertranscription.summarize.config import SummaryConfig

def check_ollama(url: str) -> bool:
    try:
        req = urllib.request.Request(f"{url}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def call_ollama(url: str, model: str, prompt: str, timeout: int) -> str:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.15,
            "top_p": 0.90,
            "num_predict": 4096,
            "num_ctx": 8192,
            "repeat_penalty": 1.15,
            "top_k": 40,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{url}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
        return body.get("response", "")

def build_prompt_llm_only(context: str) -> str:
    # Potong konteks jika terlalu panjang (seperti cara ollama_rewriter)
    max_ctx = 12000
    if len(context) <= max_ctx:
        context_section = context
    else:
        chunk = max_ctx // 3
        ctx_start = context[:chunk].strip()
        mid_point = len(context) // 2
        ctx_mid   = context[mid_point - chunk//2 : mid_point + chunk//2].strip()
        ctx_end   = context[-chunk:].strip()
        context_section = f"""
[BAGIAN AWAL TRANSKRIP]:
{ctx_start}

[BAGIAN TENGAH TRANSKRIP]:
{ctx_mid}

[BAGIAN AKHIR TRANSKRIP]:
{ctx_end}
"""

    prompt = f"""Anda adalah sekretaris akademik profesional yang bertugas membuat notulensi rapat atau catatan perkuliahan yang lengkap, terstruktur, dan informatif.

TUGAS ANDA:
Baca transkrip rapat/kuliah di bawah ini dengan cermat, lalu susun NOTULENSI RAPAT yang komprehensif. Notulensi harus mampu dipahami oleh orang yang tidak hadir dalam rapat tersebut.

=== ATURAN KONTEN (WAJIB) ===
1. JELASKAN SETIAP KONSEP SECARA LENGKAP. Tulis definisi, penjelasan, contoh, atau perbandingannya jika ada di transkrip.
2. TANGKAP SEMUA POIN PENTING dari transkrip. Jangan melewatkan informasi substansial.
3. Setiap poin harus SPESIFIK dan INFORMATIF. Hindari kalimat umum seperti "dijelaskan mengenai X" — ganti dengan "X adalah ... yang berfungsi untuk ...".
4. SINTESIS pertanyaan dan diskusi. Tulis: pertanyaan apa yang diajukan, jawaban atau penjelasan apa yang diberikan.
5. JANGAN mengarang informasi yang tidak ada di transkrip.
6. Gunakan Bahasa Indonesia baku. Hapus kata filler (ya, gitu, nah, kan, oke, eee).

=== ATURAN FORMAT OUTPUT (WAJIB DIIKUTI PERSIS) ===
1. Mulai langsung dengan bagian pertama. JANGAN tulis pengantar seperti "Berikut notulensi..." atau "Di bawah ini adalah...".
2. Setiap JUDUL BAGIAN ditulis dengan format: **Judul Bagian:** (diapit dua bintang, diakhiri titik dua). Contoh: **Pembukaan:** atau **Definisi Organisasi:**
3. Di bawah setiap judul, tulis poin-poin menggunakan tanda strip: - poin
4. Pisahkan setiap bagian dengan SATU baris kosong.
5. HANYA tanda ** boleh digunakan — hanya untuk judul bagian. DILARANG menggunakan ##, *, _, atau ` dalam output.
6. DILARANG menggunakan angka di depan poin (1. 2. 3.) — gunakan hanya tanda strip (-).

=== STRUKTUR BAGIAN (sesuaikan dengan isi transkrip) ===

**Pembukaan:**
- [Siapa yang membuka, kapan, apa agenda rapat/kuliah, siapa yang hadir jika disebutkan]

**[Nama Topik Utama 1 — sesuaikan, misal: Sejarah Psikologi Sosial]:**
- [Penjelasan detail konsep 1 dari topik ini]
- [Penjelasan detail konsep 2 dari topik ini]

**[Nama Topik Utama 2 — jika ada topik berbeda, misal: Definisi Inti Psikologi Sosial]:**
- [Penjelasan detail...]

**Pertanyaan dan Diskusi:**
- Pertanyaan: [isi pertanyaan] — Jawaban: [ringkasan jawaban yang diberikan]

**Kesimpulan:**
- [Poin simpulan utama 1]
- [Poin simpulan utama 2]

**Penutup:**
- [Bagaimana rapat/kuliah ditutup, ada pengumuman, atau informasi tambahan]

=== TRANSKRIP RAPAT / KULIAH UNTUK DIPROSES ===
{context_section}

NOTULENSI RAPAT:"""
    return prompt

def main():
    transkrip_path = os.path.join(PARENT_DIR, "hasil", "whisper transkrip psikologi.txt")
    output_dir = os.path.join(PARENT_DIR, "hasil_summarize")
    output_path = os.path.join(output_dir, "LLM_only.txt")

    if not os.path.exists(transkrip_path):
        print(f"[ERROR] File transkrip tidak ditemukan: {transkrip_path}")
        sys.exit(1)

    print(f"[Notulensia] Membaca file transkrip: {transkrip_path}")
    with open(transkrip_path, "r", encoding="utf-8", errors="ignore") as f:
        content_lines = f.readlines()

    # Skip header
    header_ended = False
    clean_text_lines = []
    for line in content_lines:
        if header_ended:
            clean_text_lines.append(line)
        elif "========================================" in line:
            header_ended = True

    text = " ".join(clean_text_lines).strip()
    if not text:
        print("[ERROR] Teks transkrip kosong.")
        sys.exit(1)

    cfg = SummaryConfig()
    
    # Cek ketersediaan Ollama
    print(f"[Notulensia] Memeriksa koneksi server Ollama ({cfg.ollama_base_url})...")
    if not check_ollama(cfg.ollama_base_url):
        print("[ERROR] Server Ollama tidak aktif / offline! Pastikan aplikasi Ollama sudah berjalan.")
        print("        Silakan jalankan perintah: `ollama run llama3.2:3b` di terminal/CMD Anda terlebih dahulu.")
        sys.exit(1)

    print("[Notulensia] Server Ollama online. Membangun prompt LLM Only...")
    prompt = build_prompt_llm_only(text)

    print(f"[Notulensia] Mengirim ke LLM {cfg.ollama_model} (Proses ini bisa memakan waktu 30-60 detik)...")
    try:
        response = call_ollama(cfg.ollama_base_url, cfg.ollama_model, prompt, cfg.ollama_timeout)
        if not response:
            print("[ERROR] Hasil generasi LLM kosong.")
            sys.exit(1)
            
        # Tulis ke file LLM_only.txt
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("========================================\n")
            f.write("   RINGKASAN ABSTRAKTIF (LLM ONLY)\n")
            f.write("   Sistem Notulensia — Tanpa LexRank\n")
            f.write("========================================\n")
            f.write(response + "\n")
        
        print(f"[SUCCESS] Hasil ringkasan LLM Only disimpan ke: {output_path}")
        
    except Exception as e:
        print(f"[ERROR] Gagal memanggil Ollama: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
