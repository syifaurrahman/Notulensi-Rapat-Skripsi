"""
transcribe_api.py — API Python untuk dipanggil PHP via exec()
=============================================================
Cara pakai:
    python transcribe_api.py <path_video>

Output: JSON ke stdout
    {"status": "success", "preview": "...", "txt_file": "transkrip_xxx.txt", "txt_path": "..."}
    {"status": "error", "message": "..."}
"""

import sys
import os
import json

# Pastikan import module tersedia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Mp43filetranscription.config import Config
from Mp43filetranscription.transcriber import FileTranscriber


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Argumen path video tidak ditemukan"}))
        sys.exit(1)

    video_path = sys.argv[1]

    if not os.path.isfile(video_path):
        print(json.dumps({"status": "error", "message": f"File tidak ditemukan: {video_path}"}))
        sys.exit(1)

    try:
        config = Config(
            model_size="small",
            language="id",
        )

        transcriber = FileTranscriber(config)
        transcriber.load_model()
        final_text = transcriber.transcribe_file(video_path)

        if not final_text.strip():
            print(json.dumps({"status": "error", "message": "Transkripsi kosong, tidak ada suara yang terdeteksi"}))
            sys.exit(1)

        # Simpan ke folder hasil/
        out_path = transcriber.save_result(final_text, video_path)
        txt_filename = os.path.basename(out_path)

        # Preview 500 karakter pertama
        preview = final_text[:500] + ("..." if len(final_text) > 500 else "")

        print(json.dumps({
            "status": "success",
            "preview": preview,
            "full_text": final_text,
            "txt_file": txt_filename,
            "txt_path": out_path,
            "char_count": len(final_text)
        }, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
