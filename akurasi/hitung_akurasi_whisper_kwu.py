# hitung_akurasi_whisper_kwu.py
# =============================================
# Hitung WER, WAcc, CER antara:
#   - Transkripsi Whisper (hypothesis)
#   - Transkripsi manual (reference)
# untuk file Zoom Meeting KWU
#
# Output: akurasi/Whisper/zoom meeting kwu.txt

import os
import re
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── PATH ──────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

WHISPER_FILE = os.path.join(
    PARENT_DIR, "hasil",
    "transkrip_Zoom Meeting KWU Sabtu 3 Juni 2023 Sistem Informasi Universitas Jambi - Reza Okto 720p h264_20260620_143855.txt"
)

MANUAL_FILE = os.path.join(
    PARENT_DIR, "hasil", "manual transkripsi",
    "Zoom Meeting Kwu.txt"
)

OUTPUT_DIR  = os.path.join(BASE_DIR, "Whisper")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "zoom meeting kwu.txt")


# ── NORMALISASI ───────────────────────────────────────────────
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[.,!?;:\"()\[\]{}\-—–/\\|<>@#$%^&*+=~`]", " ", text)
    halusinasi = [
        "terima kasih kerana menonton",
        "terima kasih sudah menonton",
        "terima kasih telah menonton",
        "selamat tinggal",
        "subscribe",
    ]
    for frasa in halusinasi:
        text = re.sub(re.escape(frasa), " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ── BACA FILE WHISPER ─────────────────────────────────────────
def read_whisper_transcript(filepath):
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


# ── BACA FILE MANUAL ──────────────────────────────────────────
def read_manual_transcript(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    content = []
    started = False
    for line in lines:
        stripped = line.strip()
        if not started:
            if stripped == "" or stripped == "---":
                continue
            if any(k in stripped.lower() for k in [
                "berikut adalah", "penulisan ulang", "saya memahami",
                "hanya berfokus", "tetap dipertahankan", "transkripsi",
                "file video", "dibuat", "model", "===", "koreksi pada"
            ]):
                continue
            started = True
        if started:
            if stripped == "---":
                continue
            content.append(line)
    return normalize_text(" ".join(content))


# ── HITUNG WER/CER ────────────────────────────────────────────
def hitung_akurasi(ref_text, hyp_text):
    try:
        import jiwer
    except ImportError:
        print("[ERROR] Library jiwer belum terinstall. Jalankan: pip install jiwer")
        sys.exit(1)

    wer_result = jiwer.process_words(ref_text, hyp_text)
    wer  = wer_result.wer
    wacc = max(0.0, 1.0 - wer)
    S = wer_result.substitutions
    D = wer_result.deletions
    I = wer_result.insertions
    H = wer_result.hits
    N = S + D + H

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
    print("  HITUNG AKURASI WHISPER — Zoom Meeting KWU")
    print("=" * 62)

    print(f"\n[1] Membaca transkripsi Whisper...")
    if not os.path.exists(WHISPER_FILE):
        print(f"[ERROR] File tidak ditemukan:\n  {WHISPER_FILE}")
        sys.exit(1)
    hyp = read_whisper_transcript(WHISPER_FILE)
    print(f"    {len(hyp.split())} kata (setelah normalisasi)")

    print(f"[2] Membaca transkripsi manual...")
    if not os.path.exists(MANUAL_FILE):
        print(f"[ERROR] File tidak ditemukan:\n  {MANUAL_FILE}")
        sys.exit(1)
    ref = read_manual_transcript(MANUAL_FILE)
    print(f"    {len(ref.split())} kata (setelah normalisasi)")

    print("[3] Menghitung WER, WAcc, CER...")
    r = hitung_akurasi(ref, hyp)

    wer_pct  = r["wer"]  * 100
    cer_pct  = r["cer"]  * 100
    wacc_pct = r["wacc"] * 100

    def wer_rating(v):
        if v < 5:   return "Sangat Baik ✓✓"
        if v < 10:  return "Baik ✓"
        if v < 20:  return "Cukup ~"
        return "Perlu Peningkatan ✗"

    def cer_rating(v):
        if v < 5:   return "Sangat Baik ✓✓"
        if v < 10:  return "Baik ✓"
        if v < 20:  return "Cukup ~"
        return "Perlu Peningkatan ✗"

    sep  = "=" * 62
    sep2 = "-" * 62
    lines = []
    lines.append(sep)
    lines.append("  HASIL PENGUJIAN AKURASI WHISPER")
    lines.append("  Sistem Notulensi — Zoom Meeting KWU")
    lines.append("  Sistem Informasi Universitas Jambi")
    lines.append(sep)
    lines.append(f"  Tanggal     : {now}")
    lines.append(f"  Metode      : jiwer (WER / CER)")
    lines.append(f"  File Ref    : Zoom Meeting Kwu.txt")
    lines.append(f"  File Hyp    : transkrip_Zoom Meeting KWU Sabtu 3 Juni 2023..._20260620_143855.txt")
    lines.append(f"  Kata Ref    : {r['ref_words']:,}")
    lines.append(f"  Kata Hyp    : {r['hyp_words']:,}")
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
    lines.append(f"  Kualitas WER  :  {wer_rating(wer_pct)}")
    lines.append(f"  Kualitas CER  :  {cer_rating(cer_pct)}")
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

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(hasil + "\n")
    print(f"\nHasil disimpan ke: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
