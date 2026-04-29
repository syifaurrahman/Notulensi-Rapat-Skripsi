"""
test_lexrank.py — Tes cepat LexRank dengan file transkripsi rapat1jam
Jalankan dari folder whispertranscription:
  python test_lexrank.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from summarize.lexrank import LexRankSummarizer
from summarize.config import SummaryConfig

TRANSKRIP_FILE = os.path.join(
    os.path.dirname(__file__),
    "hasil",
    "transkrip_rapat1jam_20260304_001010.txt"
)

def main():
    # Baca file transkripsi
    with open(TRANSKRIP_FILE, "r", encoding="utf-8") as f:
        raw = f.read()

    # Ambil hanya bagian teks (skip header)
    lines = raw.split("\n")
    content_lines = []
    header_done = False
    for line in lines:
        if "====" in line and header_done:
            content_lines.append(line)
        elif "====" in line:
            header_done = True
        elif header_done:
            content_lines.append(line)
    text = " ".join(content_lines).strip()

    print(f"📄 Total karakter teks: {len(text):,}")
    print(f"📄 Total kata: {len(text.split()):,}")
    print()

    # Test dengan Dynamic Adaptation
    cfg = SummaryConfig()
    summarizer = LexRankSummarizer(cfg)
    result = summarizer.summarize(text)

    print("=" * 60)
    print("🔹 RINGKASAN (Dynamic Sizing):")
    print("=" * 60)
    print(result)
    print()
    kalimat = [s for s in result.split("\n\n") if s.strip()]
    print(f"[{len(kalimat)} paragraf dihasilkan]")
    print()

if __name__ == "__main__":
    main()
