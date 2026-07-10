# hitung_bertscore_ollama.py
# Menghitung BERTScore untuk ringkasan Ollama (Live & Upload)
# Memproses dokumen satu per satu secara sekuensial untuk menghindari Out Of Memory (OOM) / paging file error.

import os, sys, io, gc
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import torch
from bert_score import score as bert_score_fn

BASE = r"c:\laragon\www\notulensi_rapat"
OUT  = os.path.join(BASE, "akurasi", "ollama", "Bert.txt")

def baca(path):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(path, encoding=enc, errors="replace") as f:
                return f.read().strip()
        except:
            continue
    raise FileNotFoundError(path)

def bersihkan_header(teks):
    lines = teks.split("\n")
    hasil = []
    skip = True
    for line in lines:
        if skip and "======================================" in line:
            skip = False
            continue
        if not skip:
            hasil.append(line)
    return "\n".join(hasil).strip()

# == LIVE ==
LIVE_PAIRS = [
    {
        "topik": "Depresi",
        "kandidat": r"hasil_summarize\ollama\ollama_20260629_232722.txt",
        "referensi": r"hasil\manual transkripsi\manual podcast 1.txt",
    },
    {
        "topik": "Gen-Z & Pernikahan",
        "kandidat": r"hasil_summarize\ollama\ollama_20260628_220127.txt",
        "referensi": r"hasil\manual transkripsi\manual_podcast2.txt",
    },
    {
        "topik": "Pentingnya B. Inggris",
        "kandidat": r"hasil_summarize\ollama\podcast_lexrank1.txt",
        "referensi": r"hasil\manual transkripsi\manual_podcast3.txt",
    },
    {
        "topik": "Disiplin",
        "kandidat": r"hasil_summarize\ollama\podcast_lexrank1.txt",
        "referensi": r"hasil\manual transkripsi\manual_podcast4.txt",
    },
]

# == UPLOAD ==
UPLOAD_PAIRS = [
    {
        "topik": "Basis Data",
        "kandidat": r"hasil_summarize\ollama\ollama_zoom-meeting-basis-data-sabtu-3-juni-2023-sistem-informasi-universitas-jambi-part-1-ytmp4.savetube.vip_20260619_211533.txt",
        "referensi": r"hasil\manual transkripsi\zoom_meeting_basis_data.txt",
    },
    {
        "topik": "K3 Keselamatan Kerja",
        "kandidat": r"hasil_summarize\ollama\ollama_zoom-bnsp-lsptti-pelatihan-k3-keselamatan-kesehatan-kerja-19-may-2023-break1-13-00-15-45-wib-ytmp4.savetube.vip_20260619_222933.txt",
        "referensi": r"hasil\manual transkripsi\zoom materi keselamatan kerja.txt",
    },
    {
        "topik": "KWU",
        "kandidat": r"hasil_summarize\ollama\ollama_Zoom Meeting KWU Sabtu 3 Juni 2023 Sistem Informasi Universitas Jambi - Reza Okto 720p h264_20260620_143855.txt",
        "referensi": r"hasil\manual transkripsi\Zoom Meeting Kwu.txt",
    },
    {
        "topik": "Psikologi Sosial",
        "kandidat": r"hasil_summarize\ollama\ollama_Zoom Meeting   Psikologi Sosial I C 2022 02 23 13 15 57_20260617_212234.txt",
        "referensi": r"hasil\manual transkripsi\Manual_transkrip_Psikologi.txt",
    },
    {
        "topik": "Dasar Manajemen Bisnis",
        "kandidat": r"hasil_summarize\ollama\ollama_Rekaman Zoom Sesi 1 tanggal 17 September 2020 - Mata Kuliah  Dasar Manajemen dan Bisnis - Lapaq Dosen 360p h264_20260617_213535.txt",
        "referensi": r"hasil\manual transkripsi\manual Rekaman Zoom Sesi 1 Tanggal 17 September 2020 - Mata Kuliah Dasar Manajemen Dan Bisnis - Lapaq Dosen 360P H264.txt",
    },
    {
        "topik": "Digital Marketing",
        "kandidat": r"hasil_summarize\ollama\ollama_zoom-meeting-basis-data-sabtu-3-juni-2023-sistem-informasi-universitas-jambi-part-1-ytmp4.savetube.vip_20260619_211533.txt",
        "referensi": r"hasil\manual transkripsi\Manual_transkripsi_digitalmarketing.txt",
    },
    {
        "topik": "Komisi XI DPR RI",
        "kandidat": r"hasil_summarize\ollama\ollama_KOMISI XI DPR RI RDP DENGAN 6 DIRJEN KEMENTERIAN KEUANGAN_20260618_011634.txt",
        "referensi": r"hasil\manual transkripsi\Rapat_komisi_dpr.txt",
    },
    {
        "topik": "ESG & QHSE",
        "kandidat": r"hasil_summarize\ollama\ollama_implementasi-esg-and-qhse-integrasi-bagi-daya-saing-usaha-zoom-meeting-conference-ytmp4.savetube.vip_20260619_231835.txt",
        "referensi": r"hasil\manual transkripsi\meeting esg and qhse.txt",
    },
    {
        "topik": "Ilmu Komunikasi",
        "kandidat": r"hasil_summarize\ollama\ollama_FULL HD VIDEO SIARAN ULANG ZOOM ILMU KOMUNIKASI - Dwii HS 480p_20260620_000940.txt",
        "referensi": r"hasil\manual transkripsi\ilmu komunikasi.txt",
    },
]

def hitung_sekuensial(pairs, label_grup):
    labels = []
    p_vals = []
    r_vals = []
    f1_vals = []
    skipped = []

    print(f"\nMenghitung BERTScore untuk {label_grup} secara sekuensial...")
    for idx, p in enumerate(pairs, 1):
        k_path = os.path.join(BASE, p["kandidat"])
        r_path = os.path.join(BASE, p["referensi"])
        
        if not os.path.exists(k_path):
            skipped.append((p["topik"], f"Kandidat tidak ditemukan: {k_path}"))
            continue
        if not os.path.exists(r_path):
            skipped.append((p["topik"], f"Referensi tidak ditemukan: {r_path}"))
            continue
            
        k_teks = bersihkan_header(baca(k_path))
        r_teks = baca(r_path)
        
        print(f"  [{idx}/{len(pairs)}] Memproses topik: {p['topik']}...")
        
        # Hitung satu per satu
        P_t, R_t, F1_t = bert_score_fn(
            [k_teks], [r_teks],
            lang="id",
            model_type="bert-base-multilingual-cased",
            verbose=False
        )
        
        p_vals.append(P_t[0].item() * 100)
        r_vals.append(R_t[0].item() * 100)
        f1_vals.append(F1_t[0].item() * 100)
        labels.append(p["topik"])
        
        # Bebaskan memori
        del P_t, R_t, F1_t
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return labels, p_vals, r_vals, f1_vals, skipped

SEP  = "=" * 80
SEP2 = "-" * 80

lines = []
lines.append(SEP)
lines.append("  EVALUASI BERTScore — OLLAMA ABSTRACTIVE SUMMARIZATION")
lines.append("  Metrik: Precision, Recall, F1-Score (Semantic Similarity)")
lines.append("  Model : bert-base-multilingual-cased (lang=id)")
lines.append("  Referensi: Transkripsi Manual Manusia")
lines.append(SEP)

def cetak_tabel(lines, labels, P_list, R_list, F1_list, skipped, judul):
    lines.append(f"\n{SEP}")
    lines.append(f"  {judul}")
    lines.append(SEP)
    lines.append(f"{'No':<4} {'Topik':<30} {'Precision':>12} {'Recall':>10} {'F1-Score':>10}")
    lines.append(SEP2)

    sum_p = sum_r = sum_f1 = 0
    for i, (lbl, pv, rv, f1v) in enumerate(zip(labels, P_list, R_list, F1_list), 1):
        sum_p += pv; sum_r += rv; sum_f1 += f1v
        lines.append(f"{i:<4} {lbl:<30} {pv:>11.2f}% {rv:>9.2f}% {f1v:>9.2f}%")

    lines.append(SEP2)
    n = len(labels)
    if n > 0:
        lines.append(f"{'':4} {'Rata-rata':<30} {sum_p/n:>11.2f}% {sum_r/n:>9.2f}% {sum_f1/n:>9.2f}%")
    lines.append(SEP2)

    if skipped:
        lines.append("\n[SKIP] Detail:")
        for topik, msg in skipped:
            lines.append(f"  - {topik}: {msg}")

    return sum_p/n if n else 0, sum_r/n if n else 0, sum_f1/n if n else 0

# Hitung LIVE
lab_l, P_l, R_l, F1_l, skip_l = hitung_sekuensial(LIVE_PAIRS, "LIVE")
avg_pL, avg_rL, avg_f1L = cetak_tabel(
    lines, lab_l, P_l, R_l, F1_l, skip_l,
    "TABEL 1 — BERTScore FITUR LIVE (4 Podcast)"
)

# Hitung UPLOAD
lab_u, P_u, R_u, F1_u, skip_u = hitung_sekuensial(UPLOAD_PAIRS, "UPLOAD")
avg_pU, avg_rU, avg_f1U = cetak_tabel(
    lines, lab_u, P_u, R_u, F1_u, skip_u,
    "TABEL 2 — BERTScore FITUR UPLOAD (9 Topik Rapat)"
)

# Rekapitulasi
lines.append(f"\n{SEP}")
lines.append("  REKAPITULASI PERBANDINGAN FITUR LIVE vs UPLOAD")
lines.append(SEP)
lines.append(f"{'Fitur':<20} {'Precision':>12} {'Recall':>10} {'F1-Score':>10}")
lines.append(SEP2)
lines.append(f"{'Live':<20} {avg_pL:>11.2f}% {avg_rL:>9.2f}% {avg_f1L:>9.2f}%")
lines.append(f"{'Upload':<20} {avg_pU:>11.2f}% {avg_rU:>9.2f}% {avg_f1U:>9.2f}%")
lines.append(SEP2)

lines.append("""
KETERANGAN:
  BERTScore menggunakan model multilingual BERT untuk mengukur kemiripan SEMANTIK
  antara ringkasan Ollama dengan transkripsi manual manusia (ground truth).
  Berbeda dengan ROUGE yang menghitung kecocokan kata-per-kata, BERTScore
  mengukur kemiripan makna meskipun kata-katanya berbeda.

  Precision = seberapa tepat kata dalam ringkasan (tidak ada info tidak relevan)
  Recall    = seberapa banyak informasi penting dari referensi tercakup
  F1-Score  = keseimbangan antara Precision dan Recall
""")

output = "\n".join(lines)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(output)

print(output)
print(f"\nFile disimpan di: {OUT}")
