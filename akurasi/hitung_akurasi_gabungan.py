"""
=============================================================
  HITUNG AKURASI GABUNGAN SISTEM NOTULENSIA
  Menggabungkan: Whisper (WER) + LexRank (ROUGE-L) + LLM (ROUGE-L)
  menjadi 1 nilai akurasi keseluruhan sistem (0-100%)
=============================================================
"""

import sys, os
# Fix encoding Windows console agar bisa cetak UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

"""

  METODOLOGI:
  -----------
  Sistem Notulensia terdiri dari 3 komponen pipeline berurutan:
    1. Whisper  → Transkripsi audio ke teks
    2. LexRank  → Meringkas teks secara ekstraktif
    3. LLM      → Menyempurnakan ringkasan secara generatif

  Nilai dari setiap komponen dinormalisasi ke skala 0-100%:
    - Whisper  : WAcc (Word Accuracy) = 100% - WER  → Higher is better
    - LexRank  : ROUGE-L F1 Score                   → Higher is better
    - LLM      : ROUGE-L F1 Score                   → Higher is better

  Bobot (Weight) per komponen:
    - Whisper  : 50% — Fondasi utama, jika transkripsi salah maka
                       seluruh pipeline gagal
    - LexRank  : 25% — Peran ekstraksi kunci
    - LLM      : 25% — Peran penyempurnaan

  Formula:
    Akurasi Gabungan = (W_whisper × Skor_Whisper)
                     + (W_lexrank × Skor_LexRank)
                     + (W_llm    × Skor_LLM)

=============================================================
"""

import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  NILAI AKURASI DARI MASING-MASING KOMPONEN
#  (Ambil dari hasil pengujian yang sudah ada)
# ─────────────────────────────────────────────────────────────

# --- Komponen 1: Whisper (Transkripsi) ---
# Sumber: hasil_akurasi.txt
WER        = 6.96    # Word Error Rate (%)
WAcc       = 100.0 - WER   # = 93.04%  (Word Accuracy)
CER        = 4.89    # Character Error Rate (%)
CAcc       = 100.0 - CER   # = 95.11%  (Char Accuracy)

# Skor Whisper = rata-rata Word Accuracy dan Char Accuracy
# (lebih robust daripada hanya WAcc)
skor_whisper = (WAcc + CAcc) / 2   # = 94.075%

# --- Komponen 2: LexRank (Summarization Ekstraktif) ---
# Sumber: hasil_akurasi_lexrank.txt
rouge1_lexrank = 24.02   # ROUGE-1 F1 (%)
rouge2_lexrank =  4.33   # ROUGE-2 F1 (%)
rougeL_lexrank = 10.80   # ROUGE-L F1 (%)

# Skor LexRank = weighted avg ROUGE (ROUGE-L paling representatif)
# Bobot: R1=0.25, R2=0.25, RL=0.50
skor_lexrank = (0.25 * rouge1_lexrank
              + 0.25 * rouge2_lexrank
              + 0.50 * rougeL_lexrank)

# --- Komponen 3: LLM Ollama (Summarization Generatif) ---
# Sumber: hasil_akurasi_llm.txt
rouge1_llm = 17.39   # ROUGE-1 F1 (%)
rouge2_llm =  0.51   # ROUGE-2 F1 (%)
rougeL_llm = 10.23   # ROUGE-L F1 (%)

# Skor LLM = weighted avg ROUGE (sama dengan LexRank)
skor_llm = (0.25 * rouge1_llm
           + 0.25 * rouge2_llm
           + 0.50 * rougeL_llm)

# ─────────────────────────────────────────────────────────────
#  BOBOT GABUNGAN
# ─────────────────────────────────────────────────────────────
BOBOT_WHISPER  = 0.50   # 50% — transkripsi adalah fondasi pipeline
BOBOT_LEXRANK  = 0.25   # 25% — ekstraksi kalimat penting
BOBOT_LLM      = 0.25   # 25% — penyempurnaan akhir

# Pastikan bobot berjumlah 1.0
assert abs(BOBOT_WHISPER + BOBOT_LEXRANK + BOBOT_LLM - 1.0) < 1e-9, "Bobot harus berjumlah 100%!"

# ─────────────────────────────────────────────────────────────
#  HITUNG AKURASI GABUNGAN
# ─────────────────────────────────────────────────────────────
akurasi_gabungan = (BOBOT_WHISPER * skor_whisper
                  + BOBOT_LEXRANK * skor_lexrank
                  + BOBOT_LLM    * skor_llm)

# ─────────────────────────────────────────────────────────────
#  PENILAIAN KUALITATIF
# ─────────────────────────────────────────────────────────────
def grade_gabungan(score):
    if score >= 85:
        return "Sangat Baik ✓✓✓"
    elif score >= 70:
        return "Baik ✓✓"
    elif score >= 55:
        return "Cukup ✓"
    elif score >= 40:
        return "Perlu Peningkatan"
    else:
        return "Kurang"

def grade_rouge(score):
    if score >= 30:
        return "Baik"
    elif score >= 15:
        return "Cukup"
    elif score >= 5:
        return "Perlu Peningkatan"
    else:
        return "Kurang"

def grade_wacc(score):
    if score >= 95:
        return "Sangat Baik ✓✓"
    elif score >= 85:
        return "Baik ✓"
    elif score >= 70:
        return "Cukup"
    else:
        return "Perlu Peningkatan"

penilaian_gabungan = grade_gabungan(akurasi_gabungan)

# ─────────────────────────────────────────────────────────────
#  CETAK LAPORAN KE CONSOLE
# ─────────────────────────────────────────────────────────────
SEP  = "=" * 64
SEP2 = "-" * 64
LINE = "─" * 50

print(SEP)
print("  LAPORAN AKURASI GABUNGAN SISTEM NOTULENSIA")
print(f"  Tanggal: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}")
print(SEP)

print()
print("  KOMPONEN 1 — WHISPER (Transkripsi Audio)")
print("  " + LINE)
print(f"  WER   (Word Error Rate)   : {WER:>7.2f}%  ↓ lebih kecil lebih baik")
print(f"  WAcc  (Word Accuracy)     : {WAcc:>7.2f}%  ↑ lebih besar lebih baik")
print(f"  CER   (Char Error Rate)   : {CER:>7.2f}%  ↓ lebih kecil lebih baik")
print(f"  CAcc  (Char Accuracy)     : {CAcc:>7.2f}%  ↑ lebih besar lebih baik")
print(f"  Skor Whisper (avg WAcc+CAcc) : {skor_whisper:>6.2f}%   [{grade_wacc(skor_whisper)}]")
print(f"  Bobot dalam sistem        :    {BOBOT_WHISPER*100:.0f}%")

print()
print("  KOMPONEN 2 — LEXRANK (Summarization Ekstraktif)")
print("  " + LINE)
print(f"  ROUGE-1 F1  : {rouge1_lexrank:>7.2f}%   [{grade_rouge(rouge1_lexrank)}]")
print(f"  ROUGE-2 F1  : {rouge2_lexrank:>7.2f}%   [{grade_rouge(rouge2_lexrank)}]")
print(f"  ROUGE-L F1  : {rougeL_lexrank:>7.2f}%   [{grade_rouge(rougeL_lexrank)}]")
print(f"  Skor LexRank (weighted ROUGE) : {skor_lexrank:>5.2f}%")
print(f"  Bobot dalam sistem            :   {BOBOT_LEXRANK*100:.0f}%")

print()
print("  KOMPONEN 3 — LLM OLLAMA (Summarization Generatif)")
print("  " + LINE)
print(f"  ROUGE-1 F1  : {rouge1_llm:>7.2f}%   [{grade_rouge(rouge1_llm)}]")
print(f"  ROUGE-2 F1  : {rouge2_llm:>7.2f}%   [{grade_rouge(rouge2_llm)}]")
print(f"  ROUGE-L F1  : {rougeL_llm:>7.2f}%   [{grade_rouge(rougeL_llm)}]")
print(f"  Skor LLM (weighted ROUGE)     : {skor_llm:>5.2f}%")
print(f"  Bobot dalam sistem            :   {BOBOT_LLM*100:.0f}%")

print()
print(SEP)
print()
print("  ┌─────────────────────────────────────────────────────┐")
print(f"  │  AKURASI GABUNGAN SISTEM  :  {akurasi_gabungan:>6.2f}%               │")
print(f"  │  Penilaian Keseluruhan    :  {penilaian_gabungan:<22}    │")
print("  └─────────────────────────────────────────────────────┘")
print()
print("  RINCIAN KONTRIBUSI PER KOMPONEN:")
print("  " + LINE)
kontrib_whisper = BOBOT_WHISPER * skor_whisper
kontrib_lexrank = BOBOT_LEXRANK * skor_lexrank
kontrib_llm     = BOBOT_LLM    * skor_llm
print(f"  Whisper  ({BOBOT_WHISPER*100:.0f}%) × {skor_whisper:.2f}% = {kontrib_whisper:>6.2f}%")
print(f"  LexRank  ({BOBOT_LEXRANK*100:.0f}%) × {skor_lexrank:.2f}% = {kontrib_lexrank:>6.2f}%")
print(f"  LLM      ({BOBOT_LLM*100:.0f}%) × {skor_llm:.2f}% = {kontrib_llm:>6.2f}%")
print(f"  {'─'*40}")
print(f"  TOTAL                     = {kontrib_whisper+kontrib_lexrank+kontrib_llm:>6.2f}%")
print()
print("  SKALA PENILAIAN:")
print("  ≥ 85%  →  Sangat Baik")
print("  ≥ 70%  →  Baik")
print("  ≥ 55%  →  Cukup")
print("  ≥ 40%  →  Perlu Peningkatan")
print("  < 40%  →  Kurang")
print()
print(SEP)

# ─────────────────────────────────────────────────────────────
#  SIMPAN KE FILE
# ─────────────────────────────────────────────────────────────
output_dir  = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(output_dir, "hasil_akurasi_gabungan.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(SEP + "\n")
    f.write("  LAPORAN AKURASI GABUNGAN SISTEM NOTULENSIA\n")
    f.write(f"  Tanggal: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
    f.write(SEP + "\n\n")

    f.write("  KOMPONEN 1 — WHISPER (Transkripsi Audio)\n")
    f.write("  " + LINE + "\n")
    f.write(f"  WER   (Word Error Rate)      : {WER:>7.2f}%  (lebih kecil = lebih baik)\n")
    f.write(f"  WAcc  (Word Accuracy)         : {WAcc:>7.2f}%  (lebih besar = lebih baik)\n")
    f.write(f"  CER   (Char Error Rate)       : {CER:>7.2f}%  (lebih kecil = lebih baik)\n")
    f.write(f"  CAcc  (Char Accuracy)         : {CAcc:>7.2f}%  (lebih besar = lebih baik)\n")
    f.write(f"  Skor Whisper (avg WAcc+CAcc)  : {skor_whisper:>7.2f}%  [{grade_wacc(skor_whisper)}]\n")
    f.write(f"  Bobot dalam sistem            :     {BOBOT_WHISPER*100:.0f}%\n\n")

    f.write("  KOMPONEN 2 — LEXRANK (Summarization Ekstraktif)\n")
    f.write("  " + LINE + "\n")
    f.write(f"  ROUGE-1 F1  : {rouge1_lexrank:>7.2f}%   [{grade_rouge(rouge1_lexrank)}]\n")
    f.write(f"  ROUGE-2 F1  : {rouge2_lexrank:>7.2f}%   [{grade_rouge(rouge2_lexrank)}]\n")
    f.write(f"  ROUGE-L F1  : {rougeL_lexrank:>7.2f}%   [{grade_rouge(rougeL_lexrank)}]\n")
    f.write(f"  Skor LexRank (weighted ROUGE) : {skor_lexrank:>6.2f}%\n")
    f.write(f"  Bobot dalam sistem            :    {BOBOT_LEXRANK*100:.0f}%\n\n")

    f.write("  KOMPONEN 3 — LLM OLLAMA (Summarization Generatif)\n")
    f.write("  " + LINE + "\n")
    f.write(f"  ROUGE-1 F1  : {rouge1_llm:>7.2f}%   [{grade_rouge(rouge1_llm)}]\n")
    f.write(f"  ROUGE-2 F1  : {rouge2_llm:>7.2f}%   [{grade_rouge(rouge2_llm)}]\n")
    f.write(f"  ROUGE-L F1  : {rougeL_llm:>7.2f}%   [{grade_rouge(rougeL_llm)}]\n")
    f.write(f"  Skor LLM (weighted ROUGE)     : {skor_llm:>6.2f}%\n")
    f.write(f"  Bobot dalam sistem            :    {BOBOT_LLM*100:.0f}%\n\n")

    f.write(SEP + "\n\n")
    f.write("  ╔══════════════════════════════════════════════════════╗\n")
    f.write(f"  ║  AKURASI GABUNGAN SISTEM  :  {akurasi_gabungan:>6.2f}%                ║\n")
    f.write(f"  ║  Penilaian Keseluruhan    :  {penilaian_gabungan:<23}   ║\n")
    f.write("  ╚══════════════════════════════════════════════════════╝\n\n")

    f.write("  RINCIAN KONTRIBUSI PER KOMPONEN:\n")
    f.write("  " + LINE + "\n")
    f.write(f"  Whisper  ({BOBOT_WHISPER*100:.0f}%) × {skor_whisper:.2f}%  = {kontrib_whisper:>6.2f}%\n")
    f.write(f"  LexRank  ({BOBOT_LEXRANK*100:.0f}%) × {skor_lexrank:.2f}%  = {kontrib_lexrank:>6.2f}%\n")
    f.write(f"  LLM      ({BOBOT_LLM*100:.0f}%) × {skor_llm:.2f}%  = {kontrib_llm:>6.2f}%\n")
    f.write(f"  {'─'*40}\n")
    f.write(f"  TOTAL                      = {akurasi_gabungan:>6.2f}%\n\n")

    f.write("  SKALA PENILAIAN:\n")
    f.write("  ≥ 85%  →  Sangat Baik\n")
    f.write("  ≥ 70%  →  Baik\n")
    f.write("  ≥ 55%  →  Cukup\n")
    f.write("  ≥ 40%  →  Perlu Peningkatan\n")
    f.write("  < 40%  →  Kurang\n\n")

    f.write("  METODOLOGI:\n")
    f.write("  " + LINE + "\n")
    f.write("  Formula  : Σ (Bobot_i × Skor_i)\n")
    f.write("  Whisper  : avg(WAcc, CAcc) — normalisasi WER & CER\n")
    f.write("  LexRank  : weighted ROUGE (R1=25%, R2=25%, RL=50%)\n")
    f.write("  LLM      : weighted ROUGE (R1=25%, R2=25%, RL=50%)\n")
    f.write("  Referensi: Whisper=50% (fondasi), LexRank=25%, LLM=25%\n")
    f.write(SEP + "\n")

print(f"\n  ✓ Hasil disimpan ke: {output_file}")
