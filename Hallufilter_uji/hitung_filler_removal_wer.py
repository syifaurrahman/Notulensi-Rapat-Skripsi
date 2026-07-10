# hitung_filler_removal_wer.py
# Menghitung WER sebelum dan sesudah Word Filler Removal
# menggunakan 9 file transkrip Whisper vs 9 file transkripsi manual

import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from jiwer import process_words, process_characters

# ── Filler words regex (sama persis dengan lexrank.py) ─────────────────────
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
_FILLER_INLINE_RE = re.compile(
    r'\b(e{2,}|a{2,}|u{2,}|h{2,}m+|[eEaAuU]{3,})\b',
    re.IGNORECASE,
)
_FILLER_WORDS_EXACT = {
    "eh","ah","oh","uh","um","em","eem","eee","hmm","hm",
    "nah","ya","yaa","yaaa","iya","iye","iyaa",
    "gitu","kan","lho","lah","nih","sih","deh","kok","dong","tuh",
    "jadi","intinya","pokoknya","kira-kira",
    "terus","trus","kemudian","lalu",
    "udah","oke","baik","ayo","yuk",
}
_REPEAT_RE = re.compile(r'\b(\w+)(\s+\1){2,}\b', re.IGNORECASE)
_BRACKET_RE = re.compile(r'\[.*?\]|\(.*?\)')

def apply_filler_removal(text):
    """Terapkan filler removal seperti di lexrank.py Step 1 dan Step 3."""
    # Hapus bracket artifacts
    text = _BRACKET_RE.sub(' ', text)
    # Hapus filler inline (eee, mmm, dll)
    text = _FILLER_INLINE_RE.sub('', text)
    # Hapus pengulangan kata > 2x
    text = _REPEAT_RE.sub(r'\1', text)
    # Hapus filler pendek berdiri sendiri (kata tunggal)
    words = text.split()
    cleaned_words = [w for w in words if w.lower().strip('.,!?') not in _FILLER_WORDS_EXACT]
    text = ' '.join(cleaned_words)
    # Hapus filler di awal dan akhir per kalimat
    kalimat = re.split(r'(?<=[.!?])\s+', text)
    hasil = []
    for k in kalimat:
        k = _FILLER_START_RE.sub('', k).strip()
        k = re.sub(r'^[,\s]+', '', k)
        k = _FILLER_END_RE.sub('', k).strip()
        if k:
            hasil.append(k)
    text = ' '.join(hasil)
    # Normalisasi spasi ganda
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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
    teks = re.sub(r'[^\w\s]', ' ', teks)
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks

def hitung(ref_raw, hyp_raw):
    ref = normalisasi(ref_raw)
    hyp = normalisasi(hyp_raw)
    wout = process_words(ref, hyp)
    cout = process_characters(ref, hyp)
    S = wout.substitutions
    D = wout.deletions
    I = wout.insertions
    N = len(ref.split())
    H = N - S - D
    WER = (S + D + I) / N * 100 if N > 0 else 0
    WAcc = max(0, (N - S - D - I) / N * 100) if N > 0 else 0
    CER = (cout.substitutions + cout.deletions + cout.insertions) / max(1, len(ref.replace(' ', ''))) * 100
    return N, len(hyp.split()), S, D, I, H, WER, WAcc, CER

# ── Pasangan file (manual, whisper) ─────────────────────────────────────────
BASE = r"c:\laragon\www\notulensi_rapat"
HASIL = os.path.join(BASE, r"Hallufilter_uji\Hasil_Uji_Filler_WER.txt")

PASANGAN = [
    {
        "topik": "Basis Data",
        "manual": r"hasil\manual transkripsi\zoom_meeting_basis_data.txt",
        "whisper": r"hasil\transkrip_zoom-meeting-basis-data-sabtu-3-juni-2023-sistem-informasi-universitas-jambi-part-1-ytmp4.savetube.vip_20260619_211533.txt",
    },
    {
        "topik": "K3 Keselamatan Kerja",
        "manual": r"hasil\manual transkripsi\zoom materi keselamatan kerja.txt",
        "whisper": r"hasil\transkrip_zoom-bnsp-lsptti-pelatihan-k3-keselamatan-kesehatan-kerja-19-may-2023-break1-13-00-15-45-wib-ytmp4.savetube.vip_20260619_222933.txt",
    },
    {
        "topik": "KWU",
        "manual": r"hasil\manual transkripsi\Zoom Meeting Kwu.txt",
        "whisper": r"hasil\transkrip_Zoom Meeting KWU Sabtu 3 Juni 2023 Sistem Informasi Universitas Jambi - Reza Okto 720p h264_20260620_143855.txt",
    },
    {
        "topik": "Psikologi Sosial",
        "manual": r"hasil\manual transkripsi\Manual_transkrip_Psikologi.txt",
        "whisper": r"hasil\transkrip_Zoom Meeting   Psikologi Sosial I C 2022 02 23 13 15 57_20260609_222504.txt",
    },
    {
        "topik": "Dasar Manajemen Bisnis",
        "manual": r"hasil\manual transkripsi\manual Rekaman Zoom Sesi 1 Tanggal 17 September 2020 - Mata Kuliah Dasar Manajemen Dan Bisnis - Lapaq Dosen 360P H264.txt",
        "whisper": r"hasil\transkrip_Rekaman Zoom Sesi 1 tanggal 17 September 2020 - Mata Kuliah  Dasar Manajemen dan Bisnis - Lapaq Dosen 360p h264_20260617_213535.txt",
    },
    {
        "topik": "Digital Marketing",
        "manual": r"hasil\manual transkripsi\Manual_transkripsi_digitalmarketing.txt",
        "whisper": r"hasil\transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture - PENS SKY Venture 1080p h264_2_20260610_214445.txt",
    },
    {
        "topik": "Komisi XI DPR RI",
        "manual": r"hasil\manual transkripsi\Rapat_komisi_dpr.txt",
        "whisper": r"hasil\transkrip_KOMISI XI DPR RI RDP DENGAN 6 DIRJEN KEMENTERIAN KEUANGAN_20260618_011634.txt",
    },
    {
        "topik": "ESG & QHSE",
        "manual": r"hasil\manual transkripsi\meeting esg and qhse.txt",
        "whisper": r"hasil\transkrip_implementasi-esg-and-qhse-integrasi-bagi-daya-saing-usaha-zoom-meeting-conference-ytmp4.savetube.vip_20260619_231835.txt",
    },
    {
        "topik": "Ilmu Komunikasi",
        "manual": r"hasil\manual transkripsi\ilmu komunikasi.txt",
        "whisper": r"hasil\transkrip_FULL HD VIDEO SIARAN ULANG ZOOM ILMU KOMUNIKASI - Dwii HS 480p_20260620_000940.txt",
    },
]

lines = []
lines.append("=" * 100)
lines.append("  LAPORAN PENGUJIAN WORD FILLER REMOVAL — WER/WAcc/CER SEBELUM DAN SESUDAH")
lines.append("=" * 100)

SEP = "-" * 100

def print_tabel_header(label):
    lines.append(f"\n{'=' * 100}")
    lines.append(f"  {label}")
    lines.append(f"{'=' * 100}")
    lines.append(f"{'No':<4} {'Topik Rapat':<26} {'Ref Kata':>9} {'Kata Hipo':>9} {'S':>5} {'D':>5} {'I':>5} {'H':>6} {'WER (%)':>9} {'WAcc (%)':>9} {'CER (%)':>9}")
    lines.append(SEP)

def print_tabel_baris(no, topik, N, Nhyp, S, D, I, H, WER, WAcc, CER):
    lines.append(f"{no:<4} {topik:<26} {N:>9} {Nhyp:>9} {S:>5} {D:>5} {I:>5} {H:>6} {WER:>9.2f} {WAcc:>9.2f} {CER:>9.2f}")

def print_tabel_footer(tot_N, tot_Nhyp, tot_S, tot_D, tot_I, tot_H, avg_WER, avg_WAcc, avg_CER):
    lines.append(SEP)
    lines.append(f"{'':4} {'Rata-rata':<26} {tot_N:>9} {tot_Nhyp:>9} {tot_S:>5} {tot_D:>5} {tot_I:>5} {tot_H:>6} {avg_WER:>9.2f} {avg_WAcc:>9.2f} {avg_CER:>9.2f}")

# ── Hitung semua data ───────────────────────────────────────────────────────
hasil_before = []
hasil_after  = []

for p in PASANGAN:
    manual_path  = os.path.join(BASE, p["manual"])
    whisper_path = os.path.join(BASE, p["whisper"])
    
    manual_raw  = baca(manual_path)
    whisper_raw = baca(whisper_path)
    
    # Before filler removal
    N_b, Nhyp_b, S_b, D_b, I_b, H_b, WER_b, WAcc_b, CER_b = hitung(manual_raw, whisper_raw)
    hasil_before.append((p["topik"], N_b, Nhyp_b, S_b, D_b, I_b, H_b, WER_b, WAcc_b, CER_b))
    
    # After filler removal (terapkan ke whisper, BUKAN ke manual)
    whisper_cleaned = apply_filler_removal(whisper_raw)
    N_a, Nhyp_a, S_a, D_a, I_a, H_a, WER_a, WAcc_a, CER_a = hitung(manual_raw, whisper_cleaned)
    hasil_after.append((p["topik"], N_a, Nhyp_a, S_a, D_a, I_a, H_a, WER_a, WAcc_a, CER_a))

# ── Tabel 1: Sebelum Filler Removal ────────────────────────────────────────
print_tabel_header("TABEL 1: SEBELUM WORD FILLER REMOVAL (Raw Whisper vs Manual)")
sum_N=sum_Nhyp=sum_S=sum_D=sum_I=sum_H=sum_WER=sum_WAcc=sum_CER=0
for no, (topik, N, Nhyp, S, D, I, H, WER, WAcc, CER) in enumerate(hasil_before, 1):
    print_tabel_baris(no, topik, N, Nhyp, S, D, I, H, WER, WAcc, CER)
    sum_N+=N; sum_Nhyp+=Nhyp; sum_S+=S; sum_D+=D; sum_I+=I; sum_H+=H
    sum_WER+=WER; sum_WAcc+=WAcc; sum_CER+=CER
n = len(hasil_before)
print_tabel_footer(sum_N, sum_Nhyp, sum_S, sum_D, sum_I, sum_H,
                   sum_WER/n, sum_WAcc/n, sum_CER/n)

# ── Tabel 2: Sesudah Filler Removal ─────────────────────────────────────────
print_tabel_header("TABEL 2: SESUDAH WORD FILLER REMOVAL (Cleaned Whisper vs Manual)")
sum_N=sum_Nhyp=sum_S=sum_D=sum_I=sum_H=sum_WER=sum_WAcc=sum_CER=0
for no, (topik, N, Nhyp, S, D, I, H, WER, WAcc, CER) in enumerate(hasil_after, 1):
    print_tabel_baris(no, topik, N, Nhyp, S, D, I, H, WER, WAcc, CER)
    sum_N+=N; sum_Nhyp+=Nhyp; sum_S+=S; sum_D+=D; sum_I+=I; sum_H+=H
    sum_WER+=WER; sum_WAcc+=WAcc; sum_CER+=CER
n = len(hasil_after)
print_tabel_footer(sum_N, sum_Nhyp, sum_S, sum_D, sum_I, sum_H,
                   sum_WER/n, sum_WAcc/n, sum_CER/n)

# ── Tabel 3: Perbandingan delta ─────────────────────────────────────────────
lines.append(f"\n{'=' * 100}")
lines.append("  TABEL REKAPITULASI: PERBANDINGAN WER / WAcc SEBELUM vs SESUDAH FILLER REMOVAL")
lines.append(f"{'=' * 100}")
lines.append(f"{'No':<4} {'Topik Rapat':<26} {'WER Sebelum':>12} {'WER Sesudah':>12} {'WAcc Sebelum':>13} {'WAcc Sesudah':>13} {'Delta WAcc':>11}")
lines.append(SEP)
for i, ((topik, *_, WER_b, WAcc_b, _), (_, *__, WER_a, WAcc_a, __)) in enumerate(zip(hasil_before, hasil_after), 1):
    delta = WAcc_a - WAcc_b
    lines.append(f"{i:<4} {topik:<26} {WER_b:>12.2f}% {WER_a:>12.2f}% {WAcc_b:>13.2f}% {WAcc_a:>13.2f}% {delta:>+10.2f}%")
lines.append(SEP)

# Simpan dan print
output = "\n".join(lines)
with open(HASIL, "w", encoding="utf-8") as f:
    f.write(output)

print(output)
print(f"\n\nFile disimpan di: {HASIL}")
