# scan_headers.py
import os

folder = r"c:\laragon\www\notulensi_rapat\Hallufilter_uji"
files = sorted([f for f in os.listdir(folder) if f.startswith("Hallufilter_") and f.endswith(".txt")], key=lambda x: int(x.split("_")[1].split(".")[0]))

print(f"{'File':<18} | {'Durasi & Kondisi'}")
print("-" * 50)
for fn in files:
    path = os.path.join(folder, fn)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [f.readline().strip() for _ in range(5)]
        header = ""
        for line in lines:
            if "Durasi" in line or "Kondisi" in line or "Kebenaran" in line:
                header += line + " | "
        print(f"{fn:<18} | {header}")
