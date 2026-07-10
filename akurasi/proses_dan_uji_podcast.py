# proses_dan_uji_podcast.py
# ==============================================================================
# Script ini mengotomatiskan seluruh alur pemrosesan dan pengujian untuk Podcast:
# 1. Meringkas transkrip podcast dengan LexRank murni -> hasil_summarize/lexrank/podcast_lexrank1.txt
# 2. Meringkas hasil LexRank dengan Ollama (Llama 3.2) -> hasil_summarize/ollama/podcast_lexrank1.txt
# 3. Menghitung korelasi LexRank vs transkrip asli -> akurasi/Lexrank/podcast_kolerasi1.txt
# 4. Menghitung ketepatan Ollama vs LexRank (ROUGE) -> akurasi/ollama/podcast_akurasi1.txt
# ==============================================================================

import os
import re
import sys
import io
import math
from collections import Counter
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Setup import path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PARENT_DIR)

from whispertranscription.summarize.lexrank import LexRankSummarizer
from whispertranscription.summarize.config import SummaryConfig

# ─── PATH FILE ────────────────────────────────────────────────────────────────
WHISPER_FILE = os.path.join(PARENT_DIR, "hasil", "podcast _1.txt")

# Folder output ringkasan
LEXRANK_OUT_DIR = os.path.join(PARENT_DIR, "hasil_summarize", "Lexrank")
OLLAMA_OUT_DIR  = os.path.join(PARENT_DIR, "hasil_summarize", "Ollama")
LEXRANK_OUT_FILE = os.path.join(LEXRANK_OUT_DIR, "podcast_lexrank1.txt")
OLLAMA_OUT_FILE  = os.path.join(OLLAMA_OUT_DIR, "podcast_lexrank1.txt")

# Folder output akurasi
LEXRANK_AKURASI_DIR  = os.path.join(BASE_DIR, "Lexrank")
OLLAMA_AKURASI_DIR   = os.path.join(BASE_DIR, "ollama")
KORELASI_OUT_FILE    = os.path.join(LEXRANK_AKURASI_DIR, "podcast_kolerasi1.txt")
ROUGE_OUT_FILE       = os.path.join(OLLAMA_AKURASI_DIR, "podcast_akurasi1.txt")


# ─── STOPWORDS UNTUK KORELASI ──────────────────────────────────────────────────
STOPWORDS = {
    "yang","dan","di","ke","dari","ini","itu","ada","adalah","dengan","untuk",
    "atau","juga","ya","saya","kita","kami","kalian","dia","mereka","kamu",
    "aja","gitu","nih","tuh","kan","si","lah","dah","udah","mau","bisa",
    "nanti","tapi","jadi","karena","oke","nah","gak","tidak","bukan","sama",
    "lebih","dalam","pada","oleh","satu","dua","bahwa","lagi","sudah","belum",
    "pernah","kalau","lain","misalnya","seperti","buk","ibu","bu","iya","hmm",
    "gimana","ya","terima","kasih","silahkan","boleh","mungkin","kira","apa",
    "siapa","dimana","bagaimana","sih","nih","tuh","deh","dong","lho","wah"
}

def clean_hallucinations(text):
    # Hapus prompt leak di akhir jika ada
    text = re.sub(r"pertahankan kata-kata inggris apa adanya, jangan diterjemahkan\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"pertahankan kata kata inggris apa adanya jangan diterjemahkan\.?", "", text, flags=re.IGNORECASE)
    return text

def read_raw_transcript(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    content = []
    started = False
    for line in lines:
        if not started:
            if re.match(r"^={5,}", line.strip()):
                started = True
            continue
        content.append(line)
    raw_text = " ".join(content).strip()
    return clean_hallucinations(raw_text)


# ─── METRIK KORELASI FUNCTIONS ─────────────────────────────────────────────────
def tokenize(teks):
    teks = teks.lower()
    teks = re.sub(r"[^a-z\s]", " ", teks)
    return [w for w in teks.split() if w]

def filter_stopwords(tokens):
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

def tfidf_vector(tokens_list, all_docs_sets):
    tf = Counter(tokens_list)
    total = len(tokens_list) or 1
    N = len(all_docs_sets)
    vec = {}
    for term in tf:
        df = sum(1 for ds in all_docs_sets if term in ds)
        idf = math.log((N + 1) / (df + 1)) + 1
        vec[term] = (tf[term] / total) * idf
    return vec

def cosine_sim(vec_a, vec_b):
    dot   = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in vec_a)
    mag_a = math.sqrt(sum(v**2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v**2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def split_kalimat(teks):
    parts = re.split(r"[.!?\n]+", teks)
    return [p.strip() for p in parts if len(p.strip()) > 10]

def hitung_coverage(kalimat_lex, teks_transkrip):
    trans_lower   = teks_transkrip.lower()
    trans_kalimat = split_kalimat(teks_transkrip)
    match_count   = 0
    details       = []
    for kal in kalimat_lex:
        tok_kal = set(filter_stopwords(tokenize(kal)))
        if kal.lower()[:50] in trans_lower:
            match_count += 1
            details.append((kal[:70] + "...", "EXACT", 1.0))
            continue
        best_j = 0.0
        for k_t in trans_kalimat:
            tok_t = set(filter_stopwords(tokenize(k_t)))
            j = jaccard(tok_kal, tok_t)
            if j > best_j:
                best_j = j
        label = "MATCH" if best_j >= 0.4 else "LOW"
        if best_j >= 0.4:
            match_count += 1
        details.append((kal[:70] + "...", label, round(best_j, 3)))
    coverage = match_count / len(kalimat_lex) if kalimat_lex else 0
    return coverage, details

def rating_korelasi(val, batas_tinggi, batas_sedang):
    if val >= batas_tinggi: return "TINGGI [OK]"
    if val >= batas_sedang: return "SEDANG  [~]"
    return "RENDAH  [!]"


# ─── ROUGE ACCURACY FUNCTIONS ──────────────────────────────────────────────────
def normalize_for_rouge(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text) # Hapus bold
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE) # Hapus headings
    text = re.sub(r'^\s*[\*\-\d]+[\.\)]\s*', '', text, flags=re.MULTILINE) # Hapus bullets
    text = re.sub(r'[.,!?;:()\[\]{}\-—–/\\|<>@#$%^&*+=~`"\']', ' ', text) # Hapus tanda baca
    text = re.sub(r'\s+', ' ', text).strip() # Normalisasi spasi
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

def hitung_dengan_library_rouge(reference: str, hypothesis: str):
    try:
        from rouge_score import rouge_scorer
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
        scores = scorer.score(reference, hypothesis)
        return {
            "rouge1": {"precision": scores['rouge1'].precision, "recall": scores['rouge1'].recall, "fmeasure": scores['rouge1'].fmeasure},
            "rouge2": {"precision": scores['rouge2'].precision, "recall": scores['rouge2'].recall, "fmeasure": scores['rouge2'].fmeasure},
            "rougeL": {"precision": scores['rougeL'].precision, "recall": scores['rougeL'].recall, "fmeasure": scores['rougeL'].fmeasure},
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


# ─── MAIN PROCESS ─────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("   PROSES PIPELINE SUMMARIZATION & EVALUASI PODCAST")
    print("=" * 70)

    # 1. Baca transkrip asli
    print(f"\n[1] Membaca transkrip asli dari: {WHISPER_FILE}")
    if not os.path.exists(WHISPER_FILE):
        print(f"[ERROR] File transkrip tidak ditemukan: {WHISPER_FILE}")
        sys.exit(1)
    raw_text = read_raw_transcript(WHISPER_FILE)
    print(f"    Panjang teks transkrip: {len(raw_text.split())} kata.")

    # 2. Jalankan LexRank & Ollama Summarizer
    print("\n[2] Menjalankan Pipeline Summarization...")
    cfg = SummaryConfig()
    cfg.min_sentences = 8
    cfg.max_sentences = 25
    cfg.compression_ratio = 0.20
    
    summarizer = LexRankSummarizer(cfg)
    
    # Dapatkan ringkasan LexRank dan Ollama
    res = summarizer.summarize_with_debug(raw_text)
    lexrank_extractive = res['lexrank_extractive']
    ollama_result = res['ollama_result']
    
    if not lexrank_extractive:
        print("[ERROR] Peringkasan LexRank menghasilkan teks kosong.")
        sys.exit(1)

    # Simpan hasil LexRank
    os.makedirs(LEXRANK_OUT_DIR, exist_ok=True)
    with open(LEXRANK_OUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== HASIL LEXRANK EXTRACTIVE ===\n")
        f.write(f"Sumber    : podcast _1.txt\n")
        f.write(f"Dibuat    : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Model     : Whisper small\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(lexrank_extractive + "\n")
    print(f"    ✓ Ringkasan LexRank disimpan ke: {LEXRANK_OUT_FILE}")

    # Simpan hasil Ollama
    if not ollama_result:
        print("[WARNING] Hasil Ollama kosong atau server Ollama tidak aktif. Mencoba memanggil ulang Ollama...")
        if summarizer.ollama.is_available():
            cleaned_step1 = summarizer._step1_text_cleaning(raw_text)
            raw_sents = summarizer._step2_sentence_segmentation(cleaned_step1)
            filtered_sents = summarizer._step3_sentence_filtering(raw_sents)
            if not filtered_sents:
                filtered_sents = raw_sents[:8]
            target_sentences = max(cfg.min_sentences, min(int(len(filtered_sents) * cfg.compression_ratio), cfg.max_sentences))
            top_sents, top_idx = summarizer._step4_lexrank_extraction(filtered_sents, target=target_sentences)
            organized = summarizer._step5_reorganize(top_sents, top_idx, len(filtered_sents))
            ollama_result = summarizer.ollama.rewrite(organized, full_context=cleaned_step1)
            
    if not ollama_result:
        print("[ERROR] Gagal memanggil Ollama. Pastikan server Ollama aktif (ollama run Llama 3.2).")
        sys.exit(1)

    os.makedirs(OLLAMA_OUT_DIR, exist_ok=True)
    with open(OLLAMA_OUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== HASIL OLLAMA ABSTRACTIVE ===\n")
        f.write(f"Sumber    : podcast_lexrank1.txt\n")
        f.write(f"Dibuat    : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Model     : Whisper small + {cfg.ollama_model}\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(ollama_result + "\n")
    print(f"    ✓ Ringkasan Ollama disimpan ke: {OLLAMA_OUT_FILE}")

    # 3. Hitung Korelasi LexRank vs Transkrip Asli
    print("\n[3] Menghitung Korelasi LexRank vs Transkrip Asli...")
    tok_lex_raw   = tokenize(lexrank_extractive)
    tok_trans_raw = tokenize(raw_text)
    tok_lex       = filter_stopwords(tok_lex_raw)
    tok_trans     = filter_stopwords(tok_trans_raw)
    vocab_lex     = set(tok_lex)
    vocab_trans   = set(tok_trans)

    all_sets   = [vocab_lex, vocab_trans]
    vec_lex    = tfidf_vector(tok_lex,   all_sets)
    vec_trans  = tfidf_vector(tok_trans, all_sets)
    cos_val    = cosine_sim(vec_lex, vec_trans)
    jac_val    = jaccard(vocab_lex, vocab_trans)

    cnt_lex   = Counter(tok_lex)
    cnt_trans = Counter(tok_trans)
    overlap_tok = sum(min(cnt_lex[t], cnt_trans[t]) for t in vocab_lex & vocab_trans)
    ret_val     = overlap_tok / len(tok_trans) if tok_trans else 0

    kalimat_lex            = split_kalimat(lexrank_extractive)
    coverage_val, det_cov  = hitung_coverage(kalimat_lex, raw_text)
    comp_ratio = len(tok_lex_raw) / len(tok_trans_raw) if tok_trans_raw else 0

    # Build korelasi report
    L = []
    L.append("=" * 68)
    L.append("   HASIL KORELASI: LexRank <-> Transkripsi Whisper")
    L.append("=" * 68)
    L.append("")
    L.append("FILE LEXRANK   : hasil_summarize/lexrank/podcast_lexrank1.txt")
    L.append("FILE TRANSKRIP : hasil/podcast _1.txt")
    L.append("")
    L.append("-" * 68)
    L.append("  STATISTIK DOKUMEN")
    L.append("-" * 68)
    stats = [
        ("Token LexRank (raw)",          len(tok_lex_raw)),
        ("Token Transkrip (raw)",         len(tok_trans_raw)),
        ("Token LexRank (tanpa stopword)", len(tok_lex)),
        ("Token Transkrip (tanpa stopword)", len(tok_trans)),
        ("Kosakata unik LexRank",         len(vocab_lex)),
        ("Kosakata unik Transkrip",        len(vocab_trans)),
        ("Kosakata overlap (irisan)",      len(vocab_lex & vocab_trans)),
        ("Jumlah kalimat LexRank",         len(kalimat_lex)),
    ]
    for k, v in stats:
        L.append(f"  {k:<40} : {v}")
    L.append("")
    L.append("-" * 68)
    L.append("  METRIK KORELASI")
    L.append("-" * 68)
    L.append(f"  {'1. Cosine Similarity (TF-IDF)':<42} : {cos_val*100:6.2f}%")
    L.append(f"  {'2. Jaccard Similarity (kosakata unik)':<42} : {jac_val*100:6.2f}%")
    L.append(f"  {'3. Token Retention Rate':<42} : {ret_val*100:6.2f}%")
    L.append(f"  {'4. Sentence Coverage':<42} : {coverage_val*100:6.2f}%")
    L.append(f"  {'5. Compression Ratio (lex/transkrip)':<42} : {comp_ratio*100:6.2f}%")
    L.append("")
    L.append("-" * 68)
    L.append("  INTERPRETASI SETIAP METRIK")
    L.append("-" * 68)
    L.append(f"  Cosine Similarity  : {rating_korelasi(cos_val,  0.6, 0.3)}")
    L.append(f"  Jaccard Similarity : {rating_korelasi(jac_val,  0.5, 0.25)}")
    L.append(f"  Token Retention    : {rating_korelasi(ret_val,  0.5, 0.2)}")
    L.append(f"  Sentence Coverage  : {rating_korelasi(coverage_val, 0.7, 0.4)}")
    if comp_ratio <= 0.35:
        L.append(f"  Compression Ratio  : BAIK (ringkasan padat, {comp_ratio*100:.1f}% panjang transkrip)")
    elif comp_ratio <= 0.6:
        L.append(f"  Compression Ratio  : WAJAR ({comp_ratio*100:.1f}% panjang transkrip)")
    else:
        L.append(f"  Compression Ratio  : TERLALU PANJANG ({comp_ratio*100:.1f}% panjang transkrip)")
    L.append("")
    L.append("-" * 68)
    L.append("  DETAIL COVERAGE PER KALIMAT LEXRANK")
    L.append("-" * 68)
    for i, (kal, lbl, sc) in enumerate(det_cov, 1):
        L.append(f"  [{i:2d}] [{lbl:<5}] Jaccard={sc:.3f}  \"{kal}\"")
    L.append("")
    L.append("=" * 68)
    L.append("  KESIMPULAN")
    L.append("=" * 68)
    avg_kor = (cos_val + jac_val + ret_val + coverage_val) / 4
    L.append(f"  Rata-rata korelasi (4 metrik utama) : {avg_kor*100:.2f}%")
    if avg_kor >= 0.65:
        kes = "LexRank SANGAT BERKORELASI dengan transkripsi Whisper."
    elif avg_kor >= 0.40:
        kes = "LexRank CUKUP BERKORELASI dengan transkripsi Whisper."
    else:
        kes = "LexRank KURANG BERKORELASI dengan transkripsi Whisper."
    L.append(f"  Kesimpulan                          : {kes}")
    L.append("=" * 68)

    os.makedirs(LEXRANK_AKURASI_DIR, exist_ok=True)
    with open(KORELASI_OUT_FILE, "w", encoding="utf-8") as kf:
        kf.write("\n".join(L) + "\n")
    print(f"    ✓ Laporan korelasi disimpan ke: {KORELASI_OUT_FILE}")

    # 4. Hitung ROUGE Accuracy (Ollama vs LexRank)
    print("\n[4] Menghitung Ketepatan Ringkasan (Ollama vs LexRank via ROUGE)...")
    sistem_norm = normalize_for_rouge(ollama_result)
    manual_norm = normalize_for_rouge(lexrank_extractive)

    # ROUGE
    lib_result = hitung_dengan_library_rouge(manual_norm, sistem_norm)
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

    # Build ROUGE report
    R = []
    R.append("=" * 62)
    R.append("  HASIL PENGUJIAN AKURASI SUMMARIZATION")
    R.append("  Sistem Notulensia — LLM (Ollama / Llama 3.2)")
    R.append("=" * 62)
    R.append(f"  Tanggal      : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}")
    R.append(f"  Metode       : {metode}")
    R.append(f"  File Sistem  : hasil_summarize/ollama/podcast_lexrank1.txt")
    R.append(f"  File Ref     : hasil_summarize/lexrank/podcast_lexrank1.txt")
    R.append(f"  Kata Sistem  : {len(sistem_norm.split()):,}")
    R.append(f"  Kata Ref     : {len(manual_norm.split()):,}")
    R.append("-" * 62)
    R.append("")
    R.append("  METRIK ROUGE (F1 Score)")
    R.append("  " + "─" * 50)
    R.append(f"  ROUGE-1  (unigram)    : {r1['fmeasure']*100:6.2f}%   [P: {r1['precision']*100:.2f}%  R: {r1['recall']*100:.2f}%]")
    R.append(f"  ROUGE-2  (bigram)     : {r2['fmeasure']*100:6.2f}%   [P: {r2['precision']*100:.2f}%  R: {r2['recall']*100:.2f}%]")
    R.append(f"  ROUGE-L  (LCS)        : {rl['fmeasure']*100:6.2f}%   [P: {rl['precision']*100:.2f}%  R: {rl['recall']*100:.2f}%]")
    R.append("")
    R.append("  PENILAIAN")
    R.append("  " + "─" * 50)
    R.append(f"  ROUGE-1 : {grade_rouge(r1['fmeasure'])}")
    R.append(f"  ROUGE-2 : {grade_rouge(r2['fmeasure'])}")
    R.append(f"  ROUGE-L : {grade_rouge(rl['fmeasure'])}")
    R.append("")
    R.append("=" * 62)
    R.append("  CATATAN:")
    R.append("  - ROUGE-1 mengukur kecocokan kata tunggal (unigram)")
    R.append("  - ROUGE-2 mengukur kecocokan 2 kata berurutan (bigram)")
    R.append("  - ROUGE-L mengukur urutan kata terpanjang yang cocok")
    R.append("  - F1 = harmonic mean antara Precision dan Recall")
    R.append("  - Nilai ideal untuk Bahasa Indonesia: ROUGE-L > 30%")
    R.append("  - P (Precision): seberapa relevan ringkasan sistem")
    R.append("  - R (Recall)   : seberapa lengkap isi referensi tercakup")
    R.append("=" * 62)

    os.makedirs(OLLAMA_AKURASI_DIR, exist_ok=True)
    with open(ROUGE_OUT_FILE, "w", encoding="utf-8") as rf:
        rf.write("\n".join(R) + "\n")
    print(f"    ✓ Laporan ROUGE disimpan ke: {ROUGE_OUT_FILE}")
    print("\n" + "=" * 70)
    print("   PROSES SELESAI DENGAN SUKSES!")
    print("=" * 70)

if __name__ == "__main__":
    main()
