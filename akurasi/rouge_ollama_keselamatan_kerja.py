"""
rouge_ollama_keselamatan_kerja.py
===================================
Menghitung ROUGE-L (F1, Precision, Recall) antara:
  - Reference : hasil LexRank extractive
  - Hypothesis: hasil Ollama abstractive
untuk file Zoom BNSP K3 Keselamatan Kerja

Output: akurasi/Ollama/rouge_keselamatan_kerja.txt
"""

import os
import re
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = r"c:\laragon\www\notulensi_rapat"

LEXRANK_FILE = os.path.join(
    BASE_DIR, "hasil_summarize", "Lexrank",
    "lexrank_zoom-bnsp-lsptti-pelatihan-k3-keselamatan-kesehatan-kerja-19-may-2023-break1-13-00-15-45-wib-ytmp4.savetube.vip_20260619_222933.txt"
)

OLLAMA_FILE = os.path.join(
    BASE_DIR, "hasil_summarize", "ollama",
    "ollama_zoom-bnsp-lsptti-pelatihan-k3-keselamatan-kesehatan-kerja-19-may-2023-break1-13-00-15-45-wib-ytmp4.savetube.vip_20260619_222933.txt"
)

OUTPUT_DIR  = os.path.join(BASE_DIR, "akurasi", "Ollama")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rouge_keselamatan_kerja.txt")

HEADER_MARKER = "========================================"


def read_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan:\n  {filepath}")
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    content = []
    skip = True
    for line in lines:
        if skip:
            if HEADER_MARKER in line:
                skip = False
            continue
        content.append(line)
    return " ".join(content)


def normalize(text):
    text = text.lower()
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[\*\-\d]+[\.)\:]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[.,!?;:()\[\]{}\-—–/\\|<>@#$%^&*+=~`"\']', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_ngrams(tokens, n):
    ngrams = {}
    for i in range(len(tokens) - n + 1):
        gram = tuple(tokens[i:i+n])
        ngrams[gram] = ngrams.get(gram, 0) + 1
    return ngrams


def rouge_n(reference, hypothesis, n):
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    ref_ngrams = get_ngrams(ref_tokens, n)
    hyp_ngrams = get_ngrams(hyp_tokens, n)
    ref_count  = sum(ref_ngrams.values())
    hyp_count  = sum(hyp_ngrams.values())
    overlap = sum(min(c, ref_ngrams.get(g, 0)) for g, c in hyp_ngrams.items())
    precision = overlap / hyp_count if hyp_count > 0 else 0.0
    recall    = overlap / ref_count if ref_count  > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "fmeasure": f1}


def lcs_length(x, y):
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


def rouge_l(reference, hypothesis):
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    lcs = lcs_length(ref_tokens, hyp_tokens)
    precision = lcs / len(hyp_tokens) if hyp_tokens else 0.0
    recall    = lcs / len(ref_tokens)  if ref_tokens  else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "fmeasure": f1}


def hitung_dengan_library(reference: str, hypothesis: str):
    try:
        from rouge_score import rouge_scorer  # type: ignore[import-untyped]
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
        scores = scorer.score(reference, hypothesis)
        rouge1: dict[str, float] = {"precision": scores['rouge1'].precision,
                                    "recall":    scores['rouge1'].recall,
                                    "fmeasure":  scores['rouge1'].fmeasure}
        rouge2: dict[str, float] = {"precision": scores['rouge2'].precision,
                                    "recall":    scores['rouge2'].recall,
                                    "fmeasure":  scores['rouge2'].fmeasure}
        rougeL: dict[str, float] = {"precision": scores['rougeL'].precision,
                                    "recall":    scores['rougeL'].recall,
                                    "fmeasure":  scores['rougeL'].fmeasure}
        return {
            "rouge1": rouge1,
            "rouge2": rouge2,
            "rougeL": rougeL,
            "metode": "rouge-score (library)"
        }
    except ImportError:
        return None


def grade(val):
    pct = val * 100
    if pct >= 50: return "Sangat Baik ✓✓"
    if pct >= 30: return "Baik ✓"
    if pct >= 15: return "Cukup ~"
    return "Perlu Peningkatan ✗"


def main():
    now = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    print("=" * 62)
    print("  ROUGE SCORE — Ollama vs LexRank (K3 Keselamatan Kerja)")
    print("=" * 62)

    try:
        ref_raw = read_file(LEXRANK_FILE)
        hyp_raw = read_file(OLLAMA_FILE)
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    ref_norm = normalize(ref_raw)
    hyp_norm = normalize(hyp_raw)

    print(f"  Referensi (LexRank) : {len(ref_norm.split()):,} kata")
    print(f"  Hipotesis (Ollama)  : {len(hyp_norm.split()):,} kata")
    print("  Menghitung ROUGE...", flush=True)

    lib = hitung_dengan_library(ref_norm, hyp_norm)
    if lib:
        metode: str = str(lib["metode"])
        r1: dict[str, float] = dict(lib["rouge1"])  # type: ignore[arg-type]
        r2: dict[str, float] = dict(lib["rouge2"])  # type: ignore[arg-type]
        rl: dict[str, float] = dict(lib["rougeL"])  # type: ignore[arg-type]
    else:
        metode = "ROUGE Manual (N-gram + LCS)"
        r1 = rouge_n(ref_norm, hyp_norm, 1)
        r2 = rouge_n(ref_norm, hyp_norm, 2)
        rl = rouge_l(ref_norm, hyp_norm)

    sep  = "=" * 62
    sep2 = "-" * 62
    lines = []
    lines.append(sep)
    lines.append("  HASIL ROUGE SCORE — OLLAMA ABSTRACTIVE SUMMARIZATION")
    lines.append("  Sistem Notulensi — Zoom BNSP K3 Keselamatan Kerja")
    lines.append("  Pelatihan K3 LSPTTI — 19 Mei 2023")
    lines.append(sep)
    lines.append(f"  Tanggal       : {now}")
    lines.append(f"  Metode        : {metode}")
    lines.append(f"  Referensi     : LexRank Extractive Result")
    lines.append(f"  Hipotesis     : Ollama Abstractive Result")
    lines.append(f"  Kata Referensi: {len(ref_norm.split()):,}")
    lines.append(f"  Kata Hipotesis: {len(hyp_norm.split()):,}")
    lines.append(sep2)
    lines.append("")
    lines.append("  METRIK ROUGE")
    lines.append("  " + "─" * 52)
    lines.append(f"  {'Metrik':<28} {'F1-Score':>10} {'Precision':>10} {'Recall':>10}")
    lines.append("  " + "─" * 52)
    lines.append(f"  {'ROUGE-1 (Unigram)':<28} {r1['fmeasure']*100:>9.2f}% {r1['precision']*100:>9.2f}% {r1['recall']*100:>9.2f}%")
    lines.append(f"  {'ROUGE-2 (Bigram)':<28} {r2['fmeasure']*100:>9.2f}% {r2['precision']*100:>9.2f}% {r2['recall']*100:>9.2f}%")
    lines.append(f"  {'ROUGE-L (LCS)':<28} {rl['fmeasure']*100:>9.2f}% {rl['precision']*100:>9.2f}% {rl['recall']*100:>9.2f}%")
    lines.append("  " + "─" * 52)
    lines.append("")
    lines.append("  PENILAIAN")
    lines.append("  " + "─" * 52)
    lines.append(f"  ROUGE-1 : {grade(r1['fmeasure'])}")
    lines.append(f"  ROUGE-2 : {grade(r2['fmeasure'])}")
    lines.append(f"  ROUGE-L : {grade(rl['fmeasure'])}")
    lines.append("")
    lines.append(sep)
    lines.append("  CATATAN:")
    lines.append("  - Referensi = LexRank (kalimat kunci dari transkripsi Whisper)")
    lines.append("  - Hipotesis = Ollama (notulensi abstraktif hasil LLM)")
    lines.append("  - ROUGE-1 : kecocokan kata tunggal (unigram)")
    lines.append("  - ROUGE-2 : kecocokan 2 kata berurutan (bigram)")
    lines.append("  - ROUGE-L : urutan kata terpanjang yang cocok (LCS)")
    lines.append("  - F1      : harmonic mean antara Precision dan Recall")
    lines.append("  - Precision: seberapa relevan isi ringkasan Ollama")
    lines.append("  - Recall   : seberapa banyak isi LexRank tercakup Ollama")
    lines.append("  - Nilai ideal Bahasa Indonesia: ROUGE-L > 30%")
    lines.append(sep)

    hasil = "\n".join(lines)
    print("\n" + hasil)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(hasil + "\n")
    print(f"\nHasil disimpan ke: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
