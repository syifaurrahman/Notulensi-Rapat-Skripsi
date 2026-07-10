# uji_filler_removal.py
import re
import os

# Definisikan regex filter filler words yang sama persis dengan sistem utama (lexrank.py)
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

# Contoh teks mentah percakapan rapat yang penuh filler lisan
sampel_uji = [
    {
        "id": 1,
        "raw": "Nah, jadi gini rekan-rekan, pada kesempatan ini eee kita akan membahas attml dan css ya kan."
    },
    {
        "id": 2,
        "raw": "Oke baik ya, untuk materi Bootstrap itu nanti silakan dipelajari terus dicoba juga ya."
    },
    {
        "id": 3,
        "raw": "Eh... mmm... intinya kita harus menyelesaikan update layout web ini sih, dong, ya."
    },
    {
        "id": 4,
        "raw": "Jadi, untuk database kita pakai meskel ya kan, terus jangan lupa di-backup dulu deh."
    },
    {
        "id": 5,
        "raw": "Nah ini, untuk codingan kita nanti taruh di github aja ya, oke?"
    }
]

def clean_sentence(text):
    # 1. Hapus filler inline (eee, mmm, dll)
    cleaned = _FILLER_INLINE_RE.sub('', text)
    # 2. Hapus koma berlebih di awal
    cleaned = re.sub(r'^[,\s]+', '', cleaned)
    # 3. Hapus filler di awal
    cleaned = _FILLER_START_RE.sub('', cleaned).strip()
    # 4. Hapus koma berlebih di awal (ulang)
    cleaned = re.sub(r'^[,\s]+', '', cleaned)
    # 5. Hapus filler di akhir
    cleaned = _FILLER_END_RE.sub('', cleaned).strip()
    # 6. Rapikan spasi
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # 7. Pastikan kapitalisasi di awal & diakhiri titik
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
        if cleaned[-1] not in '.!?':
            cleaned += '.'
    return cleaned

# Jalankan pengujian dan hitung metrik
folder = r"c:\laragon\www\notulensi_rapat\Hallufilter_uji"
output_path = os.path.join(folder, "Hasil_Uji_Filler_Removal.txt")

md = []
md.append("=== LAPORAN PENGUJIAN WORD FILLER REMOVAL ===")
md.append("Metode: Pengukuran reduksi jumlah kata (Word Count) sebelum dan sesudah filtering.")
md.append("-" * 80)
md.append("")
md.append("| No | Teks Asli (Raw Transcript) | Teks Bersih (Cleaned) | Kata Awal | Kata Akhir | Kata Dihapus | Reduksi (%) |")
md.append("|----|----------------------------|-----------------------|-----------|------------|--------------|-------------|")

total_raw_words = 0
total_cleaned_words = 0

for s in sampel_uji:
    cleaned = clean_sentence(s["raw"])
    raw_words = len(s["raw"].split())
    cleaned_words = len(cleaned.split())
    removed = raw_words - cleaned_words
    reduction = (removed / raw_words) * 100 if raw_words > 0 else 0
    
    total_raw_words += raw_words
    total_cleaned_words += cleaned_words
    
    md.append(f"| {s['id']} | '{s['raw']}' | '{cleaned}' | {raw_words} | {cleaned_words} | {removed} | {reduction:.2f}% |")

# Hitung rekapitulasi rata-rata
total_removed = total_raw_words - total_cleaned_words
avg_reduction = (total_removed / total_raw_words) * 100 if total_raw_words > 0 else 0

md.append(f"| | **TOTAL REKAPITULASI** | | **{total_raw_words}** | **{total_cleaned_words}** | **{total_removed}** | **{avg_reduction:.2f}%** |")

# Simpan ke file teks
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"File laporan hasil pengujian filler removal disimpan di: {output_path}")
print(f"Rata-rata Reduksi Kata: {avg_reduction:.2f}%")
print(f"Total Kata Sebelum: {total_raw_words} | Sesudah: {total_cleaned_words}")
