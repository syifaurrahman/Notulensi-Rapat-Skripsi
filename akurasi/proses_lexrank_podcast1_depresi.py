# proses_lexrank_podcast1_depresi.py
# ================================================================================================
# Proses ringkasan transkrip podcast _1.txt menggunakan LexRank saja (tanpa LLM)
# Cara pakai:
#     python akurasi/proses_lexrank_podcast1_depresi.py
# ================================================================================================

import os
import sys
import re

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
    return text

def main():
    transkrip_path = os.path.join(PARENT_DIR, "hasil", "podcast _1.txt")
    output_dir = os.path.join(PARENT_DIR, "hasil_summarize", "lexrank")
    output_path = os.path.join(output_dir, "podcast1_depresi.txt")
    
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
    # Atur min/max kalimat agar proporsional
    cfg.min_sentences = 8
    cfg.max_sentences = 25
    cfg.compression_ratio = 0.20
    
    summarizer = LexRankSummarizer(cfg)
    
    # ── JALANKAN PIPELINE LEXRANK MURNI (Lewati Ollama LLM) ──
    # Step 1: Text Cleaning
    cleaned = summarizer._step1_text_cleaning(text)
    
    # Step 2: Sentence Segmentation
    raw_sentences = summarizer._step2_sentence_segmentation(cleaned)
    
    # Step 3: Sentence Filtering
    filtered = summarizer._step3_sentence_filtering(raw_sentences)
    if not filtered:
        raw_sentences.sort(key=len, reverse=True)
        target = max(summarizer.cfg.min_sentences, min(8, len(raw_sentences)))
        filtered = raw_sentences[:target]

    # Target kalimat dinamis
    target_sentences = int(len(filtered) * summarizer.cfg.compression_ratio)
    target_sentences = max(summarizer.cfg.min_sentences, min(target_sentences, summarizer.cfg.max_sentences))

    # Step 4 & 5: Key Point Extraction & Reorganization
    if len(filtered) <= target_sentences:
        organized = filtered
    else:
        top_sentences, top_indices = summarizer._step4_lexrank_extraction(filtered, target=target_sentences)
        organized = summarizer._step5_reorganize(top_sentences, top_indices, len(filtered))

    # Step 6: Final Format (Tanpa memanggil Ollama)
    ringkasan_lexrank = summarizer._step6_final_format(organized)

    # Simpan hasil ke hasil_summarize/lexrank/podcast1_depresi.txt
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        # Tulis header informasi agar rapi
        f.write("=== HASIL LEXRANK EXTRACTIVE ===\n")
        f.write(f"Sumber    : podcast _1.txt\n")
        f.write(f"Model     : Whisper small\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(ringkasan_lexrank + "\n")
        
    print(f"[SUCCESS] Hasil ringkasan LexRank disimpan ke: {output_path}")
    print(f"          Jumlah kata ringkasan: {len(ringkasan_lexrank.split())} kata.")

if __name__ == "__main__":
    main()
