"""
test_pipeline.py — Test 6-Step LexRank Pipeline
================================================
Jalankan: python test_pipeline.py
"""
import sys
import os
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from summarize.lexrank import LexRankSummarizer
from summarize.config import SummaryConfig

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASIL_SUMMARIZE_DIR = os.path.join(BASE_DIR, "hasil_summarize")
os.makedirs(HASIL_SUMMARIZE_DIR, exist_ok=True)

def main():
    # Baca file transkrip
    txt_path = os.path.join(BASE_DIR, "hasil", "transkrip_rapat1jam_20260304_002928.txt")

    if not os.path.isfile(txt_path):
        print(f"[ERROR] File tidak ditemukan: {txt_path}")
        return

    with open(txt_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Ambil hanya konten (skip header)
    if "========" in raw:
        parts = raw.split("=" * 40)
        if len(parts) > 1:
            raw = parts[-1].strip()

    print(f"[INFO] Panjang teks: {len(raw):,} karakter")
    print(f"[INFO] Jumlah kata : {len(raw.split()):,} kata")
    print("=" * 60)

    # Jalankan summarizer
    cfg = SummaryConfig()
    summarizer = LexRankSummarizer(cfg)
    result = summarizer.summarize(raw)

    print("\n📋 HASIL RINGKASAN (6-Step Pipeline):")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print(f"\n[INFO] Panjang ringkasan: {len(result):,} karakter")
    print(f"[INFO] Jumlah kata     : {len(result.split()):,} kata")
    print(f"[INFO] Rasio kompresi  : {len(result)/len(raw)*100:.1f}%")

    # Simpan ke hasil_summarize
    txt_filename = os.path.basename(txt_path)
    sum_filename = txt_filename.replace("transkrip_", "ringkasan_")
    sum_path = os.path.join(HASIL_SUMMARIZE_DIR, sum_filename)

    with open(sum_path, "w", encoding="utf-8") as sf:
        sf.write("=== RINGKASAN RAPAT (LexRank 6-Step) ===\n")
        sf.write(f"Sumber    : {txt_filename}\n")
        sf.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        sf.write(f"Model     : Whisper small\n")
        sf.write(f"{'=' * 40}\n\n")
        sf.write(result)

    print(f"\n[INFO] ✓ Ringkasan disimpan: {sum_path}")

if __name__ == "__main__":
    main()
