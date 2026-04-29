"""
web_server.py — Flask + Socket.IO Server untuk Live Transcription via Web
==========================================================================
Server ini menjembatani browser (notulensi.php) dengan Whisper Live Transcription.

Cara menjalankan:
  cd whispertranscription/whisperLiveTranscription
  python web_server.py

Browser mengirim audio chunks via WebSocket → server transkripsi → kirim balik teks.
"""

from __future__ import annotations

import os
import sys
import datetime
import time
import threading
import numpy as np

# Pastikan import dari folder yang sama
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from config import Config
from hallucination_filter import HallucinationFilter
from audio_processor import AudioProcessor
from transcriber import Transcriber

# Buat dummy console untuk Transcriber (karena tidak pakai Rich di web)
class DummyConsole:
    """Pengganti Rich Console untuk logging sederhana di server."""
    def print(self, *args, **kwargs):
        text = " ".join(str(a) for a in args)
        # Strip Rich markup
        import re
        clean = re.sub(r'\[.*?\]', '', text)
        if clean.strip():
            print(f"[WebServer] {clean.strip()}")

    def log(self, *args, **kwargs):
        self.print(*args, **kwargs)

    def input(self, prompt=""):
        return ""


# ══════════════════════════════════════════════════
# Flask App Setup
# ══════════════════════════════════════════════════

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notulensi-whisper-secret'
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading',
                    max_http_buffer_size=10 * 1024 * 1024)  # 10MB max

# ══════════════════════════════════════════════════
# Global State
# ══════════════════════════════════════════════════

console = DummyConsole()

# Konfigurasi Whisper
cfg = Config(
    model_size="small",
    language="id",
    use_autocorrect=False,   # Matikan LanguageTool di web (berat & lambat)
    vad_threshold=0.01,
    debug_rms=False,
    min_process_sec=2.0,
    silence_pause_sec=1.2,
)

# Komponen (di-init sekali, shared semua session)
processor = AudioProcessor(cfg)
halluc_filter = HallucinationFilter(cfg)
transcriber = None       # Di-load saat pertama kali start
model_loaded = False
model_loading = False

# Per-session state
sessions = {}


class SessionState:
    """State per koneksi WebSocket."""
    def __init__(self, sid):
        self.sid = sid
        self.audio_buffer = np.zeros(0, dtype=np.float32)
        self.history_text = ""
        self.current_text = ""
        self.prev_text = ""
        self.is_listening = False
        self.start_time = None
        self.sample_rate = 16000  # Default, akan di-set dari client

    def clear(self):
        self.audio_buffer = np.zeros(0, dtype=np.float32)
        self.history_text = ""
        self.current_text = ""
        self.prev_text = ""
        self.is_listening = False
        self.start_time = None


# ══════════════════════════════════════════════════
# Helper Functions
# ══════════════════════════════════════════════════

def load_model_if_needed():
    """Load Whisper model jika belum di-load."""
    global transcriber, model_loaded, model_loading

    if model_loaded:
        return True

    if model_loading:
        # Tunggu sampai loading selesai
        while model_loading and not model_loaded:
            time.sleep(0.5)
        return model_loaded

    model_loading = True
    try:
        print("[WebServer] Loading Whisper model...")
        transcriber_obj = Transcriber(cfg, processor, console)
        transcriber_obj.load_model()
        transcriber_obj.start()
        transcriber = transcriber_obj
        model_loaded = True
        print("[WebServer] ✓ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"[WebServer] ✗ Failed to load model: {e}")
        model_loading = False
        return False
    finally:
        model_loading = False


def process_audio_buffer(session: SessionState):
    """Proses audio buffer: transkripsi dengan Whisper."""
    global transcriber

    if transcriber is None or len(session.audio_buffer) == 0:
        return

    buffer_duration = len(session.audio_buffer) / session.sample_rate
    if buffer_duration < cfg.min_process_sec:
        return

    # Hitung RMS
    latest = session.audio_buffer[-int(session.sample_rate):]
    rms = float(np.sqrt(np.mean(latest ** 2))) if len(latest) > 0 else 0.0

    if rms < cfg.vad_threshold:
        # Hening — jika ada current text, pindahkan ke history
        if session.current_text:
            session.history_text += session.current_text + " "
            session.current_text = ""
            session.prev_text = ""
        # Trim buffer agar tidak penuh
        max_samples = int(session.sample_rate * 1.0)
        if len(session.audio_buffer) > max_samples:
            session.audio_buffer = session.audio_buffer[-max_samples:]
        return

    # Ada suara — transkripsi
    buf = session.audio_buffer.copy()
    transcriber.submit_and_wait(buf, session.sample_rate, timeout=8.0)
    chunk_text = transcriber.pop_result()

    # Filter
    if halluc_filter.is_hallucination(chunk_text):
        chunk_text = ""
    if chunk_text and chunk_text == session.prev_text:
        chunk_text = ""

    if chunk_text:
        session.current_text = chunk_text
        session.prev_text = chunk_text

    # Flush buffer jika terlalu panjang
    if buffer_duration > cfg.buffer_max_sec:
        if session.current_text:
            session.history_text += session.current_text + " "
            session.current_text = ""
            session.prev_text = ""
        session.audio_buffer = np.zeros(0, dtype=np.float32)


def save_transcript(text: str) -> str:
    """Simpan transkripsi ke file di folder hasil/."""
    if not text.strip():
        return ""

    hasil_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil")
    os.makedirs(hasil_dir, exist_ok=True)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(hasil_dir, f"transkrip_{ts}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=== TRANSKRIPSI RAPAT (LIVE — Web) ===\n")
        f.write(f"Dibuat  : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Model   : Whisper {cfg.model_size}\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(text)

    print(f"[WebServer] ✓ Transkrip disimpan: {out_path}")
    return out_path


# ══════════════════════════════════════════════════
# Socket.IO Event Handlers
# ══════════════════════════════════════════════════

@socketio.on('connect')
def handle_connect():
    sid = getattr(handle_connect, '__wrapped__', None)
    from flask import request
    sid = request.sid
    sessions[sid] = SessionState(sid)
    print(f"[WebServer] Client connected: {sid}")
    emit('status_update', {'status': 'connected', 'message': 'Terhubung ke server'})


@socketio.on('disconnect')
def handle_disconnect():
    from flask import request
    sid = request.sid
    if sid in sessions:
        del sessions[sid]
    print(f"[WebServer] Client disconnected: {sid}")


@socketio.on('start_listening')
def handle_start_listening(data):
    """Client minta mulai listening. Load model jika perlu."""
    from flask import request
    sid = request.sid
    session = sessions.get(sid)
    if not session:
        session = SessionState(sid)
        sessions[sid] = session

    session.clear()
    session.sample_rate = data.get('sampleRate', 16000)
    session.is_listening = True
    session.start_time = time.time()

    print(f"[WebServer] Start listening (SR: {session.sample_rate})")

    # Load model
    emit('status_update', {'status': 'loading_model', 'message': 'Memuat model Whisper...'})

    if not load_model_if_needed():
        emit('status_update', {'status': 'error', 'message': 'Gagal memuat model Whisper'})
        session.is_listening = False
        return

    emit('status_update', {'status': 'listening', 'message': 'Mendengarkan...'})
    emit('model_ready', {'model': cfg.model_size})


@socketio.on('audio_data')
def handle_audio_data(data):
    """Terima chunk audio dari browser (ArrayBuffer float32)."""
    from flask import request
    sid = request.sid
    session = sessions.get(sid)

    if not session or not session.is_listening:
        return

    try:
        # Data berupa bytes (Float32Array dari browser)
        audio_chunk = np.frombuffer(data, dtype=np.float32)

        # Tambahkan ke buffer
        session.audio_buffer = np.concatenate((session.audio_buffer, audio_chunk))

        # Proses jika buffer cukup
        process_audio_buffer(session)

        # Kirim hasil ke client
        full_text = (session.history_text + session.current_text).strip()
        if full_text:
            emit('transcription_update', {
                'text': full_text,
                'current': session.current_text,
                'history': session.history_text,
                'is_final': False
            })

    except Exception as e:
        print(f"[WebServer] Error processing audio: {e}")


@socketio.on('stop_listening')
def handle_stop_listening():
    """Client minta stop listening."""
    from flask import request
    sid = request.sid
    session = sessions.get(sid)

    if not session:
        return

    session.is_listening = False

    # Flush sisa buffer
    if session.current_text:
        session.history_text += session.current_text + " "
        session.current_text = ""

    # Transkripsi sisa buffer terakhir jika ada
    if transcriber and len(session.audio_buffer) > int(session.sample_rate * 0.5):
        try:
            transcriber.submit_and_wait(session.audio_buffer.copy(), session.sample_rate, timeout=8.0)
            tail = transcriber.pop_result()
            if tail and not halluc_filter.is_hallucination(tail):
                session.history_text += tail + " "
        except Exception as e:
            print(f"[WebServer] Error in final flush: {e}")

    final_text = session.history_text.strip()

    # Simpan ke file
    saved_path = ""
    if final_text:
        saved_path = save_transcript(final_text)

    # Kirim hasil final
    emit('transcription_update', {
        'text': final_text,
        'current': '',
        'history': final_text,
        'is_final': True
    })

    duration = 0
    if session.start_time:
        duration = int(time.time() - session.start_time)

    emit('status_update', {
        'status': 'stopped',
        'message': 'Selesai',
        'duration': duration,
        'saved_path': saved_path
    })

    print(f"[WebServer] Stopped. Duration: {duration}s, Text length: {len(final_text)}")


@socketio.on('ping_server')
def handle_ping():
    """Health check."""
    emit('pong_server', {
        'model_loaded': model_loaded,
        'model_size': cfg.model_size
    })


# ══════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 50)
    print("  🎙 Whisper Live Transcription — Web Server")
    print(f"  Model: {cfg.model_size} | Language: {cfg.language}")
    print(f"  Server: http://localhost:5000")
    print("=" * 50)
    print()

    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
