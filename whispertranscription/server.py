"""
server.py — Server Terpadu: Live Transcription + Upload Transcription
======================================================================
Satu server Flask yang menjalankan keduanya sekaligus:

  ┌─────────────────────────────────────────────────────┐
  │  Socket.IO  →  Live Whisper Transcription (mic)     │
  │  REST API   →  Upload Whisper Transcription (file)  │
  │  LexRank   →  Ringkasan otomatis pasca transkripsi  │
  └─────────────────────────────────────────────────────┘

Cara menjalankan (cukup satu kali):
  cd whispertranscription
  python server.py

Port tunggal: http://localhost:5000
"""

from __future__ import annotations

import os
import sys
import threading
import datetime
import time
import tempfile
import re

import numpy as np

# ── Import path setup ──────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LIVE_DIR  = os.path.join(BASE_DIR, "whisperLiveTranscription")
# File .txt disimpan langsung di folder web (dapat diakses via Apache)
WEB_DIR             = os.path.abspath(os.path.join(BASE_DIR, ".."))
HASIL_DIR               = os.path.join(WEB_DIR, "hasil")
HASIL_SUMMARIZE_DIR     = os.path.join(WEB_DIR, "hasil_summarize")
HASIL_LEXRANK_DIR       = os.path.join(WEB_DIR, "hasil_summarize", "Lexrank")
HASIL_OLLAMA_DIR        = os.path.join(WEB_DIR, "hasil_summarize", "Ollama")
UPLOAD_DIR              = os.path.join(BASE_DIR, "uploads")  # temp, tetap di backend

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, LIVE_DIR)

os.makedirs(HASIL_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(HASIL_SUMMARIZE_DIR, exist_ok=True)
os.makedirs(HASIL_LEXRANK_DIR, exist_ok=True)
os.makedirs(HASIL_OLLAMA_DIR, exist_ok=True)

# ── Flask ──────────────────────────────────────────────────
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# ── Live Transcription modules ─────────────────────────────
from whisperLiveTranscription.config          import Config           as LiveConfig
from whisperLiveTranscription.hallucination_filter import HallucinationFilter
from whisperLiveTranscription.audio_processor import AudioProcessor
from whisperLiveTranscription.transcriber     import Transcriber

# ── Upload Transcription modules ───────────────────────────
from Mp43filetranscription.config      import Config           as FileConfig
from Mp43filetranscription.transcriber import FileTranscriber

# ── Summarize modules ────────────────────────────────────────────────────────
from summarize.lexrank import LexRankSummarizer
from summarize.config  import SummaryConfig

# ── Database ──────────────────────────────────────────────────────────────────
import pymysql

# Konfigurasi MySQL (sesuaikan jika berbeda)
DB_CONFIG = {
    'host'    : 'localhost',
    'user'    : 'root',
    'password': '',
    'database': 'notulensi',
    'charset' : 'utf8mb4',
}

# ══════════════════════════════════════════════════════════
# Flask App (Socket.IO embedded)
# ══════════════════════════════════════════════════════════

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notulensi-whisper-unified-2024'
CORS(app, origins="*")
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    max_http_buffer_size=10 * 1024 * 1024   # 10 MB
)


# ══════════════════════════════════════════════════════════
# Dummy Console (untuk suppress Rich output)
# ══════════════════════════════════════════════════════════

class DummyConsole:
    def print(self, *args, **kwargs):
        text = " ".join(str(a) for a in args)
        clean = re.sub(r'\[.*?\]', '', text)
        if clean.strip():
            print(f"[Server] {clean.strip()}", flush=True)

    def log(self, *args, **kwargs):
        self.print(*args, **kwargs)

    def input(self, prompt=""):
        return ""

console = DummyConsole()


# ══════════════════════════════════════════════════════════
# ① LIVE TRANSCRIPTION — Global State & Helpers
# ══════════════════════════════════════════════════════════

live_cfg = LiveConfig(
    model_size="small",
    language="id",
    use_autocorrect=False,
    vad_threshold=0.01,
    debug_rms=False,
    min_process_sec=2.0,
    silence_pause_sec=1.2,
)

live_processor     = AudioProcessor(live_cfg)
live_halluc_filter = HallucinationFilter(live_cfg)
live_transcriber   = None        # Shared Whisper model untuk Live
live_model_loaded  = False
live_model_loading = False
live_sessions      = {}          # Per-client state


class SessionState:
    """State per koneksi WebSocket."""
    def __init__(self, sid):
        self.sid          = sid
        self.audio_buffer = np.zeros(0, dtype=np.float32)
        self.history_text  = ""
        self.current_text  = ""
        self.prev_text     = ""
        self.is_listening  = False
        self.start_time    = None
        self.sample_rate   = 16000
        self.judul_rapat   = ""   # Judul rapat dari client
        self.last_txt_filename = ""  # Nama file .txt terakhir disimpan

    def clear(self):
        self.audio_buffer  = np.zeros(0, dtype=np.float32)
        self.history_text  = ""
        self.current_text  = ""
        self.prev_text     = ""
        self.is_listening  = False
        self.start_time    = None
        self.judul_rapat   = ""
        self.last_txt_filename = ""


def load_live_model():
    """Load / reuse Whisper model untuk Live mode."""
    global live_transcriber, live_model_loaded, live_model_loading
    if live_model_loaded:
        return True
    if live_model_loading:
        while live_model_loading and not live_model_loaded:
            time.sleep(0.5)
        return live_model_loaded

    live_model_loading = True
    try:
        print("[Server] Loading Live Whisper model...", flush=True)
        t = Transcriber(live_cfg, live_processor, console)
        t.load_model()
        t.start()
        live_transcriber  = t
        live_model_loaded = True
        print("[Server] ✓ Live model loaded!", flush=True)
        return True
    except Exception as e:
        print(f"[Server] ✗ Live model failed: {e}", flush=True)
        live_model_loading = False
        return False
    finally:
        live_model_loading = False


def process_live_audio(session: SessionState):
    """Proses audio buffer → transkripsi Whisper."""
    if live_transcriber is None or len(session.audio_buffer) == 0:
        return
    buf_dur = len(session.audio_buffer) / session.sample_rate
    if buf_dur < live_cfg.min_process_sec:
        return

    latest = session.audio_buffer[-int(session.sample_rate):]
    rms    = float(np.sqrt(np.mean(latest ** 2))) if len(latest) > 0 else 0.0

    if rms < live_cfg.vad_threshold:
        if session.current_text:
            session.history_text += session.current_text + " "
            session.current_text  = ""
            session.prev_text     = ""
        max_s = int(session.sample_rate * 1.0)
        if len(session.audio_buffer) > max_s:
            session.audio_buffer = session.audio_buffer[-max_s:]
        return

    buf = session.audio_buffer.copy()
    live_transcriber.submit_and_wait(buf, session.sample_rate, timeout=8.0)
    chunk_text = live_transcriber.pop_result()

    if live_halluc_filter.is_hallucination(chunk_text):
        chunk_text = ""
    if chunk_text and chunk_text == session.prev_text:
        chunk_text = ""

    if chunk_text:
        session.current_text = chunk_text
        session.prev_text    = chunk_text

    if buf_dur > live_cfg.buffer_max_sec:
        if session.current_text:
            session.history_text += session.current_text + " "
            session.current_text  = ""
            session.prev_text     = ""
        session.audio_buffer = np.zeros(0, dtype=np.float32)


def save_live_transcript(text: str) -> str:
    """Simpan hasil Live ke file di hasil/."""
    if not text.strip():
        return ""
    ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(HASIL_DIR, f"transkrip_{ts}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=== TRANSKRIPSI RAPAT (LIVE — Web) ===\n")
        f.write(f"Dibuat  : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Model   : Whisper {live_cfg.model_size}\n")
        f.write(f"{'=' * 40}\n\n")
        f.write(text)
    print(f"[Server] ✓ Live transkrip disimpan: {out_path}", flush=True)
    return out_path


# ══════════════════════════════════════════════════════════
# ① LIVE — Socket.IO Event Handlers
# ══════════════════════════════════════════════════════════

@socketio.on('connect')
def handle_connect():
    from flask import request as req
    sid = req.sid
    live_sessions[sid] = SessionState(sid)
    print(f"[Server] Client connected: {sid}", flush=True)
    emit('status_update', {'status': 'connected', 'message': 'Terhubung ke server'})


@socketio.on('disconnect')
def handle_disconnect():
    from flask import request as req
    sid = req.sid
    live_sessions.pop(sid, None)
    print(f"[Server] Client disconnected: {sid}", flush=True)


@socketio.on('start_listening')
def handle_start_listening(data):
    from flask import request as req
    sid     = req.sid
    session = live_sessions.setdefault(sid, SessionState(sid))
    session.clear()
    session.sample_rate  = data.get('sampleRate', 16000)
    session.is_listening = True
    session.start_time   = time.time()
    # Simpan judul rapat yang dikirim dari client
    session.judul_rapat  = data.get('judul_rapat', '')

    emit('status_update', {'status': 'loading_model', 'message': 'Memuat model Whisper...'})
    if not load_live_model():
        emit('status_update', {'status': 'error', 'message': 'Gagal memuat model Whisper'})
        session.is_listening = False
        return

    emit('status_update', {'status': 'listening', 'message': 'Mendengarkan...'})
    emit('model_ready', {'model': live_cfg.model_size})


@socketio.on('audio_data')
def handle_audio_data(data):
    from flask import request as req
    sid     = req.sid
    session = live_sessions.get(sid)
    if not session or not session.is_listening:
        return

    try:
        chunk = np.frombuffer(data, dtype=np.float32)
        session.audio_buffer = np.concatenate((session.audio_buffer, chunk))
        process_live_audio(session)
        full_text = (session.history_text + session.current_text).strip()
        if full_text:
            emit('transcription_update', {
                'text'    : full_text,
                'current' : session.current_text,
                'history' : session.history_text,
                'is_final': False
            })
    except Exception as e:
        print(f"[Server] Error audio: {e}", flush=True)


@socketio.on('stop_listening')
def handle_stop_listening():
    from flask import request as req
    sid     = req.sid
    session = live_sessions.get(sid)
    if not session:
        return

    session.is_listening = False
    if session.current_text:
        session.history_text += session.current_text + " "
        session.current_text  = ""

    if live_transcriber and len(session.audio_buffer) > int(session.sample_rate * 0.5):
        try:
            live_transcriber.submit_and_wait(session.audio_buffer.copy(), session.sample_rate, timeout=8.0)
            tail = live_transcriber.pop_result()
            if tail and not live_halluc_filter.is_hallucination(tail):
                session.history_text += tail + " "
        except Exception as e:
            print(f"[Server] Final flush error: {e}", flush=True)

    final_text  = session.history_text.strip()
    saved_path  = save_live_transcript(final_text)
    txt_filename = os.path.basename(saved_path) if saved_path else ""
    duration    = int(time.time() - session.start_time) if session.start_time else 0

    # Ambil judul rapat dari session (dikirim saat start_listening)
    judul_rapat = getattr(session, 'judul_rapat', '')
    if not judul_rapat:
        judul_rapat = f"Rapat Live {datetime.datetime.now().strftime('%d %B %Y %H:%M')}"

    # Simpan nama file untuk digunakan saat request_summarize
    session.last_txt_filename = txt_filename
    session.last_duration     = duration

    emit('transcription_update', {
        'text': final_text, 'current': '', 'history': final_text, 'is_final': True
    })
    emit('status_update', {
        'status': 'stopped', 'message': 'Selesai',
        'duration': duration, 'saved_path': saved_path
    })
    print(f"[Server] Live stopped. Dur: {duration}s | Chars: {len(final_text)}", flush=True)


@socketio.on('ping_server')
def handle_ping():
    emit('pong_server', {'model_loaded': live_model_loaded, 'model_size': live_cfg.model_size})


@socketio.on('request_summarize')
def handle_request_summarize(data):
    """
    Dipanggil client setelah user klik 'Simpan Notulen'.
    Menerima: { text, judul_rapat }
    Proses : save_to_db → LexRank BG → emit summarize_done
    """
    from flask import request as req
    sid     = req.sid
    session = live_sessions.get(sid)

    text        = (data.get('text', '') or '').strip()
    judul_rapat = (data.get('judul_rapat', '') or '').strip()

    if not text:
        emit('summarize_done', {'status': 'error', 'message': 'Tidak ada teks untuk diringkas'})
        return

    if not judul_rapat:
        judul_rapat = f"Rapat Live {datetime.datetime.now().strftime('%d %B %Y %H:%M')}"

    # Ambil nama file txt dari session (jika ada), atau simpan dulu
    txt_filename = ""
    if session:
        txt_filename = getattr(session, 'last_txt_filename', '')

    if not txt_filename:
        # Teks belum tersimpan ke file (edge case: user klik simpan tanpa stop dulu)
        saved_path = save_live_transcript(text)
        txt_filename = os.path.basename(saved_path) if saved_path else ""
        if session:
            session.last_txt_filename = txt_filename

    # Simpan record ke DB dengan status 'proses summarize'
    db_id = save_to_db(
        judul        = judul_rapat,
        tipe         = 'Live',
        txt_path     = txt_filename,
        ringkasan    = '[PROSES_SUMMARIZE]',
        durasi_detik = getattr(session, 'last_duration', 0)
    )

    # Beri tahu client summarize dimulai
    emit('status_update', {
        'status'  : 'summarizing',
        'message' : 'Membuat ringkasan otomatis...',
        'db_id'   : db_id,
    })

    def _run_request_summarize(summarize_text: str, d_id: int, client_sid: str, fname: str):
        try:
            print(f"[Server] BG request_summarize (DB {d_id}): mulai LexRank...", flush=True)
            result = summarizer.summarize_with_debug(summarize_text)
            ringkasan = result['ringkasan']
            ranked_sentences = result.get('ranked_sentences', [])
            lexrank_extractive  = result.get('lexrank_extractive', '')
            ollama_result       = result.get('ollama_result', None)
            if not ringkasan:
                ringkasan = "Tidak ada ringkasan yang dihasilkan."

            # Simpan file ringkasan
            if fname and fname.startswith("transkrip_"):
                sum_filename = fname.replace("transkrip_", "ringkasan_")
            else:
                ts_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                sum_filename = f"ringkasan_live_{ts_now}.txt"

            # ── [1] Simpan ringkasan UTAMA ke hasil_summarize/ ──
            sum_path = os.path.join(HASIL_SUMMARIZE_DIR, sum_filename)
            with open(sum_path, "w", encoding="utf-8") as sf:
                sf.write("=== RINGKASAN RAPAT (LIVE — LexRank 6-Step) ===\n")
                sf.write(f"Sumber    : {fname}\n")
                sf.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
                sf.write(f"Model     : Whisper {live_cfg.model_size}\n")
                sf.write(f"{'=' * 40}\n\n")
                sf.write(ringkasan)
            print(f"[Server] ✓ Ringkasan Live disimpan: {sum_filename}", flush=True)

            # ── [2] Simpan hasil LexRank EXTRACTIVE ke hasil_summarize/Lexrank/ ──
            if lexrank_extractive:
                lexrank_filename = "lexrank_" + fname.replace("transkrip_", "") if (fname and fname.startswith("transkrip_")) else f"lexrank_live_{ts_now}.txt"
                lexrank_path = os.path.join(HASIL_LEXRANK_DIR, lexrank_filename)
                with open(lexrank_path, "w", encoding="utf-8") as lf:
                    lf.write("=== HASIL LEXRANK EXTRACTIVE (LIVE) ===\n")
                    lf.write(f"Sumber    : {fname}\n")
                    lf.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
                    lf.write(f"Model     : Whisper {live_cfg.model_size}\n")
                    lf.write(f"{'=' * 40}\n\n")
                    lf.write(lexrank_extractive)
                print(f"[Server] ✓ LexRank extractive Live disimpan ke Lexrank/{lexrank_filename}", flush=True)

            # ── [3] Simpan hasil OLLAMA ABSTRACTIVE ke hasil_summarize/Ollama/ ──
            if ollama_result:
                ollama_filename = "ollama_" + fname.replace("transkrip_", "") if (fname and fname.startswith("transkrip_")) else f"ollama_live_{ts_now}.txt"
                ollama_path = os.path.join(HASIL_OLLAMA_DIR, ollama_filename)
                with open(ollama_path, "w", encoding="utf-8") as of:
                    of.write("=== HASIL OLLAMA ABSTRACTIVE (LIVE) ===\n")
                    of.write(f"Sumber    : {fname}\n")
                    of.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
                    of.write(f"Model     : Whisper {live_cfg.model_size} + {sum_cfg.ollama_model}\n")
                    of.write(f"{'=' * 40}\n\n")
                    of.write(ollama_result)
                print(f"[Server] ✓ Ollama abstractive Live disimpan ke Ollama/{ollama_filename}", flush=True)
            else:
                print(f"[Server] ℹ Ollama tidak tersedia/gagal — file Ollama tidak dibuat (Live)", flush=True)

            # ── Simpan debug JSON ──
            debug_path = sum_path.replace('.txt', '_debug.json')
            try:
                import json as _json
                with open(debug_path, 'w', encoding='utf-8') as df:
                    _json.dump(ranked_sentences, df, ensure_ascii=False, indent=2)
            except Exception:
                pass

            update_summary_in_db(d_id, ringkasan)
            print(f"[Server] ✓ DB ID {d_id} diupdate (Live summarize)", flush=True)

            socketio.emit('summarize_done', {
                'status'          : 'success',
                'ringkasan'       : ringkasan,
                'db_id'           : d_id,
                'lexrank_debug'   : ranked_sentences,
            }, to=client_sid)

        except Exception as e:
            print(f"[Server] BG request_summarize Error: {e}", flush=True)
            update_summary_in_db(d_id, f"[GAGAL_SUMMARIZE] {e}")
            socketio.emit('summarize_done', {
                'status' : 'error',
                'message': str(e),
                'db_id'  : d_id,
            }, to=client_sid)

    bg = threading.Thread(
        target=_run_request_summarize,
        args=(text, db_id, sid, txt_filename)
    )
    bg.daemon = True
    bg.start()
    print(f"[Server] request_summarize: DB {db_id} — BG thread started", flush=True)


# ══════════════════════════════════════════════════════════
# ② UPLOAD TRANSCRIPTION — REST Endpoints
# ══════════════════════════════════════════════════════════

ALLOWED_EXT      = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', 'mp3', 'wav'}
_upload_lock     = threading.Lock()

file_cfg    = FileConfig(model_size="small", language="id")
file_cfg.output_dir = HASIL_DIR   # ← samakan dengan Live: simpan ke notulensi_rapat/hasil/
sum_cfg     = SummaryConfig()
summarizer  = LexRankSummarizer(sum_cfg)


# ── DB Helper ─────────────────────────────────────────────────────────────────

def save_to_db(judul: str, tipe: str, txt_path: str, ringkasan: str, durasi_detik: int = 0) -> int:
    """
    Simpan record notulensi ke database MySQL.
    Return id baris yang baru diinsert, atau 0 jika gagal.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            sql = """
                INSERT INTO notulensi_hasil
                    (judul_rapat, waktu_rapat, tipe_transkripsi, transkrip_txt, durasi_detik, ringkasan, file_pdf)
                VALUES (%s, NOW(), %s, %s, %s, %s, '')
            """
            cur.execute(sql, (judul, tipe, txt_path, durasi_detik, ringkasan))
            conn.commit()
            new_id = cur.lastrowid
        conn.close()
        print(f"[Server] ✓ DB: record #{new_id} disimpan ({tipe})", flush=True)
        return new_id
    except Exception as e:
        print(f"[Server] ✗ DB error: {e}", flush=True)
        return 0


def update_summary_in_db(db_id: int, ringkasan: str) -> bool:
    """
    Update kolom ringkasan untuk id tertentu.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            sql = "UPDATE notulensi_hasil SET ringkasan = %s WHERE id = %s"
            cur.execute(sql, (ringkasan, db_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Server] ✗ Update DB error: {e}", flush=True)
        return False

def update_transkrip_in_db(db_id: int, txt_path: str) -> bool:
    """
    Update kolom transkrip_txt untuk id tertentu.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            sql = "UPDATE notulensi_hasil SET transkrip_txt = %s WHERE id = %s"
            cur.execute(sql, (txt_path, db_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Server] ✗ Update Transkrip DB error: {e}", flush=True)
        return False


def update_durasi_in_db(db_id: int, durasi_detik: int) -> bool:
    """
    Update kolom durasi_detik untuk id tertentu.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            sql = "UPDATE notulensi_hasil SET durasi_detik = %s WHERE id = %s"
            cur.execute(sql, (durasi_detik, db_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Server] ✗ Update Durasi DB error: {e}", flush=True)
        return False



def allowed_file(filename: str) -> bool:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in ALLOWED_EXT


def safe_filename(filename: str) -> str:
    name = os.path.basename(filename)
    name = re.sub(r'[^\w\s\-.]', '', name).strip()
    return name or "upload"


@app.route('/status', methods=['GET'])
def api_status():
    """Health check — dicek oleh PHP saat halaman dibuka."""
    return jsonify({
        "status"      : "online",
        "live_model"  : live_model_loaded,
        "upload_model": file_cfg.model_size,
        "model"       : file_cfg.model_size,
        "language"    : file_cfg.language,
    })


@app.route('/transcribe', methods=['POST'])
def api_transcribe():
    """Upload file video → Whisper FileTranscriber → JSON hasil."""
    if 'video_file' not in request.files:
        return jsonify({"status": "error", "message": "Field 'video_file' tidak ditemukan"}), 400

    file = request.files['video_file']
    if not file.filename:
        return jsonify({"status": "error", "message": "Tidak ada file yang dipilih"}), 400
    if not allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else '?'
        return jsonify({"status": "error", "message": f"Format '{ext}' tidak didukung"}), 400

    ext         = file.filename.rsplit('.', 1)[-1].lower()
    ts          = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_name   = f"upload_{ts}.{ext}"
    temp_path   = os.path.join(UPLOAD_DIR, temp_name)
    orig_name   = safe_filename(file.filename)

    try:
        file.save(temp_path)
        print(f"[Server] Upload diterima: {temp_name} ({os.path.getsize(temp_path):,} bytes)", flush=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gagal menyimpan file: {e}"}), 500

    # ── Simpan Antrian Awal ke Database (Status: Transkripsi) ──────────
    judul = request.form.get('judul_rapat', '').strip()
    if not judul:
        judul = os.path.splitext(orig_name)[0].replace('_', ' ').title()

    db_id = save_to_db(
        judul    = judul,
        tipe     = 'Upload',
        txt_path = '',
        ringkasan= '[PROSES_TRANSKRIPSI]',
    )

    # ── Background Task: Transkripsi & Summarization ───────────
    def _run_full_bg_pipeline(t_path, original_n, db_record_id):
        try:
            # Tunggu giliran jika ada transkrip lain sedang berjalan
            print(f"[Server] BG Thread (ID {db_record_id}): Menunggu antrian lock...", flush=True)
            if not _upload_lock.acquire(blocking=True, timeout=3600):
                print(f"[Server] BG Thread (ID {db_record_id}): Timeout lock!", flush=True)
                update_summary_in_db(db_record_id, "[GAGAL_TRANSKRIPSI] Timeout menunggu antrian")
                try: os.unlink(t_path)
                except: pass
                return

            try:
                print(f"[Server] BG Thread (ID {db_record_id}): Mulai Transkripsi Whisper...", flush=True)
                # Proses transkripsi
                file_transcriber = FileTranscriber(file_cfg)
                file_transcriber.load_model()
                final_text = file_transcriber.transcribe_file(t_path)

                if not final_text:
                    update_summary_in_db(db_record_id, "[GAGAL_TRANSKRIPSI] Teks kosong atau gagal")
                    return

                # Simpan file .txt transkripsi
                out_path     = file_transcriber.save_result(final_text, original_n)
                txt_filename = os.path.basename(out_path)

                # Ambil durasi
                durasi = getattr(file_transcriber, 'last_duration_sec', 0)
                update_durasi_in_db(db_record_id, durasi)

                # Update database bahwa transkripsi selesai & masuk mode summary
                update_transkrip_in_db(db_record_id, txt_filename)
                update_summary_in_db(db_record_id, '[PROSES_SUMMARIZE]')
                print(f"[Server] BG Thread (ID {db_record_id}): ✓ Transkripsi selesai ({durasi}s). Menyusun ringkasan...", flush=True)

                # ── LexRank + Ollama Summarization ──
                result_bg = summarizer.summarize_with_debug(final_text)
                ringkasan_bg        = result_bg['ringkasan']
                ranked_sentences_bg = result_bg.get('ranked_sentences', [])
                lexrank_extractive  = result_bg.get('lexrank_extractive', '')
                ollama_result       = result_bg.get('ollama_result', None)
                if not ringkasan_bg:
                    ringkasan_bg = "Tidak ada ringkasan yang dihasilkan."

                # ── [1] Simpan ringkasan UTAMA ke hasil_summarize/ (tidak diubah) ──
                sum_filename = txt_filename.replace("transkrip_", "ringkasan_")
                sum_path = os.path.join(HASIL_SUMMARIZE_DIR, sum_filename)
                with open(sum_path, "w", encoding="utf-8") as sf:
                    sf.write("=== RINGKASAN RAPAT (LexRank 6-Step) ===\n")
                    sf.write(f"Sumber    : {txt_filename}\n")
                    sf.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
                    sf.write(f"Model     : Whisper {file_cfg.model_size}\n")
                    sf.write(f"{'=' * 40}\n\n")
                    sf.write(ringkasan_bg)
                print(f"[Server] BG Thread: ✓ Ringkasan utama disimpan ke {sum_filename}", flush=True)

                # ── [2] Simpan hasil LexRank EXTRACTIVE ke hasil_summarize/Lexrank/ ──
                if lexrank_extractive:
                    lexrank_filename = "lexrank_" + txt_filename.replace("transkrip_", "")
                    lexrank_path = os.path.join(HASIL_LEXRANK_DIR, lexrank_filename)
                    with open(lexrank_path, "w", encoding="utf-8") as lf:
                        lf.write("=== HASIL LEXRANK EXTRACTIVE ===\n")
                        lf.write(f"Sumber    : {txt_filename}\n")
                        lf.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
                        lf.write(f"Model     : Whisper {file_cfg.model_size}\n")
                        lf.write(f"{'=' * 40}\n\n")
                        lf.write(lexrank_extractive)
                    print(f"[Server] BG Thread: ✓ LexRank extractive disimpan ke Lexrank/{lexrank_filename}", flush=True)

                # ── [3] Simpan hasil OLLAMA ABSTRACTIVE ke hasil_summarize/Ollama/ ──
                if ollama_result:
                    ollama_filename = "ollama_" + txt_filename.replace("transkrip_", "")
                    ollama_path = os.path.join(HASIL_OLLAMA_DIR, ollama_filename)
                    with open(ollama_path, "w", encoding="utf-8") as of:
                        of.write("=== HASIL OLLAMA ABSTRACTIVE ===\n")
                        of.write(f"Sumber    : {txt_filename}\n")
                        of.write(f"Dibuat    : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
                        of.write(f"Model     : Whisper {file_cfg.model_size} + {sum_cfg.ollama_model}\n")
                        of.write(f"{'=' * 40}\n\n")
                        of.write(ollama_result)
                    print(f"[Server] BG Thread: ✓ Ollama abstractive disimpan ke Ollama/{ollama_filename}", flush=True)
                else:
                    print(f"[Server] BG Thread: ℹ Ollama tidak tersedia/gagal — file Ollama tidak dibuat", flush=True)

                # ── Update Database & debug JSON (tidak diubah) ──
                update_summary_in_db(db_record_id, ringkasan_bg)
                import json as _json
                debug_path = sum_path.replace('.txt', '_debug.json')
                try:
                    with open(debug_path, 'w', encoding='utf-8') as df:
                        _json.dump(ranked_sentences_bg, df, ensure_ascii=False, indent=2)
                except Exception:
                    pass
                print(f"[Server] BG Thread: ✓ Database ID {db_record_id} diupdate dengan ringkasan", flush=True)

            except Exception as bg_e:
                print(f"[Server] ⚠ BG Thread Exception: {bg_e}", flush=True)
                update_summary_in_db(db_record_id, f"[GAGAL_TRANSKRIPSI] Error: {bg_e}")
            finally:
                _upload_lock.release()
                # Hapus temporer video audio
                try:
                    if os.path.exists(t_path): os.unlink(t_path)
                except Exception as e_rm:
                    print(f"Warning: gagal hapus tmp {t_path}: {e_rm}", flush=True)

        except Exception as outer_e:
             print(f"[Server] ⚠ BG Thread Fatal Error: {outer_e}", flush=True)
             update_summary_in_db(db_record_id, "[GAGAL] Error background thread")

    # Trigger background thread
    bg_thread = threading.Thread(target=_run_full_bg_pipeline, args=(temp_path, orig_name, db_id))
    bg_thread.start()

    print(f"[Server] ✓ HTTP API merespons instan. Whisper pindah ke Background. DB id={db_id}", flush=True)

    return jsonify({
        "status": "success",
        "message": "Mengantri untuk diproses Whisper AI di background.",
        "db_id": db_id,
        "judul": judul,
    })


# Endpoint /download dan /download_summary dihapus.
# File .txt kini disimpan di folder web dan dapat diakses langsung via Apache:
#   http://localhost/notulensi_rapat/hasil/transkrip_xxx.txt
#   http://localhost/notulensi_rapat/hasil_summarize/ringkasan_xxx.txt


@app.route('/api/check_summary/<int:db_id>', methods=['GET'])
def api_check_summary(db_id):
    """Endpoint untuk polling status ringkasan dari DB."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("SELECT ringkasan, transkrip_txt, judul_rapat FROM notulensi_hasil WHERE id = %s", (db_id,))
            row = cur.fetchone()
        conn.close()

        if row:
            ringkasan = row[0]
            txt_file = row[1]
            judul = row[2]

            is_processing_transcription = (ringkasan == '[PROSES_TRANSKRIPSI]')
            is_processing_sum = (ringkasan == '[PROSES_SUMMARIZE]')

            # Coba baca data debug ranking LexRank dari file JSON
            import json as _json
            lexrank_debug = []
            if txt_file and not is_processing_transcription and not is_processing_sum:
                sum_fname = txt_file.replace('transkrip_', 'ringkasan_').replace('.txt', '_debug.json')
                debug_path = os.path.join(HASIL_SUMMARIZE_DIR, sum_fname)
                try:
                    if os.path.exists(debug_path):
                        with open(debug_path, 'r', encoding='utf-8') as df:
                            lexrank_debug = _json.load(df)
                except Exception:
                    pass

            return jsonify({
                "status"       : "success",
                "ringkasan"    : ringkasan,
                "transkrip_txt": txt_file,
                "judul"        : judul,
                "is_processing": (is_processing_transcription or is_processing_sum),
                "lexrank_debug": lexrank_debug,
            })
        else:
            return jsonify({"status": "error", "message": "Record not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ══════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 60, flush=True)
    print("  🎙  Notulensi Rapat — Unified Whisper Server", flush=True)
    print("  ─────────────────────────────────────────────", flush=True)
    print(f"  Live Transcription  →  Socket.IO  (port 5000)", flush=True)
    print(f"  Upload Transcription → REST API   (port 5000)", flush=True)
    print(f"  Hasil transkripsi   →  {HASIL_DIR}", flush=True)
    print(f"  URL                 →  http://localhost:5000", flush=True)
    print("=" * 60, flush=True)
    print(flush=True)

    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )
