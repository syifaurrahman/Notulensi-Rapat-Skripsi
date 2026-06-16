"""
hitung_akurasi_lexrank_only_new.py
===================================
1. Meringkas transkrip menggunakan LexRank Only (Extractive, tanpa LLM/Ollama).
2. Menghitung ROUGE score terhadap summarize_manual.txt.
3. Menyimpan hasil pengujian ke akurasi/Lexrank only new akurasi.txt.
"""

import os
import re
import sys
import io
from datetime import datetime

# Fix encoding terminal Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

# Path setup untuk import modul whispertranscription
sys.path.append(PARENT_DIR)

from whispertranscription.summarize.lexrank import LexRankSummarizer
from whispertranscription.summarize.config import SummaryConfig

# File input
TRANSKRIP_FILE = os.path.join(PARENT_DIR, "hasil", "transkrip_Zoom Meeting   Psikologi Sosial I C 2022 02 23 13 15 57_20260610_222920.txt")
MANUAL_FILE     = os.path.join(PARENT_DIR, "hasil_summarize", "summarize_manual.txt")

# File output
OUTPUT_FILE     = os.path.join(BASE_DIR, "Lexrank only new akurasi.txt")

def read_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        return f.read()

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[\*\-\d]+[\.\)]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[.,!?;:()\[\]{}\-—–/\\|<>@#$%^&*+=~`"\']', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_ngrams(tokens: list, n: int) -> dict:
    ngrams = {}
    for i in range(len(tokens) - n + 1):
        gram = tuple(tokens[i:i+n])
        ngrams[gram] = ngrams.get(gram, 0) + 1
    return ngrams

def rouge_n(reference: str, hypothesis: str, n: int) -> dict:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    ref_ngrams = get_ngrams(ref_tokens, n)
    hyp_ngrams = get_ngrams(hyp_tokens, n)
    ref_count = sum(ref_ngrams.values())
    hyp_count = sum(hyp_ngrams.values())

    overlap = 0
    for gram, count in hyp_ngrams.items():
        overlap += min(count, ref_ngrams.get(gram, 0))

    precision = overlap / hyp_count if hyp_count > 0 else 0.0
    recall    = overlap / ref_count if ref_count > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "fmeasure": f1}

def lcs_length(x: list, y: list) -> int:
    m, n = len(x), len(y)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i-1] == y[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(curr[j-1], prev[j])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]

def rouge_l(reference: str, hypothesis: str) -> dict:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    lcs = lcs_length(ref_tokens, hyp_tokens)
    precision = lcs / len(hyp_tokens) if hyp_tokens else 0.0
    recall    = lcs / len(ref_tokens)  if ref_tokens  else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "fmeasure": f1}

def hitung_dengan_library(reference: str, hypothesis: str):
    try:
        from rouge_score import rouge_scorer
        scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=False
        )
        scores = scorer.score(reference, hypothesis)
        return {
            "rouge1": {
                "precision": scores['rouge1'].precision,
                "recall":    scores['rouge1'].recall,
                "fmeasure":  scores['rouge1'].fmeasure,
            },
            "rouge2": {
                "precision": scores['rouge2'].precision,
                "recall":    scores['rouge2'].recall,
                "fmeasure":  scores['rouge2'].fmeasure,
            },
            "rougeL": {
                "precision": scores['rougeL'].precision,
                "recall":    scores['rougeL'].recall,
                "fmeasure":  scores['rougeL'].fmeasure,
            },
            "metode": "rouge-score (library)"
        }
    except ImportError:
        return None

def grade_rouge(val: float) -> str:
    pct = val * 100
    if pct >= 50:   return "Sangat Baik"
    if pct >= 30:   return "Baik"
    if pct >= 15:   return "Cukup"
    return "Perlu Peningkatan"

def main():
    print("\n[Notulensia] Memuat transkrip Psikologi Sosial...")
    try:
        transkrip_raw = read_file(TRANSKRIP_FILE)
        manual_raw    = read_file(MANUAL_FILE)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Ambil isi transkrip (skip header jika ada)
    if "========" in transkrip_raw:
        parts = transkrip_raw.split("========\n")
        if len(parts) > 1:
            transkrip_text = parts[-1].strip()
        else:
            transkrip_text = transkrip_raw.strip()
    else:
        transkrip_text = transkrip_raw.strip()

    print(f"  Panjang transkrip: {len(transkrip_text):,} karakter ({len(transkrip_text.split()):,} kata)")

    # 1. Summarize menggunakan LexRank Only
    print("\n[Notulensia] Meringkas menggunakan LexRank Only (Ollama dimatikan)...")
    cfg = SummaryConfig()
    summarizer = LexRankSummarizer(cfg)
    # Paksa Ollama offline agar menggunakan extractive LexRank murni
    summarizer.ollama.is_available = lambda: False

    summary_result = summarizer.summarize(transkrip_text)
    
    # Simpan hasil ringkasan lexrank murni jika ingin dilihat
    temp_summary_path = os.path.join(PARENT_DIR, "hasil_summarize", "temp_lexrank_only_psikologi.txt")
    with open(temp_summary_path, "w", encoding="utf-8") as f:
        f.write(summary_result)
    print(f"  ✓ Ringkasan LexRank Only disimpan sementara ke: {temp_summary_path}")

    # 2. Hitung akurasi ROUGE terhadap ringkasan manual
    print("\n[Notulensia] Menghitung akurasi ROUGE terhadap summarize_manual.txt...")
    sistem_norm = normalize(summary_result)
    manual_norm = normalize(manual_raw)

    print(f"  Sistem (LexRank Only): {len(sistem_norm.split()):,} kata")
    print(f"  Referensi (Manual)   : {len(manual_norm.split()):,} kata")

    lib_result = hitung_dengan_library(manual_norm, sistem_norm)
    if lib_result:
        metode = lib_result["metode"]
        r1 = lib_result["rouge1"]
        r2 = lib_result["rouge2"]
        rl = lib_result["rougeL"]
    else:
        metode = "ROUGE Manual (N-gram + LCS)"
        r1 = rouge_n(manual_norm, sistem_norm, 1)
        r2 = rouge_n(manual_norm, sistem_norm, 2)
        rl = rouge_l(manual_norm, sistem_norm)

    # Cetak & simpan hasil
    timestamp = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    lines = [
        "=" * 62,
        "  HASIL PENGUJIAN AKURASI SUMMARIZATION (LEXRANK ONLY)",
        "  Sistem Notulensia — LexRank Only (Extractive)",
        "=" * 62,
        f"  Tanggal      : {timestamp}",
        f"  Metode       : {metode}",
        f"  File Sistem  : LexRank Only (temp_lexrank_only_psikologi.txt)",
        f"  File Ref     : summarize_manual.txt",
        f"  Kata Sistem  : {len(sistem_norm.split()):,}",
        f"  Kata Ref     : {len(manual_norm.split()):,}",
        "-" * 62,
        "",
        "  METRIK ROUGE (F1 Score)",
        "  ──────────────────────────────────────────────────",
        f"  ROUGE-1  (unigram)    : {r1['fmeasure']*100:6.2f}%   "
            f"[P: {r1['precision']*100:.2f}%  R: {r1['recall']*100:.2f}%]",
        f"  ROUGE-2  (bigram)     : {r2['fmeasure']*100:6.2f}%   "
            f"[P: {r2['precision']*100:.2f}%  R: {r2['recall']*100:.2f}%]",
        f"  ROUGE-L  (LCS)        : {rl['fmeasure']*100:6.2f}%   "
            f"[P: {rl['precision']*100:.2f}%  R: {rl['recall']*100:.2f}%]",
        "",
        "  PENILAIAN",
        "  ──────────────────────────────────────────────────",
        f"  ROUGE-1 : {grade_rouge(r1['fmeasure'])}",
        f"  ROUGE-2 : {grade_rouge(r2['fmeasure'])}",
        f"  ROUGE-L : {grade_rouge(rl['fmeasure'])}",
        "",
        "=" * 62,
        "  CATATAN:",
        "  - ROUGE-1 mengukur kecocokan kata tunggal (unigram)",
        "  - ROUGE-2 mengukur kecocokan 2 kata berurutan (bigram)",
        "  - ROUGE-L mengukur urutan kata terpanjang yang cocok",
        "  - F1 = harmonic mean antara Precision dan Recall",
        "  - Nilai ideal untuk Bahasa Indonesia: ROUGE-L > 30%",
        "  - P (Precision): seberapa relevan ringkasan sistem",
        "  - R (Recall)   : seberapa lengkap isi referensi tercakup",
        "=" * 62,
    ]

    output = "\n".join(lines)
    print(output)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output + "\n")

    print(f"\n  >> Hasil disimpan ke: {OUTPUT_FILE}")

    # Hapus file temp ringkasan agar folder bersih
    try:
        if os.path.exists(temp_summary_path):
            os.remove(temp_summary_path)
    except:
        pass

if __name__ == "__main__":
    main()
