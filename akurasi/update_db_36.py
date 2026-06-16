import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pymysql

# Baca ringkasan baru
RINGKASAN_FILE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "whispertranscription", "summarize", "hasil_summarize",
    "ringkasan_digital_marketing_reprocess_20260610_220630.txt"
))

with open(RINGKASAN_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Strip header file .txt
separator = "=" * 40
idx = content.find(separator)
ringkasan = content[idx + len(separator):].lstrip("\r\n").strip() if idx != -1 else content.strip()

# Bersihkan kalimat pembuka "adalah notulensi rapat berdasarkan..."
import re
ringkasan = re.sub(
    r'^(adalah notulensi[^:\n]*|notulensi rapat[^:\n]*|berdasarkan transkrip[^:\n]*)[:\s\n]*',
    '', ringkasan, flags=re.IGNORECASE
).strip()

print(f"Ringkasan siap: {len(ringkasan):,} karakter")
print(f"Preview: {ringkasan[:120]}...")

# Update DB
conn = pymysql.connect(host='localhost', user='root', password='', database='notulensi', charset='utf8mb4')
with conn.cursor() as cur:
    cur.execute("UPDATE notulensi_hasil SET ringkasan = %s WHERE id = %s", (ringkasan, 36))
    conn.commit()
    print(f"\n[OK] Record ID=36 berhasil diupdate di database!")
    print("     Cek di halaman Report sekarang.")

# Juga simpan file ringkasan ke folder hasil_summarize web
PROJECT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HASIL_WEB   = os.path.join(PROJECT_DIR, "hasil_summarize")
os.makedirs(HASIL_WEB, exist_ok=True)
out_file = os.path.join(HASIL_WEB,
    "transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture"
    " - PENS SKY Venture 1080p h264_2_20260610_214445.txt"
)
with open(out_file, "w", encoding="utf-8") as f:
    f.write(ringkasan)
print(f"[OK] File ringkasan disalin ke:\n     {out_file}")

conn.close()
