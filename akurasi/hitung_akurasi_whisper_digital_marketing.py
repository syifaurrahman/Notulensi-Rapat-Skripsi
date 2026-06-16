# hitung_akurasi_whisper_digital_marketing.py
# ==============================================
# Hitung WER, WAcc, CER antara:
#   - Transkripsi Whisper (hypothesis)
#   - Transkripsi manual (reference)
# untuk file Digital Marketing PENS SKY Venture
#
# Output: akurasi/whisper/hasil_akurasi_whisper_digital_marketing.txt

import os
import re
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── PATH ──────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR  = os.path.dirname(BASE_DIR)

WHISPER_FILE = os.path.join(
    PARENT_DIR, "hasil",
    "transkrip_Mentoring Digital Marketing Melalui Zoom Meeting PENS SKY Venture - PENS SKY Venture 1080p h264_2_20260610_214445.txt"
)

MANUAL_FILE = os.path.join(
    PARENT_DIR, "hasil", "manual transkripsi",
    "Manual_transkripsi_digitalmarketing.txt"
)

OUTPUT_DIR  = os.path.join(BASE_DIR, "whisper")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "hasil_akurasi_whisper_digital_marketing.txt")


# ── NORMALISASI ───────────────────────────────────────────────
def normalize_text(text):
    text = text.lower()
    # Hapus tanda baca
    text = re.sub(r"[.,!?;:\"()\[\]{}\-—–/\\|<>@#$%^&*+=~`]", " ", text)
    # Hapus frasa halusinasi Whisper
    halusinasi = [
        "terima kasih kerana menonton",
        "terima kasih sudah menonton",
        "terima kasih telah menonton",
        "selamat tinggal",
    ]
    for frasa in halusinasi:
        text = re.sub(re.escape(frasa), " ", text, flags=re.IGNORECASE)
    # Normalisasi spasi
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ── BACA FILE ─────────────────────────────────────────────────
def read_whisper_transcript(filepath):
    """Baca transkripsi Whisper, skip header sampai baris ========."""
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
    return normalize_text(" ".join(content))


def read_manual_transcript(filepath):
    """Baca transkripsi manual, skip header/metadata markdown."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    content = []
    started = False
    for line in lines:
        stripped = line.strip()
        # Skip header markdown sampai garis ---
        if not started:
            if stripped == "---" and len(content) == 0:
                # Pertama kali ketemu ---, mungkin awal front-matter
                continue
            if stripped.startswith("#") or stripped.startswith("**") or stripped == "---" or stripped == "":
                continue
            started = True
        if started:
            # Skip baris yang masih markdown header
            if stripped.startswith("## ") or stripped.startswith("**File") or stripped.startswith("**Dibuat") or stripped.startswith("**Model"):
                continue
            if stripped == "---":
                continue
            # Juga skip baris keterangan revisi di awal
            if "saya memahami instruksi" in stripped.lower() or "hanya berfokus" in stripped.lower() or "tetap dipertahankan" in stripped.lower():
                continue
            content.append(line)
    return normalize_text(" ".join(content))


# ── HITUNG WER/CER DENGAN JIWER ──────────────────────────────
def hitung_akurasi(ref_text, hyp_text):
    """Hitung WER, CER menggunakan jiwer library."""
    try:
        import jiwer
    except ImportError:
        print("[ERROR] Library jiwer belum terinstall.")
        print("        Jalankan: pip install jiwer")
        sys.exit(1)

    # WER
    wer_result = jiwer.process_words(ref_text, hyp_text)
    wer  = wer_result.wer
    wacc = max(0.0, 1.0 - wer)

    # Detail error
    S = wer_result.substitutions
    D = wer_result.deletions
    I = wer_result.insertions
    H = wer_result.hits
    N = S + D + H  # total kata referensi

    # CER
    cer_result = jiwer.process_characters(ref_text, hyp_text)
    cer = cer_result.cer

    return {
        "wer": wer, "wacc": wacc, "cer": cer,
        "S": S, "D": D, "I": I, "H": H, "N": N,
        "ref_words": len(ref_text.split()),
        "hyp_words": len(hyp_text.split()),
    }


# ── MAIN ──────────────────────────────────────────────────────
def main():
    now = datetime.now().strftime("%d %B %Y, %H:%M:%S")

    print("=" * 62)
    print("  HITUNG AKURASI WHISPER — Digital Marketing")
    print("=" * 62)

    # Baca file
    print(f"\n[1] Membaca transkripsi Whisper...")
    if not os.path.exists(WHISPER_FILE):
        print(f"[ERROR] File tidak ditemukan: {WHISPER_FILE}")
        sys.exit(1)
    hyp = read_whisper_transcript(WHISPER_FILE)
    print(f"    {len(hyp.split())} kata (setelah normalisasi)")

    print(f"[2] Membaca transkripsi manual...")
    if not os.path.exists(MANUAL_FILE):
        print(f"[ERROR] File tidak ditemukan: {MANUAL_FILE}")
        sys.exit(1)
    ref = read_manual_transcript(MANUAL_FILE)
    print(f"    {len(ref.split())} kata (setelah normalisasi)")

    # Hitung akurasi
    print("[3] Menghitung WER, WAcc, CER...")
    r = hitung_akurasi(ref, hyp)

    # Penilaian
    wer_pct = r["wer"] * 100
    cer_pct = r["cer"] * 100
    wacc_pct = r["wacc"] * 100

    if wer_pct < 5:
        wer_rating = "Sangat Baik ✓✓"
    elif wer_pct < 10:
        wer_rating = "Baik ✓"
    elif wer_pct < 20:
        wer_rating = "Cukup ~"
    else:
        wer_rating = "Perlu Peningkatan ✗"

    if cer_pct < 5:
        cer_rating = "Sangat Baik ✓✓"
    elif cer_pct < 10:
        cer_rating = "Baik ✓"
    elif cer_pct < 20:
        cer_rating = "Cukup ~"
    else:
        cer_rating = "Perlu Peningkatan ✗"

    # Format output
    sep  = "=" * 62
    sep2 = "-" * 62
    lines = []
    lines.append(sep)
    lines.append("  HASIL PENGUJIAN AKURASI WHISPER")
    lines.append("  Sistem Notulensia — Transkripsi Digital Marketing")
    lines.append(sep)
    lines.append(f"  Tanggal     : {now}")
    lines.append(f"  Metode      : jiwer (library)")
    lines.append(f"  File Ref    : Manual_transkripsi_digitalmarketing.txt")
    lines.append(f"  File Hyp    : transkrip_...Digital Marketing...214445.txt")
    lines.append(f"  Kata Ref    : {r['ref_words']}")
    lines.append(f"  Kata Hyp    : {r['hyp_words']}")
    lines.append(sep2)
    lines.append("")
    lines.append("  METRIK UTAMA")
    lines.append("  " + "─" * 42)
    lines.append(f"  WER   (Word Error Rate)     : {wer_pct:8.2f}%")
    lines.append(f"  WAcc  (Word Accuracy)       : {wacc_pct:8.2f}%")
    lines.append(f"  CER   (Character Error Rate): {cer_pct:8.2f}%")
    lines.append("")
    lines.append("  DETAIL ERROR (Word-level)")
    lines.append("  " + "─" * 42)
    lines.append(f"  Substitutions (S) : {r['S']:>6}")
    lines.append(f"  Deletions     (D) : {r['D']:>6}")
    lines.append(f"  Insertions    (I) : {r['I']:>6}")
    lines.append(f"  Hits          (H) : {r['H']:>6}")
    lines.append(f"  Total Ref     (N) : {r['N']:>6}")
    lines.append("")
    lines.append("  PENILAIAN")
    lines.append("  " + "─" * 42)
    lines.append(f"  Kualitas WER  :  {wer_rating}")
    lines.append(f"  Kualitas CER  :  {cer_rating}")
    lines.append("")
    lines.append(sep)
    lines.append("  CATATAN:")
    lines.append("  - WER ideal untuk speech-to-text: < 10%")
    lines.append("  - WAcc = 100% - WER")
    lines.append("  - CER lebih ketat karena dihitung per karakter")
    lines.append("  - Normalisasi: lowercase, hapus tanda baca,")
    lines.append("    hapus frasa halusinasi Whisper")
    lines.append(sep)

    hasil = "\n".join(lines)
    print("\n" + hasil)

    # Simpan
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(hasil + "\n")
    print(f"\nHasil disimpan ke: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
