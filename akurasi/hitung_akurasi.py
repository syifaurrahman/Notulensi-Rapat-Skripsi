"""
hitung_akurasi.py — Hitung Akurasi Whisper (WER, WAcc, CER)
=============================================================
Cara pakai:
    1. Pastikan jiwer sudah terinstall:
       pip install jiwer

    2. Jalankan script ini:
       python hitung_akurasi.py

    3. Hasil akan tampil di terminal dan disimpan ke:
       akurasi/hasil_akurasi.txt
"""

import os
import re
import sys
import io
from datetime import datetime

# ── Fix encoding terminal Windows ──────────────────────────
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ══════════════════════════════════════════════════════════
# KONFIGURASI FILE
# ══════════════════════════════════════════════════════════

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR    = os.path.dirname(BASE_DIR)
HASIL_DIR     = os.path.join(PARENT_DIR, "hasil")

# File transkripsi Whisper (hypothesis)
WHISPER_FILE  = os.path.join(HASIL_DIR, "whisper transkrip psikologi.txt")

# File transkripsi manual (reference / ground truth)
MANUAL_FILE   = os.path.join(HASIL_DIR, "Manual akurasi transkrip.txt")

# Output hasil akurasi
OUTPUT_FILE   = os.path.join(BASE_DIR, "hasil_akurasi.txt")

# Baris header yang harus di-skip (4 baris pertama setelah header)
HEADER_LINES  = 6   # skip sampai baris kosong setelah "===...==="


# ══════════════════════════════════════════════════════════
# FUNGSI NORMALISASI TEKS
# ══════════════════════════════════════════════════════════

def normalize_text(text: str) -> str:
    """
    Normalisasi teks sebelum perhitungan WER/CER:
    - Lowercase semua huruf
    - Hapus tanda baca (kecuali apostrof dalam kata)
    - Hapus karakter non-ASCII berlebih
    - Normalisasi spasi
    """
    # Lowercase
    text = text.lower()

    # Hapus tanda baca umum (titik, koma, tanda seru, tanya, dll.)
    text = re.sub(r"[.,!?;:\"()\[\]{}\-—–/\\|<>@#$%^&*+=~`]", " ", text)

    # Hapus frasa halusinasi Whisper umum yang sering muncul
    halusinasi = [
        "terima kasih kerana menonton",
        "terima kasih sudah menonton",
        "terima kasih telah menonton",
        "subscribe",
        "musik",
        "music",
    ]
    for frasa in halusinasi:
        text = re.sub(re.escape(frasa), " ", text, flags=re.IGNORECASE)

    # Normalisasi spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text


def read_transcript(filepath: str, skip_header: bool = True) -> str:
    """
    Baca file transkripsi, opsional skip baris header.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")

    with open(filepath, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    if skip_header:
        # Skip baris header (=== TRANSKRIPSI RAPAT === dst.)
        content_lines = []
        skip = True
        for line in lines:
            if skip:
                # Baris konten dimulai setelah baris separator "===...==="
                if re.match(r"^={5,}", line.strip()):
                    skip = False
                continue
            content_lines.append(line)
        text = " ".join(content_lines)
    else:
        text = " ".join(lines)

    return normalize_text(text)


# ══════════════════════════════════════════════════════════
# HITUNG WER DAN CER — EDIT DISTANCE
# ══════════════════════════════════════════════════════════

def edit_distance(ref_tokens: list, hyp_tokens: list) -> tuple:
    """
    Hitung edit distance antara dua list token.
    Return (substitusi, penghapusan, penyisipan, distance_total).
    Menggunakan dynamic programming (Wagner-Fischer).
    """
    n = len(ref_tokens)
    m = len(hyp_tokens)

    # DP table: dp[i][j] = edit distance antara ref[:i] dan hyp[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_tokens[i - 1] == hyp_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    # Traceback untuk hitung S, D, I
    i, j = n, m
    substitusi = penghapusan = penyisipan = 0

    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref_tokens[i-1] == hyp_tokens[j-1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            substitusi += 1
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            penyisipan += 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            penghapusan += 1
            i -= 1
        else:
            break

    return substitusi, penghapusan, penyisipan, dp[n][m]


def hitung_wer(reference: str, hypothesis: str) -> dict:
    """Hitung Word Error Rate (WER), WAcc, dan info detil."""
    ref_words = reference.split()
    hyp_words = hypothesis.split()

    if not ref_words:
        return {"wer": 0.0, "wacc": 1.0, "S": 0, "D": 0, "I": 0, "N": 0}

    S, D, I, _ = edit_distance(ref_words, hyp_words)
    N   = len(ref_words)
    wer = (S + D + I) / N

    return {
        "wer"  : min(wer, 1.0),          # cap di 100%
        "wacc" : max(0.0, 1.0 - wer),
        "S"    : S, "D": D, "I": I, "N": N,
        "hyp_words": len(hyp_words),
    }


def hitung_cer(reference: str, hypothesis: str) -> dict:
    """Hitung Character Error Rate (CER)."""
    ref_chars = list(reference.replace(" ", ""))
    hyp_chars = list(hypothesis.replace(" ", ""))

    if not ref_chars:
        return {"cer": 0.0, "N_char": 0}

    S, D, I, _ = edit_distance(ref_chars, hyp_chars)
    N   = len(ref_chars)
    cer = (S + D + I) / N

    return {
        "cer"   : min(cer, 1.0),
        "S_c"   : S, "D_c": D, "I_c": I, "N_char": N,
    }


# ══════════════════════════════════════════════════════════
# HITUNG DENGAN JIWER (JIKA TERSEDIA)
# ══════════════════════════════════════════════════════════

def hitung_dengan_jiwer(reference: str, hypothesis: str):
    """
    Gunakan library jiwer jika tersedia (lebih akurat & cepat).
    Return dict atau None jika jiwer tidak ada.
    """
    try:
        from jiwer import wer as jiwer_wer, cer as jiwer_cer
        wer_val = jiwer_wer(reference, hypothesis)
        cer_val = jiwer_cer(reference, hypothesis)
        return {
            "wer"  : wer_val,
            "wacc" : max(0.0, 1.0 - wer_val),
            "cer"  : cer_val,
            "metode": "jiwer (library)",
        }
    except ImportError:
        return None


# ══════════════════════════════════════════════════════════
# FORMAT OUTPUT
# ══════════════════════════════════════════════════════════

def cetak_hasil(ref: str, hyp: str, wer_data: dict, cer_data: dict, metode: str):
    """Cetak dan simpan hasil ke file."""
    wer_pct  = wer_data["wer"]  * 100
    wacc_pct = wer_data["wacc"] * 100
    cer_pct  = cer_data["cer"]  * 100

    # Penilaian kualitas
    def grade(wer):
        if wer <= 5:   return "Sangat Baik ✓✓"
        if wer <= 10:  return "Baik ✓"
        if wer <= 20:  return "Cukup"
        if wer <= 35:  return "Kurang"
        return "Perlu Peningkatan"

    timestamp = datetime.now().strftime("%d %B %Y, %H:%M:%S")

    lines = [
        "=" * 60,
        "  HASIL PENGUJIAN AKURASI WHISPER",
        "  Sistem Notulensia — Transkripsi Rapat",
        "=" * 60,
        f"  Tanggal     : {timestamp}",
        f"  Metode      : {metode}",
        f"  File Ref    : Manual akurasi transkrip.txt",
        f"  File Hyp    : whisper transkrip psikologi.txt",
        "-" * 60,
        "",
        "  METRIK UTAMA",
        "  ─────────────────────────────────────────",
        f"  WER   (Word Error Rate)     :  {wer_pct:6.2f}%",
        f"  WAcc  (Word Accuracy)       :  {wacc_pct:6.2f}%",
        f"  CER   (Character Error Rate):  {cer_pct:6.2f}%",
        "",
    ]

    if "S" in wer_data:
        lines += [
            "  DETAIL WORD LEVEL",
            "  ─────────────────────────────────────────",
            f"  Total kata referensi (N) :  {wer_data['N']:,}",
            f"  Total kata hipotesis     :  {wer_data.get('hyp_words', '?'):,}",
            f"  Substitusi (S)           :  {wer_data['S']:,}",
            f"  Penghapusan (D)          :  {wer_data['D']:,}",
            f"  Penyisipan  (I)          :  {wer_data['I']:,}",
            "",
        ]

    if "N_char" in cer_data:
        lines += [
            "  DETAIL CHARACTER LEVEL",
            "  ─────────────────────────────────────────",
            f"  Total karakter referensi :  {cer_data['N_char']:,}",
            f"  Substitusi karakter (S)  :  {cer_data['S_c']:,}",
            f"  Penghapusan karakter (D) :  {cer_data['D_c']:,}",
            f"  Penyisipan  karakter (I) :  {cer_data['I_c']:,}",
            "",
        ]

    lines += [
        "  PENILAIAN",
        "  ─────────────────────────────────────────",
        f"  Kualitas WER  :  {grade(wer_pct)}",
        f"  Kualitas CER  :  {grade(cer_pct)}",
        "",
        "=" * 60,
        "  CATATAN:",
        "  - WER ideal untuk speech-to-text: < 10%",
        "  - WAcc = 100% - WER",
        "  - CER lebih ketat karena dihitung per karakter",
        "  - Normalisasi: lowercase, hapus tanda baca,",
        "    hapus frasa halusinasi Whisper",
        "=" * 60,
    ]

    output = "\n".join(lines)
    print(output)

    # Simpan ke file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\n  >> Hasil disimpan ke: {OUTPUT_FILE}")


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════

def main():
    print("\n[Notulensia] Memuat file transkripsi...", flush=True)

    try:
        reference  = read_transcript(MANUAL_FILE,  skip_header=True)
        hypothesis = read_transcript(WHISPER_FILE, skip_header=True)
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    print(f"  Referensi : {len(reference.split()):,} kata, {len(reference):,} karakter")
    print(f"  Whisper   : {len(hypothesis.split()):,} kata, {len(hypothesis):,} karakter")
    print("\n[Notulensia] Menghitung akurasi...", flush=True)

    # Coba pakai jiwer dulu
    jiwer_result = hitung_dengan_jiwer(reference, hypothesis)

    if jiwer_result:
        metode: str   = str(jiwer_result["metode"])
        wer_data = {"wer": jiwer_result["wer"], "wacc": jiwer_result["wacc"]}
        cer_data = {"cer": jiwer_result["cer"]}
    else:
        print("  [INFO] library jiwer tidak ditemukan, menggunakan kalkulasi manual.")
        print("         (install dengan: pip install jiwer)")
        metode   = "Edit Distance Manual (Wagner-Fischer)"
        wer_data = hitung_wer(reference, hypothesis)
        cer_data = hitung_cer(reference, hypothesis)

    cetak_hasil(reference, hypothesis, wer_data, cer_data, metode)


if __name__ == "__main__":
    main()
