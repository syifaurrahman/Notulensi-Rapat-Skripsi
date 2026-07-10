# hitung_akurasi_live_podcast2_genZ_ollama.py
# ==============================================================================
# Menghitung ketepatan ringkasan (ROUGE Score) antara:
#   - Ringkasan Ollama (hasil_summarize/live_podcast2_genz_pilih_tidak_nikah.txt)
#   - Ringkasan LexRank (hasil_summarize/lexrank/podcast2_genZ.txt)
#
# Metrik:
#   - ROUGE-1 (unigram F1, Precision, Recall)
#   - ROUGE-2 (bigram F1, Precision, Recall)
#   - ROUGE-L (LCS F1, Precision, Recall)
#
# Output: akurasi/ollama/live_podcast2_genZ_ollama.txt
# ==============================================================================

import os
import re
import sys
import io
from datetime import datetime

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── PATH FILE ────────────────────────────────────────────────────────────────
BASE_DIR        = r"c:\laragon\www\notulensi_rapat"
SISTEM_FILE     = os.path.join(BASE_DIR, "hasil_summarize", "live_podcast2_genz_pilih_tidak_nikah.txt")
MANUAL_FILE     = os.path.join(BASE_DIR, "hasil_summarize", "lexrank", "podcast2_genZ.txt")
OUTPUT_FILE     = os.path.join(BASE_DIR, "akurasi", "ollama", "live_podcast2_genZ_ollama.txt")

HEADER_MARKER   = "========================================"

# ─── BACA & NORMALISASI TEKS ──────────────────────────────────────────────────

def read_file(filepath: str, skip_header: bool = False) -> str:
    """Baca file teks, opsional skip header sistem."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")

    with open(filepath, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    if skip_header:
        content = []
        skip = True
        for line in lines:
            if skip:
                if HEADER_MARKER in line:
                    skip = False
                continue
            content.append(line)
        return " ".join(content)
    else:
        return " ".join(lines)

def normalize(text: str) -> str:
    """Normalisasi teks untuk ROUGE (lowercase, hapus markdown dan tanda baca)."""
    text = text.lower()
    # Hapus markdown bold/italic
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    # Hapus heading markdown
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Hapus bullet/numbering
    text = re.sub(r'^\s*[\*\-\d]+[\.\)]\s*', '', text, flags=re.MULTILINE)
    # Hapus tanda baca
    text = re.sub(r'[.,!?;:()\[\]{}\-—–/\\|<>@#$%^&*+=~`"\']', ' ', text)
    # Hapus baris kosong / newline
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ─── ROUGE MANUAL FALLBACK ───────────────────────────────────────────────────

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

# ─── RUN LIBRARY IF AVAILABLE ────────────────────────────────────────────────

def hitung_dengan_library(reference: str, hypothesis: str):
    try:
        from rouge_score import rouge_scorer
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
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
    if pct >= 50:   return "Sangat Baik ✓✓"
    if pct >= 30:   return "Baik ✓"
    if pct >= 15:   return "Cukup ~"
    return "Perlu Peningkatan ✗"

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("Memproses evaluasi ROUGE...")
    
    try:
        sistem_raw = read_file(SISTEM_FILE, skip_header=True)
        manual_raw = read_file(MANUAL_FILE, skip_header=True)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    sistem_norm = normalize(sistem_raw)
    manual_norm = normalize(manual_raw)

    ref_words = len(manual_norm.split())
    hyp_words = len(sistem_norm.split())

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

    timestamp = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    
    sep  = "=" * 62
    sep2 = "-" * 62
    lines = [
        sep,
        "  HASIL PENGUJIAN AKURASI SUMMARIZATION",
        "  Sistem Notulensia — LLM (Ollama / Llama 3.2)",
        "  Topik: Live Podcast Gen Z",
        sep,
        f"  Tanggal      : {timestamp}",
        f"  Metode       : {metode}",
        f"  File Sistem  : hasil_summarize/live_podcast2_genz_pilih_tidak_nikah.txt",
        f"  File Ref     : hasil_summarize/lexrank/podcast2_genZ.txt",
        f"  Kata Sistem  : {hyp_words:,}",
        f"  Kata Ref     : {ref_words:,}",
        sep2,
        "",
        "  METRIK ROUGE (F1 Score)",
        "  ──────────────────────────────────────────────────",
        f"  ROUGE-1  (unigram)    : {r1['fmeasure']*100:6.2f}%   [P: {r1['precision']*100:.2f}%  R: {r1['recall']*100:.2f}%]",
        f"  ROUGE-2  (bigram)     : {r2['fmeasure']*100:6.2f}%   [P: {r2['precision']*100:.2f}%  R: {r2['recall']*100:.2f}%]",
        f"  ROUGE-L  (LCS)        : {rl['fmeasure']*100:6.2f}%   [P: {rl['precision']*100:.2f}%  R: {rl['recall']*100:.2f}%]",
        "",
        "  PENILAIAN",
        "  ──────────────────────────────────────────────────",
        f"  ROUGE-1 : {grade_rouge(r1['fmeasure'])}",
        f"  ROUGE-2 : {grade_rouge(r2['fmeasure'])}",
        f"  ROUGE-L : {grade_rouge(rl['fmeasure'])}",
        "",
        sep,
        "  CATATAN:",
        "  - ROUGE-1 mengukur kecocokan kata tunggal (unigram)",
        "  - ROUGE-2 mengukur kecocokan 2 kata berurutan (bigram)",
        "  - ROUGE-L mengukur urutan kata terpanjang yang cocok",
        "  - F1 = harmonic mean antara Precision dan Recall",
        "  - Nilai ideal untuk Bahasa Indonesia: ROUGE-L > 30%",
        "  - P (Precision): seberapa relevan ringkasan sistem",
        "  - R (Recall)   : seberapa lengkap isi referensi tercakup",
        sep,
    ]

    output_text = "\n".join(lines)
    print("\n" + output_text)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output_text + "\n")

    print(f"\nHasil disimpan ke: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
