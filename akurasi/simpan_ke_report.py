"""
simpan_ke_report.py
===================
Simpan ringkasan reprocess ke database notulensi (tabel notulensi_hasil).
Script one-shot, tidak mengubah pipeline utama.
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────
# Konten ringkasan (strip baris header file .txt)
# ─────────────────────────────────────────────────────────────
RINGKASAN_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "whispertranscription", "summarize", "hasil_summarize",
    "ringkasan_digital_marketing_reprocess_20260610_220630.txt"
)
RINGKASAN_FILE = os.path.normpath(RINGKASAN_FILE)

# File transkrip sumber (untuk cari record di DB)
TXT_FILENAME = (
    "transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture"
    " - PENS SKY Venture 1080p h264_2_20260610_214445.txt"
)

# ─────────────────────────────────────────────────────────────
# Baca isi ringkasan (strip header 5 baris pertama)
# ─────────────────────────────────────────────────────────────
def read_ringkasan(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    separator = "=" * 40
    idx = content.find(separator)
    if idx != -1:
        after = content[idx + len(separator):].lstrip("\r\n").strip()
        return after
    return content.strip()

# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  SIMPAN RINGKASAN KE DATABASE REPORT")
    print("=" * 60)

    # 1. Baca ringkasan
    if not os.path.isfile(RINGKASAN_FILE):
        print(f"[ERROR] File ringkasan tidak ditemukan:\n  {RINGKASAN_FILE}")
        sys.exit(1)

    ringkasan = read_ringkasan(RINGKASAN_FILE)
    print(f"\n[1] Ringkasan dibaca: {len(ringkasan):,} karakter")

    # 2. Koneksi DB
    try:
        import pymysql
    except ImportError:
        print("[ERROR] pymysql tidak tersedia. Install: pip install pymysql")
        sys.exit(1)

    DB_CONFIG = {
        'host'    : 'localhost',
        'user'    : 'root',
        'password': '',
        'database': 'notulensi',
        'charset' : 'utf8mb4',
    }

    print("\n[2] Menghubungkan ke database...")
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("    [OK] Terhubung ke database 'notulensi'")
    except Exception as e:
        print(f"    [ERROR] Gagal koneksi: {e}")
        sys.exit(1)

    try:
        with conn.cursor() as cur:
            # 3. Cari record berdasarkan txt_path
            print(f"\n[3] Mencari record untuk file:\n    {TXT_FILENAME}")

            cur.execute(
                "SELECT id, judul_rapat, ringkasan, created_at FROM notulensi_hasil "
                "WHERE txt_path = %s ORDER BY id DESC LIMIT 5",
                (TXT_FILENAME,)
            )
            rows = cur.fetchall()

            if not rows:
                # Coba cari dengan LIKE jika exact match tidak ditemukan
                like_pattern = "%20260610_214445%"
                cur.execute(
                    "SELECT id, judul_rapat, ringkasan, created_at FROM notulensi_hasil "
                    "WHERE txt_path LIKE %s ORDER BY id DESC LIMIT 5",
                    (like_pattern,)
                )
                rows = cur.fetchall()

            if not rows:
                print("    [X] Record tidak ditemukan di database.")
                print("\n    Daftar 5 record terakhir di database:")
                cur.execute(
                    "SELECT id, judul_rapat, txt_path, created_at FROM notulensi_hasil "
                    "ORDER BY id DESC LIMIT 5"
                )
                for r in cur.fetchall():
                    print(f"    ID {r[0]}: {r[1]} | {r[2]} | {r[3]}")
                conn.close()
                sys.exit(1)

            print(f"    [OK] Ditemukan {len(rows)} record:")
            for r in rows:
                ringkasan_preview = (r[2] or '')[:60].replace('\n', ' ')
                print(f"    -> ID {r[0]}: '{r[1]}' | Created: {r[3]}")
                print(f"       Ringkasan saat ini: {ringkasan_preview}...")

            # 4. Ambil ID record terbaru (pertama dari hasil query DESC)
            target_id = rows[0][0]
            print(f"\n[4] Akan update record ID: {target_id}")

            # 5. Simpan juga file ringkasan ke folder hasil_summarize web
            PROJECT_DIR = os.path.normpath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
            )
            HASIL_SUMMARIZE_WEB = os.path.join(PROJECT_DIR, "hasil_summarize")
            os.makedirs(HASIL_SUMMARIZE_WEB, exist_ok=True)

            sum_filename = TXT_FILENAME.replace("transkrip_", "ringkasan_")
            sum_path     = os.path.join(HASIL_SUMMARIZE_WEB, sum_filename)

            with open(sum_path, "w", encoding="utf-8") as f:
                f.write(ringkasan)
            print(f"    [OK] File ringkasan disalin ke:\n    {sum_path}")

            # 6. Update ringkasan di DB
            cur.execute(
                "UPDATE notulensi_hasil SET ringkasan = %s, sum_path = %s WHERE id = %s",
                (ringkasan, sum_filename, target_id)
            )
            conn.commit()

            print(f"\n[5] [OK] Database ID {target_id} berhasil diupdate!")
            print(f"    Karakter ringkasan baru: {len(ringkasan):,}")

    except pymysql.err.OperationalError as e:
        # Kolom sum_path mungkin tidak ada — coba tanpa sum_path
        print(f"    [!] Warning: {e}")
        print("    Mencoba update tanpa kolom sum_path...")
        try:
            with conn.cursor() as cur2:
                cur2.execute(
                    "UPDATE notulensi_hasil SET ringkasan = %s WHERE id = %s",
                    (ringkasan, target_id)
                )
                conn.commit()
            print(f"    [OK] Database ID {target_id} berhasil diupdate (ringkasan saja)!")
        except Exception as e2:
            print(f"    [ERROR] Gagal update: {e2}")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

    print(f"\n{'=' * 60}")
    print("  SELESAI - Cek di halaman Report")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
