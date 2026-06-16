"""
reprocess_transkrip.py
======================
Script one-shot: baca transkrip .txt yang sudah ada ->
strip header -> proses LexRank + Ollama -> simpan ringkasan.

Tidak mengubah alur pipeline utama (server.py / upload_server.py).
Setelah selesai, script ini bisa dihapus tanpa efek apapun.
"""

import sys
import os
import datetime

# Atur encoding output agar tidak error di Windows terminal
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────
#  Path setup: tambahkan whispertranscription ke PYTHONPATH
# ─────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
WHISPER_DIR = os.path.join(PROJECT_DIR, "whispertranscription")

if WHISPER_DIR not in sys.path:
    sys.path.insert(0, WHISPER_DIR)

# ─────────────────────────────────────────────────────────────
#  Import LexRank Summarizer dari pipeline yang sudah ada
# ─────────────────────────────────────────────────────────────
from summarize.lexrank import LexRankSummarizer
from summarize.config  import SummaryConfig

# ─────────────────────────────────────────────────────────────
#  File transkrip yang akan diproses ulang
# ─────────────────────────────────────────────────────────────
TRANSKRIP_FILE = os.path.join(
    PROJECT_DIR, "hasil",
    "transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture"
    " - PENS SKY Venture 1080p h264_2_20260610_214445.txt"
)

OUTPUT_DIR = os.path.join(WHISPER_DIR, "summarize", "hasil_summarize")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_transcript_strip_header(filepath: str) -> str:
    """
    Baca file transkrip, buang header:
    === TRANSKRIPSI RAPAT ===
    File Video  : ...
    Dibuat      : ...
    Model       : ...
    ========================================
    [teks transkrip mulai dari sini]
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    separator = "=" * 40
    idx = content.find(separator)
    if idx != -1:
        after_sep = content[idx + len(separator):]
        teks = after_sep.lstrip("\r\n").strip()
        return teks
    else:
        return content.strip()


def main():
    print("=" * 60)
    print("  REPROCESS TRANSKRIP -> LEXRANK + OLLAMA")
    print("=" * 60)

    # 1. Baca transkrip
    if not os.path.isfile(TRANSKRIP_FILE):
        print(f"[ERROR] File tidak ditemukan:\n  {TRANSKRIP_FILE}")
        sys.exit(1)

    print("\n[1] Membaca transkrip...")
    teks = read_transcript_strip_header(TRANSKRIP_FILE)
    word_count = len(teks.split())
    print(f"    [OK] {len(teks):,} karakter | {word_count:,} kata")

    if len(teks) < 50:
        print("[ERROR] Teks terlalu pendek setelah strip header.")
        sys.exit(1)

    # 2. Init LexRank Summarizer
    print("\n[2] Inisialisasi LexRank Summarizer...")
    cfg        = SummaryConfig()
    summarizer = LexRankSummarizer(cfg)

    print(f"    compression_ratio : {cfg.compression_ratio}")
    print(f"    max_sentences     : {cfg.max_sentences}")
    print(f"    min_sentences     : {cfg.min_sentences}")
    print(f"    ollama_model      : {cfg.ollama_model}")

    # 3. Cek Ollama
    is_ollama = summarizer.ollama.is_available()
    status    = "[OK] Online" if is_ollama else "[X] Offline (LexRank saja)"
    print(f"\n[3] Ollama status: {status}")

    # 4. Jalankan summarization
    print("\n[4] Memulai LexRank 6-Step Pipeline...")
    print("    (Ini mungkin memakan beberapa menit)")
    print("-" * 60)

    result = summarizer.summarize_with_debug(teks)

    ringkasan        = result['ringkasan']
    ranked_sentences = result.get('ranked_sentences', [])

    print("-" * 60)
    print(f"    [OK] Selesai. {len(ranked_sentences)} kalimat di-ranking.")
    print(f"    [OK] Ringkasan: {len(ringkasan):,} karakter")

    # 5. Simpan ringkasan
    ts           = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_filename = f"ringkasan_digital_marketing_reprocess_{ts}.txt"
    out_path     = os.path.join(OUTPUT_DIR, out_filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=== RINGKASAN RAPAT (Reprocess - LexRank + Ollama) ===\n")
        f.write(f"Sumber    : {os.path.basename(TRANSKRIP_FILE)}\n")
        f.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Ollama    : {'Online - ' + cfg.ollama_model if is_ollama else 'Offline - LexRank saja'}\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(ringkasan)

    print(f"\n[5] [OK] Ringkasan disimpan ke:")
    print(f"    {out_path}")

    # 6. Preview ringkasan
    print(f"\n{'=' * 60}")
    print("  PREVIEW RINGKASAN:")
    print(f"{'=' * 60}")
    preview = ringkasan[:2000]
    try:
        print(preview)
    except UnicodeEncodeError:
        print(preview.encode('ascii', errors='replace').decode('ascii'))

    if len(ringkasan) > 2000:
        print(f"\n... [+{len(ringkasan)-2000} karakter tersisa, lihat file output]")

    # 7. Top 5 kalimat LexRank
    if ranked_sentences:
        print(f"\n{'-' * 60}")
        print("  TOP 5 KALIMAT (LexRank Scoring):")
        print(f"{'-' * 60}")
        for item in ranked_sentences[:5]:
            score   = item.get('score', 0)
            sent    = item.get('sentence', '')
            rank    = item.get('rank', '?')
            preview = sent[:100] + ('...' if len(sent) > 100 else '')
            try:
                print(f"  #{rank}  [{score:.4f}]  {preview}")
            except UnicodeEncodeError:
                print(f"  #{rank}  [{score:.4f}]  [kalimat mengandung karakter khusus]")

    print(f"\n{'=' * 60}")
    print("  SELESAI")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
