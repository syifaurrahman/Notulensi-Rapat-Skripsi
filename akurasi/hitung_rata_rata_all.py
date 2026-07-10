# hitung_rata_rata_all.py
# ==============================================================================
# Menghitung rata-rata metrik untuk:
#   1. LexRank (live_podcast1_depresi_kolerasi.txt, live_podcast2_genZ_kolerasi.txt,
#               live_podcast3_pentingBinggris_kolerasi.txt, live_podcast4_disiplin_kolerasi.txt)
#      Output -> akurasi/Lexrank/live_ratarata.txt
#
#   2. Ollama (live_podcast1_depresi_ollama.txt, live_podcast2_genZ_ollama.txt,
#              live_podcast3_PentingBinggris_ollama.txt, live_podcast4_disiplin_ollama.txt)
#      Output -> akurasi/ollama/live_ratarata.txt
#
#   3. Whisper (live_podcast1_depresi.txt, live_podcast2_genZ.txt,
#               live_podcast3_pentingBinggris.txt, live_podcast4_disiplin.txt)
#      Output -> akurasi/Whisper/live_ratarata.txt
# ==============================================================================

import os
import re
import sys
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR = r"c:\laragon\www\notulensi_rapat"

# File paths
LEXRANK_FILES = [
    os.path.join(BASE_DIR, "akurasi", "Lexrank", "live_podcast1_depresi_kolerasi.txt"),
    os.path.join(BASE_DIR, "akurasi", "Lexrank", "live_podcast2_genZ_kolerasi.txt"),
    os.path.join(BASE_DIR, "akurasi", "Lexrank", "live_podcast3_pentingBinggris_kolerasi.txt"),
    os.path.join(BASE_DIR, "akurasi", "Lexrank", "live_podcast4_disiplin_kolerasi.txt")
]

OLLAMA_FILES = [
    os.path.join(BASE_DIR, "akurasi", "ollama", "live_podcast1_depresi_ollama.txt"),
    os.path.join(BASE_DIR, "akurasi", "ollama", "live_podcast2_genZ_ollama.txt"),
    os.path.join(BASE_DIR, "akurasi", "ollama", "live_podcast3_PentingBinggris_ollama.txt"),
    os.path.join(BASE_DIR, "akurasi", "ollama", "live_podcast4_disiplin_ollama.txt")
]

WHISPER_FILES = [
    os.path.join(BASE_DIR, "akurasi", "Whisper", "live_podcast1_depresi.txt"),
    os.path.join(BASE_DIR, "akurasi", "Whisper", "live_podcast2_genZ.txt"),
    os.path.join(BASE_DIR, "akurasi", "Whisper", "live_podcast3_pentingBinggris.txt"),
    os.path.join(BASE_DIR, "akurasi", "Whisper", "live_podcast4_disiplin.txt")
]

# Output files
LEXRANK_OUT = os.path.join(BASE_DIR, "akurasi", "Lexrank", "live_ratarata.txt")
OLLAMA_OUT   = os.path.join(BASE_DIR, "akurasi", "ollama", "live_ratarata.txt")
WHISPER_OUT  = os.path.join(BASE_DIR, "akurasi", "Whisper", "live_ratarata.txt")

# ─── PARSER ───────────────────────────────────────────────────────────────────

def read_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def parse_lexrank(content):
    res = {}
    # Cosine Similarity (TF-IDF)
    m1 = re.search(r"Cosine Similarity\s*\(TF-IDF\)\s*:\s*([\d\.]+)%", content)
    if m1: res["cosine"] = float(m1.group(1))
    
    # Jaccard Similarity
    m2 = re.search(r"Jaccard Similarity\s*\(kosakata unik\)\s*:\s*([\d\.]+)%", content)
    if m2: res["jaccard"] = float(m2.group(1))

    # Token Retention Rate
    m3 = re.search(r"Token Retention Rate\s*:\s*([\d\.]+)%", content)
    if m3: res["retention"] = float(m3.group(1))

    # Sentence Coverage
    m4 = re.search(r"Sentence Coverage\s*:\s*([\d\.]+)%", content)
    if m4: res["coverage"] = float(m4.group(1))

    # Compression Ratio
    m5 = re.search(r"Compression Ratio\s*\(lex/transkrip\)\s*:\s*([\d\.]+)%", content)
    if m5: res["compression"] = float(m5.group(1))

    # Rata-rata korelasi
    m6 = re.search(r"Rata-rata korelasi\s*\(4 metrik utama\)\s*:\s*([\d\.]+)%", content)
    if m6: res["average"] = float(m6.group(1))

    return res

def parse_ollama(content):
    res = {}
    # ROUGE-1 (unigram)
    m1 = re.search(r"ROUGE-1\s+\(unigram\)\s*:\s*([\d\.]+)%\s*\[P:\s*([\d\.]+)%\s*R:\s*([\d\.]+)%\]", content)
    if m1:
        res["r1_f"] = float(m1.group(1))
        res["r1_p"] = float(m1.group(2))
        res["r1_r"] = float(m1.group(3))
        
    # ROUGE-2 (bigram)
    m2 = re.search(r"ROUGE-2\s+\(bigram\)\s*:\s*([\d\.]+)%\s*\[P:\s*([\d\.]+)%\s*R:\s*([\d\.]+)%\]", content)
    if m2:
        res["r2_f"] = float(m2.group(1))
        res["r2_p"] = float(m2.group(2))
        res["r2_r"] = float(m2.group(3))

    # ROUGE-L (LCS)
    m3 = re.search(r"ROUGE-L\s+\(LCS\)\s*:\s*([\d\.]+)%\s*\[P:\s*([\d\.]+)%\s*R:\s*([\d\.]+)%\]", content)
    if m3:
        res["rl_f"] = float(m3.group(1))
        res["rl_p"] = float(m3.group(2))
        res["rl_r"] = float(m3.group(3))

    return res

def parse_whisper(content):
    res = {}
    # WER
    m1 = re.search(r"WER\s+\(Word Error Rate\)\s*:\s*([\d\.]+)%", content)
    if m1: res["wer"] = float(m1.group(1))

    # WAcc
    m2 = re.search(r"WAcc\s+\(Word Accuracy\)\s*:\s*([\d\.]+)%", content)
    if m2: res["wacc"] = float(m2.group(1))

    # CER
    m3 = re.search(r"CER\s+\(Character Error Rate\)\s*:\s*([\d\.]+)%", content)
    if m3: res["cer"] = float(m3.group(1))

    return res

# ─── RUN ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  PROSES HITUNG RATA-RATA EVALUASI LIVE PODCAST")
    print("=" * 62)

    # 1. RATA-RATA LEXRANK
    print("\n[1] Membaca & Menghitung Rata-rata LexRank...")
    lex_data = []
    for fpath in LEXRANK_FILES:
        name = os.path.basename(fpath)
        if not os.path.exists(fpath):
            print(f"    [WARN] File tidak ditemukan: {fpath}")
            continue
        c = read_file(fpath)
        p = parse_lexrank(c)
        lex_data.append((name, p))
        print(f"    - {name}: Cosine={p.get('cosine',0):.2f}%, Coverage={p.get('coverage',0):.2f}%")

    if lex_data:
        n = len(lex_data)
        avg_cosine = sum(d[1].get("cosine", 0) for d in lex_data) / n
        avg_jaccard = sum(d[1].get("jaccard", 0) for d in lex_data) / n
        avg_retention = sum(d[1].get("retention", 0) for d in lex_data) / n
        avg_coverage = sum(d[1].get("coverage", 0) for d in lex_data) / n
        avg_compression = sum(d[1].get("compression", 0) for d in lex_data) / n
        avg_all = sum(d[1].get("average", 0) for d in lex_data) / n

        sep = "=" * 68
        sep2 = "-" * 68
        lines = [
            sep,
            "  RATA-RATA METRIK KORELASI LEXRANK <-> WHISPER",
            "  Sistem Notulensi — Live Podcast (Rata-rata 4 Podcast)",
            sep,
            f"  Jumlah Dokumen Evaluasi : {n}",
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
            "  DETAIL SKOR PER PODCAST:",
            sep2
        ]
        for name, p in lex_data:
            lines.append(f"  * {name:<42} : Cosine={p.get('cosine',0):.2f}%, Coverage={p.get('coverage',0):.2f}%, Rata2={p.get('average',0):.2f}%")
        lines.append(sep)

        lex_report = "\n".join(lines)
        os.makedirs(os.path.dirname(LEXRANK_OUT), exist_ok=True)
        with open(LEXRANK_OUT, "w", encoding="utf-8") as f:
            f.write(lex_report + "\n")
        print(f"    -> Hasil rata-rata LexRank disimpan ke: {LEXRANK_OUT}")

    # 2. RATA-RATA OLLAMA
    print("\n[2] Membaca & Menghitung Rata-rata Ollama...")
    oll_data = []
    for fpath in OLLAMA_FILES:
        name = os.path.basename(fpath)
        if not os.path.exists(fpath):
            print(f"    [WARN] File tidak ditemukan: {fpath}")
            continue
        c = read_file(fpath)
        p = parse_ollama(c)
        oll_data.append((name, p))
        print(f"    - {name}: ROUGE-1 F1={p.get('r1_f',0):.2f}%, ROUGE-L F1={p.get('rl_f',0):.2f}%")

    if oll_data:
        n = len(oll_data)
        avg_r1_f = sum(d[1].get("r1_f", 0) for d in oll_data) / n
        avg_r1_p = sum(d[1].get("r1_p", 0) for d in oll_data) / n
        avg_r1_r = sum(d[1].get("r1_r", 0) for d in oll_data) / n

        avg_r2_f = sum(d[1].get("r2_f", 0) for d in oll_data) / n
        avg_r2_p = sum(d[1].get("r2_p", 0) for d in oll_data) / n
        avg_r2_r = sum(d[1].get("r2_r", 0) for d in oll_data) / n

        avg_rl_f = sum(d[1].get("rl_f", 0) for d in oll_data) / n
        avg_rl_p = sum(d[1].get("rl_p", 0) for d in oll_data) / n
        avg_rl_r = sum(d[1].get("rl_r", 0) for d in oll_data) / n

        sep = "=" * 62
        sep2 = "-" * 62
        lines = [
            sep,
            "  RATA-RATA AKURASI RINGKASAN OLLAMA (ROUGE Score)",
            "  Sistem Notulensia — LLM (Rata-rata 4 Podcast)",
            sep,
            f"  Jumlah Dokumen Evaluasi : {n}",
            sep2,
            "  RATA-RATA METRIK ROUGE (F1 Score)",
            sep2,
            f"  ROUGE-1  (unigram)    :  {avg_r1_f:6.2f}%   [P: {avg_r1_p:.2f}%  R: {avg_r1_r:.2f}%]",
            f"  ROUGE-2  (bigram)     :  {avg_r2_f:6.2f}%   [P: {avg_r2_p:.2f}%  R: {avg_r2_r:.2f}%]",
            f"  ROUGE-L  (LCS)        :  {avg_rl_f:6.2f}%   [P: {avg_rl_p:.2f}%  R: {avg_rl_r:.2f}%]",
            sep2,
            "  PENILAIAN UMUM ROUGE-L",
            sep2,
            "  Status: " + ("Sangat Baik" if avg_rl_f >= 50.0 else "Baik" if avg_rl_f >= 30.0 else "Cukup" if avg_rl_f >= 15.0 else "Perlu Peningkatan"),
            sep,
            "",
            "  DETAIL SKOR PER PODCAST:",
            sep2
        ]
        for name, p in oll_data:
            lines.append(f"  * {name:<40} : ROUGE-1={p.get('r1_f',0):.2f}%, ROUGE-L={p.get('rl_f',0):.2f}%")
        lines.append(sep)

        oll_report = "\n".join(lines)
        os.makedirs(os.path.dirname(OLLAMA_OUT), exist_ok=True)
        with open(OLLAMA_OUT, "w", encoding="utf-8") as f:
            f.write(oll_report + "\n")
        print(f"    -> Hasil rata-rata Ollama disimpan ke: {OLLAMA_OUT}")

    # 3. RATA-RATA WHISPER
    print("\n[3] Membaca & Menghitung Rata-rata Whisper...")
    wh_data = []
    for fpath in WHISPER_FILES:
        name = os.path.basename(fpath)
        if not os.path.exists(fpath):
            print(f"    [WARN] File tidak ditemukan: {fpath}")
            continue
        c = read_file(fpath)
        p = parse_whisper(c)
        wh_data.append((name, p))
        print(f"    - {name}: WER={p.get('wer',0):.2f}%, WAcc={p.get('wacc',0):.2f}%, CER={p.get('cer',0):.2f}%")

    if wh_data:
        n = len(wh_data)
        avg_wer = sum(d[1].get("wer", 0) for d in wh_data) / n
        avg_wacc = sum(d[1].get("wacc", 0) for d in wh_data) / n
        avg_cer = sum(d[1].get("cer", 0) for d in wh_data) / n

        sep = "=" * 62
        sep2 = "-" * 62
        lines = [
            sep,
            "  RATA-RATA AKURASI TRANSKRIPSI WHISPER (WER / CER)",
            "  Sistem Notulensi — Live Podcast (Rata-rata 4 Podcast)",
            sep,
            f"  Jumlah Dokumen Evaluasi : {n}",
            sep2,
            "  RATA-RATA METRIK UTAMA",
            sep2,
            f"  WER   (Word Error Rate)     :  {avg_wer:6.2f}%",
            f"  WAcc  (Word Accuracy)       :  {avg_wacc:6.2f}%",
            f"  CER   (Character Error Rate):  {avg_cer:6.2f}%",
            sep2,
            "  PENILAIAN UMUM WHISPER (WAcc)",
            sep2,
            "  Status: " + ("Sangat Baik" if avg_wacc >= 90 else "Baik" if avg_wacc >= 80 else "Cukup" if avg_wacc >= 60 else "Perlu Peningkatan"),
            sep,
            "",
            "  DETAIL SKOR PER PODCAST:",
            sep2
        ]
        for name, p in wh_data:
            lines.append(f"  * {name:<36} : WER={p.get('wer',0):.2f}%, WAcc={p.get('wacc',0):.2f}%, CER={p.get('cer',0):.2f}%")
        lines.append(sep)

        wh_report = "\n".join(lines)
        os.makedirs(os.path.dirname(WHISPER_OUT), exist_ok=True)
        with open(WHISPER_OUT, "w", encoding="utf-8") as f:
            f.write(wh_report + "\n")
        print(f"    -> Hasil rata-rata Whisper disimpan ke: {WHISPER_OUT}")

    print("\n[FINISH] Seluruh rata-rata berhasil dihitung.")

if __name__ == "__main__":
    main()
