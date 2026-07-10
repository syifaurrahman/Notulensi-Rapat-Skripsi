# proses_lexrank_podcast2_genZ.py
# ================================================================================================
# Proses ringkasan transkrip live_Podcast2_genZ.txt menggunakan LexRank saja (tanpa LLM)
# Cara pakai:
#     python akurasi/proses_lexrank_podcast2_genZ.py
# ================================================================================================

import os
import sys
import re
from datetime import datetime

# Tambahkan root directory ke sys.path agar bisa import modul whispertranscription
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PARENT_DIR)

from whispertranscription.summarize.lexrank import LexRankSummarizer
from whispertranscription.summarize.config import SummaryConfig

def clean_hallucinations(text):
    # Hapus prompt leak di akhir jika ada
    text = re.sub(r"pertahankan kata-kata inggris apa adanya, jangan diterjemahkan\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"pertahankan kata kata inggris apa adanya jangan diterjemahkan\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"pertahankan kata-kata inggris apa adanya jangan diterjemahkan\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"pertahankan kata kata inggris apa adanya, jangan diterjemahkan\.?", "", text, flags=re.IGNORECASE)
    return text

def main():
    transkrip_path = os.path.join(PARENT_DIR, "hasil", "live_Podcast2_genZ.txt")
    output_dir = os.path.join(PARENT_DIR, "hasil_summarize", "lexrank")
    output_path = os.path.join(output_dir, "podcast2_genZ.txt")
    
    if not os.path.exists(transkrip_path):
        print(f"[ERROR] File transkrip tidak ditemukan: {transkrip_path}")
        sys.exit(1)

    print(f"[Notulensia] Membaca file: {transkrip_path}")
    with open(transkrip_path, "r", encoding="utf-8", errors="ignore") as f:
        content_lines = f.readlines()

    # Skip header transkrip Whisper
    header_ended = False
    clean_text_lines = []
    for line in content_lines:
        if header_ended:
            clean_text_lines.append(line)
        elif "========================================" in line:
            header_ended = True
            
    text = " ".join(clean_text_lines).strip()
    text = clean_hallucinations(text)
    if not text:
        print("[ERROR] Teks transkrip kosong setelah membuang header.")
        sys.exit(1)

    print(f"[Notulensia] Panjang teks transkrip: {len(text.split())} kata.")
    print("[Notulensia] Memproses dengan LexRank Summarizer (Hanya Extractive)...")

    # Inisialisasi LexRank
    cfg = SummaryConfig()
    cfg.min_sentences = 8
    cfg.max_sentences = 25
    cfg.compression_ratio = 0.20
    
    summarizer = LexRankSummarizer(cfg)
    
    # ── JALANKAN PIPELINE LEXRANK MURNI ──
    cleaned = summarizer._step1_text_cleaning(text)
    raw_sentences = summarizer._step2_sentence_segmentation(cleaned)
    filtered = summarizer._step3_sentence_filtering(raw_sentences)
    if not filtered:
        raw_sentences.sort(key=len, reverse=True)
        target = max(summarizer.cfg.min_sentences, min(8, len(raw_sentences)))
        filtered = raw_sentences[:target]

    target_sentences = int(len(filtered) * summarizer.cfg.compression_ratio)
    target_sentences = max(summarizer.cfg.min_sentences, min(target_sentences, summarizer.cfg.max_sentences))

    if len(filtered) <= target_sentences:
        organized = filtered
    else:
        top_sentences, top_indices = summarizer._step4_lexrank_extraction(filtered, target=target_sentences)
        organized = summarizer._step5_reorganize(top_sentences, top_indices, len(filtered))

    ringkasan_lexrank = summarizer._step6_final_format(organized)

    # Simpan hasil ke hasil_summarize/lexrank/podcast2_genZ.txt
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== HASIL LEXRANK EXTRACTIVE (LIVE) ===\n")
        f.write(f"Sumber    : live_Podcast2_genZ.txt\n")
        f.write(f"Dibuat    : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Model     : Whisper small\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(ringkasan_lexrank + "\n")
        
    print(f"[SUCCESS] Hasil ringkasan LexRank disimpan ke: {output_path}")
    print(f"          Jumlah kata ringkasan: {len(ringkasan_lexrank.split())} kata.")

if __name__ == "__main__":
    main()
