"""
summarize_existing.py — Ringkas file transkrip yang sudah ada & simpan ke DB
============================================================================
Jalankan:
    cd whispertranscription
    python summarize_existing.py

Akan membaca file transkrip, meringkasnya dengan LexRank (+Ollama jika aktif),
lalu menyimpan hasilnya ke database notulensi_hasil.
"""

import os
import sys
import re
import datetime

# ── Path setup ──────────────────────────────────────────────
BASE_DIR            = os.path.dirname(os.path.abspath(__file__))
HASIL_DIR           = os.path.join(BASE_DIR, "hasil")
HASIL_SUMMARIZE_DIR = os.path.join(BASE_DIR, "hasil_summarize")
LIVE_HASIL_DIR      = os.path.join(BASE_DIR, "whisperLiveTranscription", "hasil")

sys.path.insert(0, BASE_DIR)
os.makedirs(HASIL_DIR, exist_ok=True)
os.makedirs(HASIL_SUMMARIZE_DIR, exist_ok=True)

import pymysql
from summarize.lexrank import LexRankSummarizer
from summarize.config  import SummaryConfig

# ── DB Config ────────────────────────────────────────────────
DB_CONFIG = {
    'host'    : 'localhost',
    'user'    : 'root',
    'password': '',
    'database': 'notulensi',
    'charset' : 'utf8mb4',
}

# ── File yang ingin diproses ─────────────────────────────────
# Ganti path ini dengan file yang ingin diringkas
TARGET_FILE = os.path.join(LIVE_HASIL_DIR, "transkrip_20260422_160937.txt")

# Judul rapat (bisa diubah)
JUDUL_RAPAT = "Progress Presentasi Skripsi - 22 April 2026"


# ── Helpers ─────────────────────────────────────────────────

def read_transcript(path: str) -> str:
    """Baca isi transkrip, skip baris header."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Skip header (baris yg dimulai dengan ===, Dibuat, Model, ====)
    lines = raw.splitlines()
    content_lines = []
    header_done = False
    for line in lines:
        stripped = line.strip()
        if not header_done:
            if re.match(r'^={4,}', stripped) and content_lines:
                # Baris === kedua = akhir header
                header_done = True
                continue
            elif stripped.startswith("===") or stripped.startswith("Dibuat") or stripped.startswith("Model"):
                continue
            # Baris === pertama
            if re.match(r'^={4,}', stripped):
                continue
        else:
            content_lines.append(line)

    text = "\n".join(content_lines).strip()
    if not text:
        # Fallback: ambil semua setelah baris keempat
        text = "\n".join(lines[5:]).strip()
    return text


def save_to_db(judul: str, tipe: str, txt_path: str, ringkasan: str) -> int:
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            sql = """
                INSERT INTO notulensi_hasil
                    (judul_rapat, waktu_rapat, tipe_transkripsi, transkrip_txt, ringkasan, file_pdf)
                VALUES (%s, NOW(), %s, %s, %s, '')
            """
            cur.execute(sql, (judul, tipe, txt_path, ringkasan))
            conn.commit()
            new_id = cur.lastrowid
        conn.close()
        print(f"✓ Record #{new_id} disimpan ke database.", flush=True)
        return new_id
    except Exception as e:
        print(f"✗ DB Error: {e}", flush=True)
        return 0


def update_summary_in_db(db_id: int, ringkasan: str):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            conn.cursor().execute(
                "UPDATE notulensi_hasil SET ringkasan = %s WHERE id = %s",
                (ringkasan, db_id)
            )
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"✗ Update DB Error: {e}", flush=True)


# ── Main ─────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Summarize Existing Transcript")
    print("=" * 60)

    # 1. Cek file
    if not os.path.isfile(TARGET_FILE):
        print(f"✗ File tidak ditemukan: {TARGET_FILE}")
        sys.exit(1)

    txt_filename = os.path.basename(TARGET_FILE)
    print(f"  File     : {txt_filename}")
    print(f"  Judul    : {JUDUL_RAPAT}")
    print()

    # 2. Baca isi transkrip
    print("[1/4] Membaca isi transkrip...")
    full_text = read_transcript(TARGET_FILE)
    if len(full_text.strip()) < 50:
        print("✗ Teks transkrip terlalu pendek atau kosong.")
        sys.exit(1)
    print(f"      → {len(full_text)} karakter terbaca.")

    # 3. Simpan record awal ke DB
    print("[2/4] Menyimpan record awal ke database...")
    db_id = save_to_db(
        judul    = JUDUL_RAPAT,
        tipe     = 'Live',
        txt_path = txt_filename,
        ringkasan= '[PROSES_SUMMARIZE]',
    )
    if db_id == 0:
        print("✗ Gagal menyimpan ke database. Cek koneksi MySQL / Laragon.")
        sys.exit(1)

    # 4. LexRank + Ollama summarization
    print("[3/4] Menjalankan LexRank pipeline (bisa butuh beberapa menit jika Ollama aktif)...")
    cfg        = SummaryConfig()
    summarizer = LexRankSummarizer(cfg)
    ringkasan  = summarizer.summarize(full_text)

    if not ringkasan:
        ringkasan = "Tidak ada ringkasan yang dihasilkan."

    print(f"      → Ringkasan: {len(ringkasan)} karakter")

    # 5. Simpan file ringkasan
    ts_now       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sum_filename = f"ringkasan_live_{ts_now}.txt"
    sum_path     = os.path.join(HASIL_SUMMARIZE_DIR, sum_filename)
    with open(sum_path, "w", encoding="utf-8") as sf:
        sf.write("=== RINGKASAN RAPAT (LIVE — LexRank) ===\n")
        sf.write(f"Sumber    : {txt_filename}\n")
        sf.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        sf.write(f"{'=' * 40}\n\n")
        sf.write(ringkasan)
    print(f"      → Disimpan: {sum_filename}")

    # 6. Update ringkasan ke DB
    print("[4/4] Mengupdate ringkasan ke database...")
    update_summary_in_db(db_id, ringkasan)

    print()
    print("=" * 60)
    print(f"  ✓ SELESAI! Record DB ID: #{db_id}")
    print(f"  Buka http://localhost/notulensi_rapat/report.php")
    print(f"  untuk melihat hasilnya.")
    print("=" * 60)
    print()
    print("─── PREVIEW RINGKASAN ───")
    print(ringkasan[:800] + ("..." if len(ringkasan) > 800 else ""))


if __name__ == "__main__":
    main()
