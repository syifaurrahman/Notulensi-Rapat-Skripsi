# hitung_uji_hallufilter.py
import os
import re

folder = r"c:\laragon\www\notulensi_rapat\Hallufilter_uji"

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
    # Segments pattern:
    # [Timestamp] Output Whisper: '...'
    #             Keputusan Filter: ...
    #             Status Evaluasi : ...
    # Wait, some Status Evaluasi might have "(Trailing Flush)" or similar. Let's capture the core code.
    pattern = r"\[(\d{2}:\d{2}:\d{2})\] Output Whisper: '(.*?)'\s*\n\s*Keputusan Filter:\s*([^\n]+)\n\s*Status Evaluasi\s*:\s*([^\n]+)"
    matches = re.findall(pattern, content)
    for m in matches:
        timestamp, whisper_out, decision, status_raw = m
        # Normalize status to TP, FP, FN, TN
        status = status_raw.strip().split()[0] # e.g. "FN (Trailing" -> "FN"
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

# Load all 15 files
data = {}
for i in range(1, 16):
    fn = f"Hallufilter_{i}.txt"
    path = os.path.join(folder, fn)
    data[i] = parse_file(path)

# Let's see counts of segments
for i in range(1, 16):
    print(f"File {i}: TP={data[i]['tp']}, FP={data[i]['fp']}, FN={data[i]['fn']}, TN={data[i]['tn']}, parsed_segments={len(data[i]['segments'])}")
