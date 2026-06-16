# hitung_korelasi_lexrank.py
# ===========================
# Menghitung KORELASI antara:
#   - Hasil ringkasan LexRank  (hasil_summarize/Lexrank.txt)
#   - Transkripsi asli Whisper  (hasil/transkrip_...txt)
#
# Metrik:
#   1. Cosine Similarity (TF-IDF)
#   2. Jaccard Similarity (kosakata unik)
#   3. Token Retention Rate
#   4. Sentence Coverage
#   5. Compression Ratio
#
# Output: akurasi/kolerasi_lexrank.txt

import os
import re
import sys
import io
import math
from collections import Counter

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── PATH FILE ────────────────────────────────────────────────────────────────
BASE_DIR       = r"c:\laragon\www\notulensi_rapat"
LEXRANK_FILE   = os.path.join(BASE_DIR, "hasil_summarize", "Lexrank.txt")
TRANSKRIP_FILE = os.path.join(
    BASE_DIR, "hasil",
    "transkrip_Zoom Meeting   Psikologi Sosial I C 2022 02 23 13 15 57_20260609_222504.txt"
)
OUTPUT_FILE    = os.path.join(BASE_DIR, "akurasi", "kolerasi_lexrank.txt")

# ─── STOPWORD BAHASA INDONESIA ────────────────────────────────────────────────
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

# ─── HELPER ───────────────────────────────────────────────────────────────────

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
        # --- cek substring exact (50 karakter pertama)
        if kal.lower()[:50] in trans_lower:
            match_count += 1
            details.append((kal[:70] + "...", "EXACT", 1.0))
            continue
        # --- cek jaccard terbaik vs semua kalimat transkrip
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


def rating(val, batas_tinggi, batas_sedang):
    if val >= batas_tinggi: return "TINGGI [OK]"
    if val >= batas_sedang: return "SEDANG  [~]"
    return "RENDAH  [!]"


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("Membaca file...")

    teks_lex   = baca_file(LEXRANK_FILE)
    teks_trans = baca_file(TRANSKRIP_FILE)

    # Hapus header transkripsi (6 baris pertama: === header ===)
    baris = teks_trans.split("\n")
    teks_trans_bersih = "\n".join(baris[6:]) if len(baris) > 6 else teks_trans

    # ── Tokenisasi
    tok_lex_raw   = tokenize(teks_lex)
    tok_trans_raw = tokenize(teks_trans_bersih)
    tok_lex       = filter_stopwords(tok_lex_raw)
    tok_trans     = filter_stopwords(tok_trans_raw)
    vocab_lex     = set(tok_lex)
    vocab_trans   = set(tok_trans)

    # ── 1. Cosine Similarity TF-IDF
    all_sets   = [vocab_lex, vocab_trans]
    vec_lex    = tfidf_vector(tok_lex,   all_sets)
    vec_trans  = tfidf_vector(tok_trans, all_sets)
    cos_val    = cosine_sim(vec_lex, vec_trans)

    # ── 2. Jaccard Similarity kosakata
    jac_val    = jaccard(vocab_lex, vocab_trans)

    # ── 3. Token Retention Rate
    cnt_lex   = Counter(tok_lex)
    cnt_trans = Counter(tok_trans)
    overlap_tok = sum(min(cnt_lex[t], cnt_trans[t]) for t in vocab_lex & vocab_trans)
    ret_val     = overlap_tok / len(tok_trans) if tok_trans else 0

    # ── 4. Sentence Coverage
    kalimat_lex            = split_kalimat(teks_lex)
    coverage_val, det_cov  = hitung_coverage(kalimat_lex, teks_trans_bersih)

    # ── 5. Compression Ratio
    comp_ratio = len(tok_lex_raw) / len(tok_trans_raw) if tok_trans_raw else 0

    # ── Bangun output
    sep  = "=" * 68
    sep2 = "-" * 68
    L    = []

    L.append(sep)
    L.append("   HASIL KORELASI: LexRank <-> Transkripsi Whisper")
    L.append(sep)
    L.append("")
    L.append("FILE LEXRANK   : " + LEXRANK_FILE)
    L.append("FILE TRANSKRIP : " + TRANSKRIP_FILE)
    L.append("")
    L.append(sep2)
    L.append("  STATISTIK DOKUMEN")
    L.append(sep2)
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
    L.append(sep2)
    L.append("  METRIK KORELASI")
    L.append(sep2)
    L.append(f"  {'1. Cosine Similarity (TF-IDF)':<42} : {cos_val*100:6.2f}%")
    L.append(f"  {'2. Jaccard Similarity (kosakata unik)':<42} : {jac_val*100:6.2f}%")
    L.append(f"  {'3. Token Retention Rate':<42} : {ret_val*100:6.2f}%")
    L.append(f"  {'4. Sentence Coverage':<42} : {coverage_val*100:6.2f}%")
    L.append(f"  {'5. Compression Ratio (lex/transkrip)':<42} : {comp_ratio*100:6.2f}%")

    L.append("")
    L.append(sep2)
    L.append("  INTERPRETASI SETIAP METRIK")
    L.append(sep2)
    L.append(f"  Cosine Similarity  : {rating(cos_val,  0.6, 0.3)}")
    L.append(f"  Jaccard Similarity : {rating(jac_val,  0.5, 0.25)}")
    L.append(f"  Token Retention    : {rating(ret_val,  0.5, 0.2)}")
    L.append(f"  Sentence Coverage  : {rating(coverage_val, 0.7, 0.4)}")
    if comp_ratio <= 0.35:
        L.append(f"  Compression Ratio  : BAIK (ringkasan padat, {comp_ratio*100:.1f}% panjang transkrip)")
    elif comp_ratio <= 0.6:
        L.append(f"  Compression Ratio  : WAJAR ({comp_ratio*100:.1f}% panjang transkrip)")
    else:
        L.append(f"  Compression Ratio  : TERLALU PANJANG ({comp_ratio*100:.1f}% panjang transkrip)")

    L.append("")
    L.append(sep2)
    L.append("  DETAIL COVERAGE PER KALIMAT LEXRANK")
    L.append(sep2)
    for i, (kal, lbl, sc) in enumerate(det_cov, 1):
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
    print(hasil)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(hasil)
    print(f"\nHasil disimpan ke: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
