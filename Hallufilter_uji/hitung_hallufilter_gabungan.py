# hitung_hallufilter_gabungan.py
import os
import re

folder = r"c:\laragon\www\notulensi_rapat\Hallufilter_uji"
output_file = os.path.join(folder, "Hasil_Pengujian_Hallufilter.md")

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Parse metrics
    tp = int(re.search(r"True Positive \(TP\)\s*:\s*(\d+)", content).group(1))
    fp = int(re.search(r"False Positive \(FP\)\s*:\s*(\d+)", content).group(1))
    fn = int(re.search(r"False Negative \(FN\)\s*:\s*(\d+)", content).group(1))
    tn = int(re.search(r"True Negative \(TN\)\s*:\s*(\d+)", content).group(1))

    # Parse segments
    segments = []
    pattern = r"\[(\d{2}:\d{2}:\d{2})\] Output Whisper: '(.*?)'\s*\n\s*Keputusan Filter:\s*([^\n]+)\n\s*Status Evaluasi\s*:\s*([^\n]+)"
    matches = re.findall(pattern, content)
    for m in matches:
        timestamp, whisper_out, decision, status_raw = m
        status = status_raw.strip().split()[0] # normalize status (e.g. FN)
        segments.append({
            "timestamp": timestamp,
            "whisper_out": whisper_out,
            "decision": decision.strip(),
            "status": status
        })
    
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "segments": segments
    }

# Parse all 15 files
data = {}
for i in range(1, 16):
    fn = f"Hallufilter_{i}.txt"
    path = os.path.join(folder, fn)
    data[i] = parse_file(path)

# Grouping trials by condition
groups = {
    "Hening": list(range(1, 6)),
    "Noise": list(range(6, 11)),
    "Percakapan": list(range(11, 16))
}

# Calculate statistics for each group
stats = {}
for gname, files in groups.items():
    tp_sum = sum(data[i]["tp"] for i in files)
    fp_sum = sum(data[i]["fp"] for i in files)
    fn_sum = sum(data[i]["fn"] for i in files)
    tn_sum = sum(data[i]["tn"] for i in files)
    
    # Formulas
    precision = tp_sum / (tp_sum + fp_sum) if (tp_sum + fp_sum) > 0 else 0.0
    recall = tp_sum / (tp_sum + fn_sum) if (tp_sum + fn_sum) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp_sum + tn_sum) / (tp_sum + tn_sum + fp_sum + fn_sum) if (tp_sum + tn_sum + fp_sum + fn_sum) > 0 else 0.0
    
    stats[gname] = {
        "tp": tp_sum, "fp": fp_sum, "fn": fn_sum, "tn": tn_sum,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
        "accuracy": accuracy * 100
    }

# Let's start building the Markdown file content
md = []
md.append("# LAPORAN EVALUASI DETEKSI HALLUCINATION FILTER")
md.append("Dokumen ini berisi hasil pengujian keandalan Hallucination Filter pada 3 kondisi pengujian (Hening, Noise, dan Percakapan Latar) dengan masing-masing 5 kali percobaan.")
md.append("")

def generate_table_markdown(gname, files, title):
    lines = []
    lines.append(f"### {title}")
    lines.append("")
    lines.append("| No | Output Whisper | Ground Truth | Output Hallucination Filter | Kategori | TP | FP | FN | TN |")
    lines.append("|----|----------------|--------------|-----------------------------|----------|----|----|----|----|")
    
    global_no = 1
    
    # Write segments from each file
    for fn_idx in files:
        file_data = data[fn_idx]
        lines.append(f"| | **Percobaan {fn_idx - files[0] + 1} (File: Hallufilter_{fn_idx}.txt)** | | | | | | | |")
        
        # Add actual segments (TP and FN cases)
        for seg in file_data["segments"]:
            out_filter = "Dihapus (Kosong)" if seg["decision"] == "BUANG" else seg["whisper_out"]
            tp_val = 1 if seg["status"] == "TP" else 0
            fp_val = 1 if seg["status"] == "FP" else 0
            fn_val = 1 if seg["status"] == "FN" else 0
            tn_val = 1 if seg["status"] == "TN" else 0
            
            lines.append(f"| {global_no} | '{seg['whisper_out']}' | Hening | '{out_filter}' | {seg['status']} | {tp_val} | {fp_val} | {fn_val} | {tn_val} |")
            global_no += 1
            
        # Add True Negatives (TNs) as a bulk summary row for this trial
        if file_data["tn"] > 0:
            lines.append(f"| {global_no} | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | {file_data['tn']} |")
            global_no += 1
            
    # Add summary totals row
    tp_sum = sum(data[i]["tp"] for i in files)
    fp_sum = sum(data[i]["fp"] for i in files)
    fn_sum = sum(data[i]["fn"] for i in files)
    tn_sum = sum(data[i]["tn"] for i in files)
    lines.append("| | **TOTAL REKAPITULASI** | | | | **{}** | **{}** | **{}** | **{}** |".format(tp_sum, fp_sum, fn_sum, tn_sum))
    lines.append("")
    
    # Append metrics calculation description
    g_stats = stats[gname]
    lines.append(f"**Metrik Performa {gname}:**")
    lines.append(f"- **Accuracy** = {g_stats['accuracy']:.2f}%")
    lines.append(f"- **Precision** = {g_stats['precision']:.2f}%")
    lines.append(f"- **Recall** = {g_stats['recall']:.2f}%")
    lines.append(f"- **F1-Score** = {g_stats['f1']:.2f}%")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)

# Generate the three tables
md.append(generate_table_markdown("Hening", groups["Hening"], "Tabel 4.1 Hasil Pengujian Hallucination Filter pada Kondisi Hening"))
md.append(generate_table_markdown("Noise", groups["Noise"], "Tabel 4.2 Hasil Pengujian Hallucination Filter pada Kondisi Noise"))
md.append(generate_table_markdown("Percakapan", groups["Percakapan"], "Tabel 4.3 Hasil Pengujian Hallucination Filter pada Kondisi Percakapan"))

# Generate Rekapitulasi Table
md.append("### Tabel Rekapitulasi Seluruh Pengujian")
md.append("")
md.append("| Kondisi Pengujian | TP | FP | FN | TN | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) |")
md.append("|-------------------|----|----|----|----|--------------|---------------|------------|--------------|")
for gname, g_stats in stats.items():
    md.append(f"| Kondisi {gname} | {g_stats['tp']} | {g_stats['fp']} | {g_stats['fn']} | {g_stats['tn']} | {g_stats['accuracy']:.2f}% | {g_stats['precision']:.2f}% | {g_stats['recall']:.2f}% | {g_stats['f1']:.2f}% |")

# Add overall micro/macro average rekapitulasi
tp_all = sum(stats[g]["tp"] for g in stats)
fp_all = sum(stats[g]["fp"] for g in stats)
fn_all = sum(stats[g]["fn"] for g in stats)
tn_all = sum(stats[g]["tn"] for g in stats)

p_all = tp_all / (tp_all + fp_all) * 100 if (tp_all + fp_all) > 0 else 0
r_all = tp_all / (tp_all + fn_all) * 100 if (tp_all + fn_all) > 0 else 0
f1_all = 2 * (p_all * r_all) / (p_all + r_all) if (p_all + r_all) > 0 else 0
acc_all = (tp_all + tn_all) / (tp_all + tn_all + fp_all + fn_all) * 100 if (tp_all + tn_all + fp_all + fn_all) > 0 else 0

md.append(f"| **Rata-rata Keseluruhan** | **{tp_all}** | **{fp_all}** | **{fn_all}** | **{tn_all}** | **{acc_all:.2f}%** | **{p_all:.2f}%** | **{r_all:.2f}%** | **{f1_all:.2f}%** |")
md.append("")
md.append("---")
md.append("")
md.append("### Kesimpulan Analisis Performa:")
md.append("1. **Kondisi Hening Sempurna**: Menghasilkan akurasi tinggi karena VAD dan minimal frame processing menahan sebagian besar audio tanpa pengiriman ke Whisper. Presisi mencapai 100%, yang berarti tidak ada satupun ucapan valid yang terbuang.")
md.append("2. **Kondisi Noise Kipas**: Memiliki recall terendah (~29.31%), artinya banyak halusinasi kalimat repetitif pendek di luar blacklist yang lolos dari filter (seperti kalimat 'Pertahankan kata-kata'). Namun akurasi keseluruhan tetap terjaga tinggi di atas 90% karena kontribusi TN (suara hening yang berhasil dipertahankan) yang sangat banyak.")
md.append("3. **Kondisi Percakapan Latar**: Memiliki jumlah segmen terbanyak karena suara latar memicu deteksi VAD untuk melakukan transkripsi aktif. Akurasi berada di kisaran 76.54% dengan keseimbangan F1-Score sebesar 65.41%.")

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"File hasil pengujian berhasil disimpan di: {output_file}")
print("\n=== RINGKASAN REKAPITULASI ===")
for gname, g_stats in stats.items():
    print(f"Kondisi {gname:<12} | TP={g_stats['tp']:<3} FP={g_stats['fp']:<3} FN={g_stats['fn']:<3} TN={g_stats['tn']:<4} | Acc={g_stats['accuracy']:.2f}% P={g_stats['precision']:.2f}% R={g_stats['recall']:.2f}% F1={g_stats['f1']:.2f}%")
