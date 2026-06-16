import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='notulensi', charset='utf8mb4')

print("=== Cari record Digital Marketing ===")
with conn.cursor() as cur:
    cur.execute(
        "SELECT id, judul_rapat, transkrip_txt, LEFT(ringkasan,80), created_at "
        "FROM notulensi_hasil "
        "WHERE transkrip_txt LIKE %s "
        "   OR judul_rapat LIKE %s "
        "ORDER BY id DESC LIMIT 10",
        ('%Digital%', '%Digital%')
    )
    rows = cur.fetchall()
    if rows:
        for r in rows:
            print(f"ID={r[0]} | Judul={r[1]} | transkrip_txt={r[2]} | created={r[4]}")
            print(f"  Ringkasan: {r[3]}")
    else:
        print("Tidak ditemukan dengan 'Digital' — cek semua record terbaru:")
        cur.execute(
            "SELECT id, judul_rapat, transkrip_txt, created_at "
            "FROM notulensi_hasil ORDER BY id DESC LIMIT 10"
        )
        for r in cur.fetchall():
            print(f"ID={r[0]} | Judul={r[1]} | transkrip_txt={r[2]} | created={r[3]}")

conn.close()
