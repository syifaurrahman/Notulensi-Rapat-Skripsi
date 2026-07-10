# hitung_noise_bunyihp.py
# Menghitung WER / WAcc / CER untuk noise bunyi HP:
#   Tabel 1: Real vs Sebelum Noise Filter (before_noise_bunyihp)
#   Tabel 2: Real vs Sesudah Noise Filter (after_noise_bunyihp)

import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from jiwer import process_words, process_characters

BASE = r"c:\laragon\www\notulensi_rapat\noise_reduction"

REF_FILE    = os.path.join(BASE, "uud1945_real.txt")
BEFORE_FILE = os.path.join(BASE, "uud1945_before_noise_bunyihp.txt")
AFTER_FILE  = os.path.join(BASE, "uud1945_after_noise_bunyihp.txt")

def baca(path):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return f.read().strip()
        except:
            continue
    raise FileNotFoundError(path)

def normalisasi(teks):
    teks = teks.lower()
    teks = re.sub(r"[^\w\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks).strip()
    return teks

def hitung(ref_raw, hyp_raw, label):
    ref = normalisasi(ref_raw)
    hyp = normalisasi(hyp_raw)

    wout = process_words(ref, hyp)
    cout = process_characters(ref, hyp)

    S = wout.substitutions
    D = wout.deletions
    I = wout.insertions
    H = wout.hits
    N     = S + D + H
    N_hyp = S + I + H

    wer  = wout.wer  * 100
    wacc = (1 - wout.wer) * 100
    cer  = cout.cer * 100

    print(f"\n{'='*68}")
    print(f"  {label}")
    print(f"{'='*68}")
    print(f"  Referensi Kata (N)   : {N}")
    print(f"  Kata Hipotesis       : {N_hyp}")
    print(f"  Substitutions (S)    : {S}")
    print(f"  Deletions     (D)    : {D}")
    print(f"  Insertions    (I)    : {I}")
    print(f"  Hits          (H)    : {H}")
    print(f"  WER                  : {wer:.2f}%")
    print(f"  WAcc                 : {wacc:.2f}%")
    print(f"  CER                  : {cer:.2f}%")
    print(f"{'='*68}")

    return {
        "N": N, "N_hyp": N_hyp,
        "S": S, "D": D, "I": I, "H": H,
        "WER": round(wer, 2), "WAcc": round(wacc, 2), "CER": round(cer, 2)
    }

ref    = baca(REF_FILE)
before = baca(BEFORE_FILE)
after  = baca(AFTER_FILE)

r1 = hitung(ref, before, "Tabel 1 — Sebelum Noise Filter (Bunyi HP) vs Referensi Asli")
r2 = hitung(ref, after,  "Tabel 2 — Sesudah Noise Filter (Bunyi HP) vs Referensi Asli")

print("\n\nRINGKASAN PERBANDINGAN:")
print(f"{'Metrik':<12} {'Sebelum Filter':>16} {'Sesudah Filter':>16} {'Selisih':>10}")
print("-"*56)
for k in ("WER", "WAcc", "CER"):
    diff = r2[k] - r1[k]
    arah = "+" if diff > 0 else ""
    print(f"{k:<12} {r1[k]:>15.2f}%  {r2[k]:>15.2f}%  {arah}{diff:>8.2f}%")
