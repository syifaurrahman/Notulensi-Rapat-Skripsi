# korelasi_new_digital_marketing.py
# ==================================
# 1. Baca transkrip Digital Marketing
# 2. Proses LexRank (extractive summarization)
# 3. Hitung korelasi hasil LexRank vs transkripsi asli
# 4. Simpan ke akurasi/kolerasi_new.txt

import os
import re
import sys
import io
import math
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── PATH ─────────────────────────────────────────────────────────────────────
BASE_DIR       = r"c:\laragon\www\notulensi_rapat"
TRANSKRIP_FILE = os.path.join(
    BASE_DIR, "hasil",
    "transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture - PENS SKY Venture 1080p h264_2_20260610_214445.txt"
)
LEXRANK_OUT    = os.path.join(BASE_DIR, "hasil_summarize", "Lexrank_digital_marketing.txt")
OUTPUT_FILE    = os.path.join(BASE_DIR, "akurasi", "kolerasi_new.txt")

# Tambahkan parent dir ke sys.path agar bisa import whispertranscription
PARENT_DIR = BASE_DIR
sys.path.insert(0, PARENT_DIR)

# ─── STOPWORD ─────────────────────────────────────────────────────────────────
STOPWORDS = {
    "yang","dan","di","ke","dari","ini","itu","ada","adalah","dengan","untuk",
    "atau","juga","ya","saya","kita","kami","kalian","dia","mereka","kamu",
    "aja","gitu","nih","tuh","kan","si","lah","dah","udah","mau","bisa",
    "nanti","tapi","jadi","karena","oke","nah","gak","tidak","bukan","sama",
    "lebih","dalam","pada","oleh","satu","dua","bahwa","lagi","sudah","belum",
    "pernah","kalau","lain","misalnya","seperti","buk","ibu","bu","iya","hmm",
    "gimana","terima","kasih","silahkan","boleh","mungkin","kira","apa","siapa",
    "dimana","bagaimana","sih","deh","dong","lho","wah","tapi","terus","emang",
    "banget","kayak","tuh","gitu","kalo","kalau","nih","juga","aja","oke","nah",
    "gak","yuk","ya","sih","iya","oh","ah","eh","hai","hey","halo","yah","pak"
}

# ─── HELPER KORELASI ──────────────────────────────────────────────────────────

def baca_file(path):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    raise FileNotFoundError(f"Tidak bisa membaca: {path}")

def tokenize(teks):
    teks = teks.lower()
    teks = re.sub(r"[^a-z\s]", " ", teks)
    return [w for w in teks.split() if w]

def filter_sw(tokens):
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

def tfidf_vector(tokens_list, all_docs_sets):
    tf    = Counter(tokens_list)
    total = len(tokens_list) or 1
    N     = len(all_docs_sets)
    vec   = {}
    for term in tf:
        df  = sum(1 for ds in all_docs_sets if term in ds)
        idf = math.log((N + 1) / (df + 1)) + 1
        vec[term] = (tf[term] / total) * idf
    return vec

def cosine_sim(va, vb):
    dot   = sum(va.get(k, 0) * vb.get(k, 0) for k in va)
    mag_a = math.sqrt(sum(v**2 for v in va.values()))
    mag_b = math.sqrt(sum(v**2 for v in vb.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def jaccard(sa, sb):
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def split_kalimat(teks):
    parts = re.split(r"[.!?\n]+", teks)
    return [p.strip() for p in parts if len(p.strip()) > 10]

def hitung_coverage(kal_lex, teks_trans):
    trans_lower   = teks_trans.lower()
    trans_kalimat = split_kalimat(teks_trans)
    match_count   = 0
    details       = []
    for kal in kal_lex:
        tok_kal = set(filter_sw(tokenize(kal)))
        if kal.lower()[:50] in trans_lower:
            match_count += 1
            details.append((kal[:75] + "...", "EXACT", 1.0))
            continue
        best_j = 0.0
        for kt in trans_kalimat:
            j = jaccard(tok_kal, set(filter_sw(tokenize(kt))))
            if j > best_j:
                best_j = j
        label = "MATCH" if best_j >= 0.4 else "LOW"
        if best_j >= 0.4:
            match_count += 1
        details.append((kal[:75] + "...", label, round(best_j, 3)))
    cov = match_count / len(kal_lex) if kal_lex else 0
    return cov, details

def rating(val, hi, mid):
    if val >= hi:  return "TINGGI [OK]"
    if val >= mid: return "SEDANG  [~]"
    return "RENDAH  [!]"

# ─── STEP 1: BACA & BERSIHKAN TRANSKRIP ───────────────────────────────────────

def baca_transkrip(path):
    raw = baca_file(path)
    baris = raw.split("\n")
    bersih = []
    started = False
    for b in baris:
        if not started:
            if "======================================" in b:
                started = True
        else:
            bersih.append(b)
    return "\n".join(bersih).strip(), raw

# ─── STEP 2: LEXRANK PIPELINE ─────────────────────────────────────────────────

def jalankan_lexrank(teks_bersih):
    try:
        from whispertranscription.summarize.lexrank import LexRankSummarizer
        from whispertranscription.summarize.config import SummaryConfig
    except ImportError as e:
        print(f"[ERROR] Import LexRankSummarizer gagal: {e}")
        sys.exit(1)

    cfg = SummaryConfig()
    cfg.min_sentences    = 8
    cfg.max_sentences    = 25
    cfg.compression_ratio = 0.20

    summarizer = LexRankSummarizer(cfg)

    print("  [1] Text Cleaning...")
    cleaned = summarizer._step1_text_cleaning(teks_bersih)

    print("  [2] Sentence Segmentation...")
    raw_sent = summarizer._step2_sentence_segmentation(cleaned)

    print("  [3] Sentence Filtering...")
    filtered = summarizer._step3_sentence_filtering(raw_sent)
    if not filtered:
        raw_sent.sort(key=len, reverse=True)
        target = max(cfg.min_sentences, min(8, len(raw_sent)))
        filtered = raw_sent[:target]

    target_n = int(len(filtered) * cfg.compression_ratio)
    target_n = max(cfg.min_sentences, min(target_n, cfg.max_sentences))
    print(f"  [4] LexRank Extraction (target {target_n} kalimat dari {len(filtered)})...")

    if len(filtered) <= target_n:
        organized = filtered
    else:
        top_sent, top_idx = summarizer._step4_lexrank_extraction(filtered, target=target_n)
        organized = summarizer._step5_reorganize(top_sent, top_idx, len(filtered))

    print("  [5] Final Format...")
    ringkasan = summarizer._step6_final_format(organized)
    return ringkasan

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  LEXRANK + KORELASI: Digital Marketing Transcription")
    print("=" * 65)

    # ── Baca transkrip
    print("\n[1] Membaca transkrip...")
    teks_bersih, teks_raw = baca_transkrip(TRANSKRIP_FILE)
    print(f"    Panjang: {len(teks_bersih.split())} kata")

    # ── Jalankan LexRank
    print("\n[2] Memproses LexRank...")
    ringkasan = jalankan_lexrank(teks_bersih)
    print(f"    Ringkasan: {len(ringkasan.split())} kata")

    # ── Simpan hasil LexRank
    os.makedirs(os.path.dirname(LEXRANK_OUT), exist_ok=True)
    with open(LEXRANK_OUT, "w", encoding="utf-8") as f:
        f.write("========================================\n")
        f.write("   RINGKASAN LEXRANK — Digital Marketing\n")
        f.write("========================================\n")
        f.write(ringkasan + "\n")
    print(f"    Disimpan ke: {LEXRANK_OUT}")

    # ── Hitung Korelasi
    print("\n[3] Menghitung korelasi LexRank vs Transkripsi...")

    tok_lex_raw   = tokenize(ringkasan)
    tok_trans_raw = tokenize(teks_bersih)
    tok_lex       = filter_sw(tok_lex_raw)
    tok_trans     = filter_sw(tok_trans_raw)
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

    comp_ratio  = len(tok_lex_raw) / len(tok_trans_raw) if tok_trans_raw else 0

    kal_lex             = split_kalimat(ringkasan)
    coverage_val, det   = hitung_coverage(kal_lex, teks_bersih)

    # ── Format Output
    sep  = "=" * 68
    sep2 = "-" * 68
    L    = []

    L.append(sep)
    L.append("   HASIL KORELASI: LexRank <-> Transkripsi Whisper")
    L.append("   Topik: Mentoring Digital Marketing (PENS SKY Venture)")
    L.append(sep)
    L.append("")
    L.append("FILE TRANSKRIP : " + TRANSKRIP_FILE)
    L.append("FILE LEXRANK   : " + LEXRANK_OUT)
    L.append("")
    L.append(sep2)
    L.append("  STATISTIK DOKUMEN")
    L.append(sep2)
    stats = [
        ("Token LexRank (raw)",              len(tok_lex_raw)),
        ("Token Transkrip (raw)",             len(tok_trans_raw)),
        ("Token LexRank (tanpa stopword)",    len(tok_lex)),
        ("Token Transkrip (tanpa stopword)",  len(tok_trans)),
        ("Kosakata unik LexRank",             len(vocab_lex)),
        ("Kosakata unik Transkrip",           len(vocab_trans)),
        ("Kosakata overlap (irisan)",         len(vocab_lex & vocab_trans)),
        ("Jumlah kalimat LexRank",            len(kal_lex)),
    ]
    for k, v in stats:
        L.append(f"  {k:<42} : {v}")

    L.append("")
    L.append(sep2)
    L.append("  METRIK KORELASI")
    L.append(sep2)
    L.append(f"  {'1. Cosine Similarity (TF-IDF)':<44} : {cos_val*100:6.2f}%")
    L.append(f"  {'2. Jaccard Similarity (kosakata unik)':<44} : {jac_val*100:6.2f}%")
    L.append(f"  {'3. Token Retention Rate':<44} : {ret_val*100:6.2f}%")
    L.append(f"  {'4. Sentence Coverage':<44} : {coverage_val*100:6.2f}%")
    L.append(f"  {'5. Compression Ratio (lex/transkrip)':<44} : {comp_ratio*100:6.2f}%")

    L.append("")
    L.append(sep2)
    L.append("  INTERPRETASI")
    L.append(sep2)
    L.append(f"  Cosine Similarity  : {rating(cos_val,  0.6, 0.3)}")
    L.append(f"  Jaccard Similarity : {rating(jac_val,  0.5, 0.25)}")
    L.append(f"  Token Retention    : {rating(ret_val,  0.5, 0.2)}")
    L.append(f"  Sentence Coverage  : {rating(coverage_val, 0.7, 0.4)}")
    if comp_ratio <= 0.35:
        L.append(f"  Compression Ratio  : BAIK - ringkasan padat ({comp_ratio*100:.1f}% panjang transkrip)")
    elif comp_ratio <= 0.6:
        L.append(f"  Compression Ratio  : WAJAR ({comp_ratio*100:.1f}% panjang transkrip)")
    else:
        L.append(f"  Compression Ratio  : TERLALU PANJANG ({comp_ratio*100:.1f}% panjang transkrip)")

    L.append("")
    L.append(sep2)
    L.append("  DETAIL COVERAGE PER KALIMAT LEXRANK")
    L.append(sep2)
    for i, (kal, lbl, sc) in enumerate(det, 1):
        L.append(f"  [{i:2d}] [{lbl:<5}] Jaccard={sc:.3f}  \"{kal}\"")

    L.append("")
    L.append(sep)
    L.append("  KESIMPULAN")
    L.append(sep)
    avg = (cos_val + jac_val + ret_val + coverage_val) / 4
    L.append(f"  Rata-rata korelasi (4 metrik utama) : {avg*100:.2f}%")
    if avg >= 0.65:
        kes = "LexRank SANGAT BERKORELASI dengan transkripsi Whisper."
    elif avg >= 0.40:
        kes = "LexRank CUKUP BERKORELASI dengan transkripsi Whisper."
    else:
        kes = "LexRank KURANG BERKORELASI dengan transkripsi Whisper."
    L.append(f"  Kesimpulan                          : {kes}")
    L.append(sep)

    hasil = "\n".join(L)
    print("\n" + hasil)

    # ── Simpan
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(hasil)
    print(f"\nHasil disimpan ke: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
