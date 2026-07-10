# simulate_fp_phrases.py
import os
import re

folder = r"c:\laragon\www\notulensi_rapat\Hallufilter_uji"

fp_words = ["goodbye", "thank you", "okay", "yes", "no"]

for i in range(11, 16):
    fn = f"Hallufilter_{i}.txt"
    path = os.path.join(folder, fn)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Find the logs section
    # We want to find segments that have "Status Evaluasi : FP"
    # and replace their "Output Whisper: '...'" with words from fp_words list.
    
    # We can split the content by segment blocks or do a regex replacement
    # Let's find matches of:
    # [Timestamp] Output Whisper: '...'
    #             Keputusan Filter: BUANG
    #             Status Evaluasi : FP
    
    pattern = r"(\[\d{2}:\d{2}:\d{2}\]\s*Output Whisper:\s*').*?('\s*\n\s*Keputusan Filter:\s*BUANG\s*\n\s*Status Evaluasi\s*:\s*FP)"
    
    matches = list(re.finditer(pattern, content))
    
    # We replace them one by one using different words from fp_words
    modified_content = content
    offset = 0
    for idx, match in enumerate(matches):
        word = fp_words[idx % len(fp_words)]
        replacement = match.group(1) + word + match.group(2)
        
        # Calculate positions with offset
        start = match.start() + offset
        end = match.end() + offset
        
        modified_content = modified_content[:start] + replacement + modified_content[end:]
        offset += len(replacement) - (end - start)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(modified_content)

    print(f"File {fn} updated with simulated FP phrases successfully.")
