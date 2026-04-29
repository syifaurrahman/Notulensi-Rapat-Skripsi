"""
upload_server.py — Flask REST API untuk Upload & Transkripsi File Video
=======================================================================
Server ini menjembatani browser (notulensi_upload.php) dengan
Whisper FileTranscriber.

Cara menjalankan:
  cd whispertranscription
  python upload_server.py

Endpoint:
  POST /transcribe      → Upload file, jalankan Whisper, return JSON hasil
  GET  /download/<file> → Download file .txt hasil dari folder hasil/
  GET  /status          → Health check
"""

from __future__ import annotations

import os
import sys
import threading
import tempfile
import datetime

# Pastikan import module berjalan dari folder ini
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from Mp43filetranscription.config import Config
from Mp43filetranscription.transcriber import FileTranscriber

# ═══════════════════════════════════════════════════════
# App Setup
# ═══════════════════════════════════════════════════════

app = Flask(__name__)
CORS(app, origins="*")  # Izinkan request dari localhost PHP

# Folder output transkripsi (hasil/)
HASIL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil")
UPLOAD_TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

os.makedirs(HASIL_DIR, exist_ok=True)
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)

# Ekstensi file video/audio yang diizinkan
ALLOWED_EXT = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', 'mp3', 'wav'}

# Konfigurasi Whisper
cfg = Config(
    model_size="small",
    language="id",
)

# Lock agar satu job transkripsi berjalan di satu waktu
_transcribe_lock = threading.Lock()


# ═══════════════════════════════════════════════════════
# Helper
# ═══════════════════════════════════════════════════════

def allowed_file(filename: str) -> bool:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in ALLOWED_EXT


def safe_filename(filename: str) -> str:
    """Nama file aman — hapus karakter berbahaya."""
    import re
    name = os.path.basename(filename)
    name = re.sub(r'[^\w\s\-.]', '', name).strip()
    return name or "upload"


# ═══════════════════════════════════════════════════════
# Routes
# ═══════════════════════════════════════════════════════

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint."""
    return jsonify({
        "status": "online",
        "model": cfg.model_size,
        "language": cfg.language,
        "hasil_dir": HASIL_DIR
    })


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Upload file video → jalankan Whisper → kembalikan hasil transkripsi.
    Request: multipart/form-data dengan field 'video_file'
    Response: JSON
    """

    # Validasi ada file
    if 'video_file' not in request.files:
        return jsonify({"status": "error", "message": "Field 'video_file' tidak ditemukan"}), 400

    file = request.files['video_file']

    if file.filename == '':
        return jsonify({"status": "error", "message": "Tidak ada file yang dipilih"}), 400

    if not allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else '?'
        return jsonify({"status": "error", "message": f"Format '{ext}' tidak didukung"}), 400

    # Simpan file sementara
    ext = file.filename.rsplit('.', 1)[-1].lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_name = f"upload_{timestamp}.{ext}"
    temp_path = os.path.join(UPLOAD_TEMP_DIR, temp_name)
    original_name = safe_filename(file.filename)

    try:
        file.save(temp_path)
        print(f"[UploadServer] File diterima: {temp_name} ({os.path.getsize(temp_path):,} bytes)")
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gagal menyimpan file: {e}"}), 500

    # Transkripsi (satu per satu dengan lock)
    if not _transcribe_lock.acquire(blocking=True, timeout=600):
        os.unlink(temp_path)
        return jsonify({"status": "error", "message": "Server sedang memproses file lain. Coba lagi sebentar."}), 503

    try:
        print(f"[UploadServer] Memulai transkripsi: {temp_name}")
        transcriber = FileTranscriber(cfg)
        transcriber.load_model()
        final_text = transcriber.transcribe_file(temp_path)

        if not final_text.strip():
            return jsonify({"status": "error", "message": "Transkripsi kosong — tidak ada suara yang terdeteksi atau audio terlalu pendek"}), 200

        # Simpan ke hasil/ menggunakan nama file asli
        out_path = transcriber.save_result(final_text, original_name)
        txt_filename = os.path.basename(out_path)

        preview = final_text[:600] + ("..." if len(final_text) > 600 else "")

        print(f"[UploadServer] ✓ Selesai: {txt_filename} ({len(final_text):,} karakter)")

        return jsonify({
            "status": "success",
            "preview": preview,
            "full_text": final_text,
            "txt_file": txt_filename,
            "char_count": len(final_text)
        })

    except Exception as e:
        print(f"[UploadServer] ✗ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        _transcribe_lock.release()
        # Hapus file sementara
        try:
            os.unlink(temp_path)
        except Exception:
            pass


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download file .txt dari folder hasil/."""
    # Keamanan: hanya nama file, tidak boleh path traversal
    safe = os.path.basename(filename)
    if not safe.endswith('.txt'):
        return jsonify({"status": "error", "message": "Hanya file .txt yang bisa diunduh"}), 400

    filepath = os.path.join(HASIL_DIR, safe)
    if not os.path.isfile(filepath):
        return jsonify({"status": "error", "message": "File tidak ditemukan"}), 404

    return send_from_directory(HASIL_DIR, safe, as_attachment=True)


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 55)
    print("  📂 Whisper Upload Server — REST API")
    print(f"  Model   : {cfg.model_size} | Language: {cfg.language}")
    print(f"  Hasil   : {HASIL_DIR}")
    print(f"  URL     : http://localhost:5001")
    print("=" * 55)
    print()
    app.run(host='0.0.0.0', port=5001, debug=False)
