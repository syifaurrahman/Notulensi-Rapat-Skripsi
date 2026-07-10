# hitung_rata_rata_upload_lexrank.py
# ==============================================================================
# Menghitung rata-rata dari 5 metrik korelasi LexRank untuk dataset upload (9 file):
#   1. Cosine Similarity
#   2. Jaccard Similarity
#   3. Token Retention Rate
#   4. Sentence Coverage
#   5. Compression Ratio
#
# Output: akurasi/Lexrank/rata rata lexrank.txt
# ==============================================================================

import os
import re
import sys
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = r"c:\laragon\www\notulensi_rapat"
LEXRANK_DIR = os.path.join(BASE_DIR, "akurasi", "Lexrank")

UPLOAD_FILES = [
    " meeting esg and qhse.txt",
    "ilmu komunikasi.txt",
    "keselamatan kerja.txt",
    "kolerasi_lexrank_digital marketing.txt",
    "kolerasi_lexrank_psikologi.txt",
    "manajemen bisnis.txt",
    "rapat komisi dpr.txt",
    "zoom meeting basis data.txt",
    "zoom meeting kwu.txt"
]

def read_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def parse_metrics(content):
    res = {}
    m1 = re.search(r"Cosine Similarity\s*\(TF-IDF\)\s*:\s*([\d\.]+)%", content)
    if m1: res["cosine"] = float(m1.group(1))

    m2 = re.search(r"Jaccard Similarity\s*\(kosakata unik\)\s*:\s*([\d\.]+)%", content)
    if m2: res["jaccard"] = float(m2.group(1))

    m3 = re.search(r"Token Retention Rate\s*:\s*([\d\.]+)%", content)
    if m3: res["retention"] = float(m3.group(1))

    m4 = re.search(r"Sentence Coverage\s*:\s*([\d\.]+)%", content)
    if m4: res["coverage"] = float(m4.group(1))

    m5 = re.search(r"Compression Ratio\s*\(lex/transkrip\)\s*:\s*([\d\.]+)%", content)
    if m5: res["compression"] = float(m5.group(1))

    m6 = re.search(r"Rata-rata korelasi\s*\(4 metrik utama\)\s*:\s*([\d\.]+)%", content)
    if m6: res["average"] = float(m6.group(1))

    return res

def main():
    print("Membaca & Memproses Averages Dataset Upload...")
    
    data = []
    for fname in UPLOAD_FILES:
        fpath = os.path.join(LEXRANK_DIR, fname)
        if not os.path.exists(fpath):
            print(f"[WARN] File tidak ditemukan: {fpath}")
            continue
        c = read_file(fpath)
        m = parse_metrics(c)
        data.append((fname, m))
        print(f"  - {fname}: Cosine={m.get('cosine', 0):.2f}%, Jaccard={m.get('jaccard', 0):.2f}%, Retention={m.get('retention', 0):.2f}%")

    if not data:
        print("[ERROR] Tidak ada data upload yang bisa diproses.")
        sys.exit(1)

    n = len(data)
    avg_cosine = sum(d[1].get("cosine", 0) for d in data) / n
    avg_jaccard = sum(d[1].get("jaccard", 0) for d in data) / n
    avg_retention = sum(d[1].get("retention", 0) for d in data) / n
    avg_coverage = sum(d[1].get("coverage", 0) for d in data) / n
    avg_compression = sum(d[1].get("compression", 0) for d in data) / n
    avg_all = sum(d[1].get("average", 0) for d in data) / n

    sep = "=" * 68
    sep2 = "-" * 68
    
    lines = [
        sep,
        "  RATA-RATA EVALUASI KORELASI LEXRANK (DATASET UPLOAD - 9 TOPIK)",
        "  Sistem Notulensi — Upload Rapat (Rata-rata 9 Rapat)",
        sep,
        f"  Jumlah Dataset Pengujian : {n} file rapat",
        f"  Tanggal Perhitungan      : 01 July 2026",
        sep2,
        "  RINCIAN RATA-RATA METRIK",
        sep2,
        f"  1. Cosine Similarity (TF-IDF)          :  {avg_cosine:6.2f}%",
        f"  2. Jaccard Similarity (kosakata unik)  :  {avg_jaccard:6.2f}%",
        f"  3. Token Retention Rate                :  {avg_retention:6.2f}%",
        f"  4. Sentence Coverage                   :  {avg_coverage:6.2f}%",
        f"  5. Compression Ratio (lex/transkrip)   :  {avg_compression:6.2f}%",
        sep2,
        "  KESIMPULAN UMUM",
        sep2,
        f"  Rata-rata korelasi (4 metrik utama)    :  {avg_all:6.2f}%",
        f"  Status: " + ("SANGAT BERKORELASI" if avg_all >= 65 else "CUKUP BERKORELASI" if avg_all >= 40 else "KURANG BERKORELASI"),
        sep,
        "",
        "  DETAIL METRIK PER TOPIK RAPAT:",
        sep2
    ]

    for fname, m in data:
        lines.append(f"  * {fname:<42} : Cosine={m.get('cosine', 0):.2f}%, Jaccard={m.get('jaccard', 0):.2f}%, Coverage={m.get('coverage', 0):.2f}%")
    lines.append(sep)

    output_text = "\n".join(lines)
    print("\n" + output_text)

    output_file = os.path.join(LEXRANK_DIR, "rata rata lexrank.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text + "\n")
    print(f"\nHasil rata-rata upload disimpan ke: {output_file}")

if __name__ == "__main__":
    main()
