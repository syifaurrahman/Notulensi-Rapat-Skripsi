"""
reprocess_ollama.py
===================
Memproses ulang file ringkasan yang GAGAL di-rewrite Ollama.
Menggunakan data LexRank dari debug JSON yang sudah ada,
lalu menyimpan hasil Ollama ke file ringkasan dengan nama yang sama.

Jalankan: python reprocess_ollama.py
"""

import sys
import os
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ─── PATH KONFIGURASI ────────────────────────────────────────────────────────

BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
SUMMARIZE_DIR    = os.path.join(BASE_DIR, "hasil_summarize")

# File yang gagal diringkas Ollama (dari log server tadi)
TARGET_BASENAME  = (
    "ringkasan_Rekaman Zoom Sesi 1 tanggal 17 September 2020 "
    "- Mata Kuliah  Dasar Manajemen dan Bisnis - Lapaq Dosen 360p h264_20260828_123703"
)

# txt_path yang tersimpan di DB (nama file transkrip tanpa path)
TXT_PATH_DB      = (
    "transkrip_Rekaman Zoom Sesi 1 tanggal 17 September 2020 "
    "- Mata Kuliah  Dasar Manajemen dan Bisnis - Lapaq Dosen 360p h264_20260828_123703.txt"
)

# Konfigurasi DB
DB_CONFIG = {
    'host'    : 'localhost',
    'user'    : 'root',
    'password': '',
    'database': 'notulensi',
    'charset' : 'utf8mb4',
}

RINGKASAN_FILE   = os.path.join(SUMMARIZE_DIR, TARGET_BASENAME + ".txt")
DEBUG_JSON_FILE  = os.path.join(SUMMARIZE_DIR, TARGET_BASENAME + "_debug.json")
OLLAMA_DIR       = os.path.join(SUMMARIZE_DIR, "ollama")

# Nama file output Ollama
OLLAMA_FILENAME  = "ollama_Rekaman Zoom Sesi 1 tanggal 17 September 2020 - Mata Kuliah  Dasar Manajemen dan Bisnis - Lapaq Dosen 360p h264_20260828_123703.txt"
OLLAMA_FILE      = os.path.join(OLLAMA_DIR, OLLAMA_FILENAME)

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  REPROCESS OLLAMA — File yang Sebelumnya Gagal")
    print("=" * 65)

    # 1. Verifikasi file debug JSON ada
    if not os.path.isfile(DEBUG_JSON_FILE):
        print(f"\n[ERROR] Debug JSON tidak ditemukan:\n  {DEBUG_JSON_FILE}")
        sys.exit(1)
    print(f"\n[1] Debug JSON ditemukan: {os.path.basename(DEBUG_JSON_FILE)}")

    # 2. Load ranked sentences dari debug JSON
    with open(DEBUG_JSON_FILE, "r", encoding="utf-8") as f:
        ranked_data = json.load(f)

    sentences = [item["sentence"] for item in ranked_data if "sentence" in item]
    print(f"    {len(sentences)} kalimat LexRank ditemukan")

    # Ambil top-25 kalimat untuk prompt (sesuai max_sentences config)
    top_sentences = sentences[:25]

    # 3. Load teks ringkasan saat ini sebagai context
    context = ""
    if os.path.isfile(RINGKASAN_FILE):
        with open(RINGKASAN_FILE, "r", encoding="utf-8") as f:
            context = f.read()
        print(f"    Ringkasan saat ini: {len(context):,} karakter")

    # 4. Import OllamaRewriter
    sys.path.insert(0, os.path.join(BASE_DIR, "whispertranscription"))
    try:
        from summarize.ollama_rewriter import OllamaRewriter
        from summarize.config import SummaryConfig
    except ImportError as e:
        print(f"\n[ERROR] Gagal import OllamaRewriter: {e}")
        sys.exit(1)

    cfg = SummaryConfig()
    print(f"\n[2] Ollama URL : {cfg.ollama_base_url}")
    print(f"    Model      : {cfg.ollama_model}")
    print(f"    Timeout    : {cfg.ollama_timeout}s")

    # 5. Cek Ollama tersedia
    rewriter = OllamaRewriter(cfg)
    print("\n[3] Mengecek koneksi Ollama...")
    if not rewriter.is_available():
        print(f"    [ERROR] Ollama tidak tersedia di {cfg.ollama_base_url}")
        print("    Pastikan Ollama sudah berjalan (ollama serve)")
        sys.exit(1)
    print("    [OK] Ollama tersedia!")

    # 6. Panggil Ollama
    print(f"\n[4] Memanggil Ollama ({cfg.ollama_model}) untuk rewrite...")
    print(f"    Input: {len(top_sentences)} kalimat, context: {len(context):,} karakter")
    print("    (Ini bisa memakan waktu 1-3 menit...)\n")

    result = rewriter.rewrite(top_sentences, full_context=context)

    if not result:
        print("\n[ERROR] Ollama mengembalikan hasil kosong.")
        sys.exit(1)

    print(f"\n[OK] Ollama selesai! Output: {len(result):,} karakter")

    # 7. Simpan ke file ringkasan (nama sama, isi diganti)
    print(f"\n[5] Menyimpan ke file ringkasan (overwrite)...")

    # Baca header dari file ringkasan lama (4 baris pertama s/d separator)
    header_lines = []
    if os.path.isfile(RINGKASAN_FILE):
        with open(RINGKASAN_FILE, "r", encoding="utf-8") as f:
            raw = f.read()
        # Cari separator ====
        sep = "=" * 40
        idx = raw.find(sep)
        if idx != -1:
            header_lines = raw[:idx + len(sep)].rstrip()
        else:
            # Ambil 4 baris pertama saja
            lines = raw.splitlines()
            header_lines = "\n".join(lines[:5])
    
    new_content = header_lines + "\n\n" + result + "\n"

    with open(RINGKASAN_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"    [OK] Disimpan: {os.path.basename(RINGKASAN_FILE)}")
    print(f"         Ukuran baru: {len(new_content):,} karakter")

    # 8. Simpan juga ke folder Ollama
    os.makedirs(OLLAMA_DIR, exist_ok=True)
    with open(OLLAMA_FILE, "w", encoding="utf-8") as f:
        f.write("=== HASIL OLLAMA ABSTRACTIVE ===\n")
        f.write(f"Model     : {cfg.ollama_model}\n")
        f.write(f"Sumber    : {TARGET_BASENAME}.txt\n")
        f.write("=" * 40 + "\n\n")
        f.write(result)
    print(f"    [OK] Disimpan: ollama/{os.path.basename(OLLAMA_FILE)}")

    # 9. Update database
    print(f"\n[6] Mengupdate database...")
    try:
        import pymysql
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            # Cari ID record berdasarkan txt_path
            cur.execute(
                "SELECT id, judul_rapat FROM notulensi_hasil WHERE txt_path = %s ORDER BY id DESC LIMIT 1",
                (TXT_PATH_DB,)
            )
            row = cur.fetchone()
            if row:
                db_id    = row[0]
                judul    = row[1]
                # Update kolom ringkasan dengan hasil Ollama
                cur.execute(
                    "UPDATE notulensi_hasil SET ringkasan = %s, sum_path = %s WHERE id = %s",
                    (result, os.path.basename(RINGKASAN_FILE), db_id)
                )
                conn.commit()
                print(f"    [OK] Database ID {db_id} diupdate!")
                print(f"         Judul: {judul}")
            else:
                print(f"    [WARN] Record tidak ditemukan untuk txt_path:\n    {TXT_PATH_DB}")
                print("    Coba cek ID manual di phpMyAdmin dan update manual.")
        conn.close()
    except ImportError:
        print("    [WARN] pymysql tidak tersedia, skip update DB.")
        print("    Install: pip install pymysql")
    except Exception as e:
        print(f"    [ERROR] Gagal update DB: {e}")

    print("\n" + "=" * 65)
    print("  SELESAI! File berhasil di-rewrite dengan Ollama.")
    print("=" * 65)

    # Preview 500 karakter pertama
    print("\nPreview hasil Ollama:")
    print("-" * 50)
    print(result[:500])
    print("..." if len(result) > 500 else "")


if __name__ == "__main__":
    main()
