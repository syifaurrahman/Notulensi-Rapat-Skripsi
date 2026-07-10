# hitung_filler_confmat.py
# Evaluasi Word Filler Removal menggunakan Confusion Matrix
# TP/FP/TN/FN → Precision, Recall, F1-Score, Accuracy
#
# Definisi per-token pada Whisper transcript:
#   Ground Truth Filler  = kata ada di daftar filler (FILLER_WORDS_EXACT / regex)
#   Ground Truth Valid   = kata bukan filler
#   Predicted Filler     = kata DIHAPUS oleh sistem (tidak ada di cleaned text)
#   Predicted Valid      = kata DIPERTAHANKAN oleh sistem
#
#   TP = GT Filler  + Predicted Filler   (benar hapus filler)
#   FP = GT Valid   + Predicted Filler   (salah hapus kata valid)
#   FN = GT Filler  + Predicted Valid    (filler lolos, tidak dihapus)
#   TN = GT Valid   + Predicted Valid    (benar pertahankan kata valid)

import os, re, sys, io
from difflib import SequenceMatcher

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── Filler word definitions (sama seperti lexrank.py) ──────────────────────
_FILLER_WORDS_EXACT = {
    "eh","ah","oh","uh","um","em","eem","eee","hmm","hm",
    "nah","ya","yaa","yaaa","iya","iye","iyaa",
    "gitu","kan","lho","lah","nih","sih","deh","kok","dong","tuh",
    "jadi","intinya","pokoknya","kira-kira",
    "terus","trus","kemudian","lalu",
    "udah","oke","baik","ayo","yuk",
}

_FILLER_INLINE_RE = re.compile(
    r'^(?:e{2,}|a{2,}|u{2,}|h{2,}m*|m{2,}|[eEaAuU]{3,})$',
    re.IGNORECASE,
)

_FILLER_START_RE = re.compile(
    r'^(?:(?:nah|ya|jadi|oke|baik|iya|eh|ah|oh|terus|trus|'
    r'gitu|kan|lah|lho|nih|sih|deh|kok|dong|tuh|'
    r'intinya|pokoknya|kemudian|lalu|udah|jadi\s+ya|'
    r'oke\s+ya|baik\s+ya|nah\s+ini|nah\s+itu),?\s*)+',
    re.IGNORECASE,
)
_FILLER_END_RE = re.compile(
    r'(?:\s*,?\s*(?:ya|kan|lho|nih|sih|deh|gitu|dong|tuh|'
    r'gitu\s+ya|gitu\s+kan|ya\s+kan))+[.,]?\s*$',
    re.IGNORECASE,
)
_REPEAT_RE = re.compile(r'\b(\w+)(\s+\1){2,}\b', re.IGNORECASE)
_BRACKET_RE = re.compile(r'\[.*?\]|\(.*?\)')

def apply_filler_removal(text):
    text = _BRACKET_RE.sub(' ', text)
    text = _FILLER_INLINE_RE.sub('', text)
    text = _REPEAT_RE.sub(r'\1', text)
    words = text.split()
    cleaned_words = [w for w in words if w.lower().strip('.,!?;:') not in _FILLER_WORDS_EXACT]
    text = ' '.join(cleaned_words)
    kalimat = re.split(r'(?<=[.!?])\s+', text)
    hasil = []
    for k in kalimat:
        k = _FILLER_START_RE.sub('', k).strip()
        k = re.sub(r'^[,\s]+', '', k)
        k = _FILLER_END_RE.sub('', k).strip()
        if k:
            hasil.append(k)
    text = ' '.join(hasil)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_gt_filler(word):
    """Apakah kata ini termasuk filler menurut ground truth (definisi sistem)?"""
    clean = word.lower().strip('.,!?;:\'"')
    if clean in _FILLER_WORDS_EXACT:
        return True
    if _FILLER_INLINE_RE.match(clean):
        return True
    return False

def baca(path):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return f.read().strip()
        except:
            continue
    raise FileNotFoundError(path)

def hitung_confusion(whisper_raw):
    """Hitung TP/FP/TN/FN per token pada Whisper transcript."""
    whisper_cleaned = apply_filler_removal(whisper_raw)

    # Tokenisasi sederhana (split by whitespace, lowercase)
    w_tokens = whisper_raw.lower().split()
    c_tokens = whisper_cleaned.lower().split()

    # Alignment menggunakan SequenceMatcher untuk menemukan token yang dihapus
    sm = SequenceMatcher(None, w_tokens, c_tokens, autojunk=False)
    removed_indices = set()  # indeks di w_tokens yang dihapus sistem

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'delete':
            for idx in range(i1, i2):
                removed_indices.add(idx)
        # 'replace' bisa berarti terjadi substitusi oleh regex → hitung sebagai dihapus
        elif tag == 'replace':
            # hanya kata yang ukurannya berkurang (delete dominant)
            if (i2 - i1) > (j2 - j1):
                diff = (i2 - i1) - (j2 - j1)
                # anggap diff kata terakhir dari blok ini dihapus
                for idx in range(i2 - diff, i2):
                    removed_indices.add(idx)

    TP = FP = FN = TN = 0
    filler_count = 0
    valid_count  = 0

    for idx, token in enumerate(w_tokens):
        gt_filler     = is_gt_filler(token)
        sys_removed   = idx in removed_indices

        if gt_filler:
            filler_count += 1
            if sys_removed:
                TP += 1   # benar hapus filler
            else:
                FN += 1   # filler lolos
        else:
            valid_count += 1
            if sys_removed:
                FP += 1   # salah hapus kata valid
            else:
                TN += 1   # benar pertahankan kata valid

    return TP, FP, FN, TN, filler_count, valid_count

def metrik(TP, FP, FN, TN):
    P  = TP / (TP + FP) * 100 if (TP + FP) > 0 else 0
    R  = TP / (TP + FN) * 100 if (TP + FN) > 0 else 0
    F1 = 2 * P * R / (P + R)  if (P + R) > 0  else 0
    Ac = (TP + TN) / (TP + TN + FP + FN) * 100 if (TP + TN + FP + FN) > 0 else 0
    return P, R, F1, Ac

# ── Pasangan file ────────────────────────────────────────────────────────────
BASE = r"c:\laragon\www\notulensi_rapat"
HASIL = os.path.join(BASE, r"Hallufilter_uji\Hasil_Uji_Filler_ConfMat.txt")

PASANGAN = [
    {
        "topik": "Basis Data",
        "whisper": r"hasil\transkrip_zoom-meeting-basis-data-sabtu-3-juni-2023-sistem-informasi-universitas-jambi-part-1-ytmp4.savetube.vip_20260619_211533.txt",
    },
    {
        "topik": "K3 Keselamatan Kerja",
        "whisper": r"hasil\transkrip_zoom-bnsp-lsptti-pelatihan-k3-keselamatan-kesehatan-kerja-19-may-2023-break1-13-00-15-45-wib-ytmp4.savetube.vip_20260619_222933.txt",
    },
    {
        "topik": "KWU",
        "whisper": r"hasil\transkrip_Zoom Meeting KWU Sabtu 3 Juni 2023 Sistem Informasi Universitas Jambi - Reza Okto 720p h264_20260620_143855.txt",
    },
    {
        "topik": "Psikologi Sosial",
        "whisper": r"hasil\transkrip_Zoom Meeting   Psikologi Sosial I C 2022 02 23 13 15 57_20260609_222504.txt",
    },
    {
        "topik": "Dasar Manajemen Bisnis",
        "whisper": r"hasil\transkrip_Rekaman Zoom Sesi 1 tanggal 17 September 2020 - Mata Kuliah  Dasar Manajemen dan Bisnis - Lapaq Dosen 360p h264_20260617_213535.txt",
    },
    {
        "topik": "Digital Marketing",
        "whisper": r"hasil\transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture - PENS SKY Venture 1080p h264_2_20260610_214445.txt",
    },
    {
        "topik": "Komisi XI DPR RI",
        "whisper": r"hasil\transkrip_KOMISI XI DPR RI RDP DENGAN 6 DIRJEN KEMENTERIAN KEUANGAN_20260618_011634.txt",
    },
    {
        "topik": "ESG & QHSE",
        "whisper": r"hasil\transkrip_implementasi-esg-and-qhse-integrasi-bagi-daya-saing-usaha-zoom-meeting-conference-ytmp4.savetube.vip_20260619_231835.txt",
    },
    {
        "topik": "Ilmu Komunikasi",
        "whisper": r"hasil\transkrip_FULL HD VIDEO SIARAN ULANG ZOOM ILMU KOMUNIKASI - Dwii HS 480p_20260620_000940.txt",
    },
]

SEP = "-" * 110

lines = []
lines.append("=" * 110)
lines.append("  HASIL PENGUJIAN WORD FILLER REMOVAL — CONFUSION MATRIX")
lines.append("  Precision, Recall, F1-Score, dan Accuracy")
lines.append("=" * 110)

# ── Kumpulkan data semua topik ───────────────────────────────────────────────
all_data = []  # (topik, fc, vc, TP_after, FP_after, FN_after, TN_after)
for p in PASANGAN:
    w_path = os.path.join(BASE, p["whisper"])
    w_raw  = baca(w_path)
    TP, FP, FN, TN, fc, vc = hitung_confusion(w_raw)
    all_data.append((p["topik"], fc, vc, TP, FP, FN, TN))

# ══════════════════════════════════════════════════════════════════════════════
# TABEL 1 — SEBELUM WORD FILLER REMOVAL (BASELINE)
# Sebelum sistem aktif: tidak ada kata yang dihapus
#   TP = 0  (tidak ada filler yang dihapus)
#   FP = 0  (tidak ada kata yang dihapus sama sekali)
#   FN = fc (semua filler lolos / tidak terdeteksi)
#   TN = vc (semua kata valid dipertahankan — benar, tapi bukan karena sistem)
# ══════════════════════════════════════════════════════════════════════════════
lines.append(f"\n{'=' * 110}")
lines.append("  TABEL 1 — SEBELUM WORD FILLER REMOVAL (Baseline: sistem tidak aktif)")
lines.append(f"{'=' * 110}")
lines.append(f"{'No':<4} {'Topik Rapat':<26} "
             f"{'TP':>7} {'FP':>7} {'FN':>7} {'TN':>8} "
             f"{'Precision (%)':>14} {'Recall (%)':>11} {'F1-Score (%)':>13} {'Accuracy (%)':>13}")
lines.append(SEP)

bef_rows = []
tot_bTP = tot_bFP = tot_bFN = tot_bTN = 0
for no, (topik, fc, vc, *_) in enumerate(all_data, 1):
    bTP, bFP, bFN, bTN = 0, 0, fc, vc
    tot_bTP += bTP; tot_bFP += bFP; tot_bFN += bFN; tot_bTN += bTN
    bP, bR, bF1, bAc = metrik(bTP, bFP, bFN, bTN)
    lines.append(f"{no:<4} {topik:<26} "
                 f"{bTP:>7} {bFP:>7} {bFN:>7} {bTN:>8} "
                 f"{bP:>14.2f} {bR:>11.2f} {bF1:>13.2f} {bAc:>13.2f}")
    bef_rows.append((no, topik, bTP, bFP, bFN, bTN, bP, bR, bF1, bAc))

lines.append(SEP)
tbP, tbR, tbF1, tbAc = metrik(tot_bTP, tot_bFP, tot_bFN, tot_bTN)
lines.append(f"{'':4} {'RATA-RATA / GABUNGAN':<26} "
             f"{tot_bTP:>7} {tot_bFP:>7} {tot_bFN:>7} {tot_bTN:>8} "
             f"{tbP:>14.2f} {tbR:>11.2f} {tbF1:>13.2f} {tbAc:>13.2f}")
lines.append(SEP)

# ══════════════════════════════════════════════════════════════════════════════
# TABEL 2 — SESUDAH WORD FILLER REMOVAL
# ══════════════════════════════════════════════════════════════════════════════
lines.append(f"\n{'=' * 110}")
lines.append("  TABEL 2 — SESUDAH WORD FILLER REMOVAL (Sistem aktif)")
lines.append(f"{'=' * 110}")
lines.append(f"{'No':<4} {'Topik Rapat':<26} "
             f"{'Kata Filler (GT)':>16} {'Kata Valid (GT)':>15} "
             f"{'TP':>7} {'FP':>7} {'FN':>7} {'TN':>8}")
lines.append(SEP)

metrik_rows = []
tot_TP = tot_FP = tot_FN = tot_TN = 0
for no, (topik, fc, vc, TP, FP, FN, TN) in enumerate(all_data, 1):
    tot_TP += TP; tot_FP += FP; tot_FN += FN; tot_TN += TN
    P, R, F1, Ac = metrik(TP, FP, FN, TN)
    lines.append(f"{no:<4} {topik:<26} {fc:>16} {vc:>15} {TP:>7} {FP:>7} {FN:>7} {TN:>8}")
    metrik_rows.append((no, topik, TP, FP, FN, TN, P, R, F1, Ac))

lines.append(SEP)
tP, tR, tF1, tAc = metrik(tot_TP, tot_FP, tot_FN, tot_TN)
lines.append(f"{'':4} {'TOTAL / GABUNGAN':<26} "
             f"{'':>16} {'':>15} "
             f"{tot_TP:>7} {tot_FP:>7} {tot_FN:>7} {tot_TN:>8}")

# ── Tabel Metrik Sesudah ─────────────────────────────────────────────────────
lines.append(f"\n{'=' * 110}")
lines.append("  TABEL METRIK EVALUASI SESUDAH FILLER REMOVAL: PRECISION, RECALL, F1-SCORE, ACCURACY")
lines.append(f"{'=' * 110}")
lines.append(f"{'No':<4} {'Topik Rapat':<26} "
             f"{'TP':>6} {'FP':>6} {'FN':>6} {'TN':>7} "
             f"{'Precision (%)':>14} {'Recall (%)':>11} {'F1-Score (%)':>13} {'Accuracy (%)':>13}")
lines.append(SEP)

for no, topik, TP, FP, FN, TN, P, R, F1, Ac in metrik_rows:
    lines.append(f"{no:<4} {topik:<26} "
                 f"{TP:>6} {FP:>6} {FN:>6} {TN:>7} "
                 f"{P:>14.2f} {R:>11.2f} {F1:>13.2f} {Ac:>13.2f}")

lines.append(SEP)
lines.append(f"{'':4} {'RATA-RATA / GABUNGAN':<26} "
             f"{tot_TP:>6} {tot_FP:>6} {tot_FN:>6} {tot_TN:>7} "
             f"{tP:>14.2f} {tR:>11.2f} {tF1:>13.2f} {tAc:>13.2f}")
lines.append(SEP)

# ── Tabel Perbandingan Sebelum vs Sesudah ────────────────────────────────────
lines.append(f"\n{'=' * 110}")
lines.append("  TABEL PERBANDINGAN SEBELUM vs SESUDAH WORD FILLER REMOVAL")
lines.append(f"{'=' * 110}")
lines.append(f"{'No':<4} {'Topik Rapat':<26} "
             f"{'Prec Sblm':>10} {'Prec Ssdh':>10} "
             f"{'Rec Sblm':>9} {'Rec Ssdh':>9} "
             f"{'F1 Sblm':>8} {'F1 Ssdh':>8} "
             f"{'Acc Sblm':>9} {'Acc Ssdh':>9}")
lines.append(SEP)

for (no, topik, bTP, bFP, bFN, bTN, bP, bR, bF1, bAc), \
    (_, _t2, TP, FP, FN, TN, P, R, F1, Ac) in zip(bef_rows, metrik_rows):
    lines.append(f"{no:<4} {topik:<26} "
                 f"{bP:>9.2f}% {P:>9.2f}% "
                 f"{bR:>8.2f}% {R:>8.2f}% "
                 f"{bF1:>7.2f}% {F1:>7.2f}% "
                 f"{bAc:>8.2f}% {Ac:>8.2f}%")
lines.append(SEP)
lines.append(f"{'':4} {'RATA-RATA':<26} "
             f"{tbP:>9.2f}% {tP:>9.2f}% "
             f"{tbR:>8.2f}% {tR:>8.2f}% "
             f"{tbF1:>7.2f}% {tF1:>7.2f}% "
             f"{tbAc:>8.2f}% {tAc:>8.2f}%")
lines.append(SEP)

lines.append(f"""
KETERANGAN:
  TP (True Positive)  = Kata filler yang BENAR dihapus sistem
  FP (False Positive) = Kata VALID (bukan filler) yang SALAH dihapus sistem
  FN (False Negative) = Kata filler yang LOLOS / TIDAK dihapus sistem
  TN (True Negative)  = Kata valid yang BENAR dipertahankan sistem

  Precision = TP / (TP + FP)
  Recall    = TP / (TP + FN)
  F1-Score  = 2 x (Precision x Recall) / (Precision + Recall)
  Accuracy  = (TP + TN) / (TP + TN + FP + FN)

  Ground Truth Filler  = kata ada di kamus FILLER_WORDS_EXACT atau cocok regex inline
  Ground Truth Valid   = kata tidak termasuk kategori filler di atas
""")

output = "\n".join(lines)
with open(HASIL, "w", encoding="utf-8") as f:
    f.write(output)

print(output)
print(f"\nFile disimpan di: {HASIL}")
