# 🎙 Whisper Transcription — Voice to Text untuk Rapat

Transkripsi otomatis **realtime** (via mikrofon) dan **offline** (via file video MP4) menggunakan [OpenAI Whisper](https://github.com/openai/whisper), dilengkapi **noise reduction** dan **anti-hallucination** untuk hasil transkripsi yang bersih dan akurat.

---

## 📁 Struktur Project

```
whispertranscription/
│
├── app.py              # Live transcription via mikrofon (realtime)
├── app2.py             # Library utama + standalone transkripsi video (interaktif)
├── run_video_mp4.py    # Runner transkripsi video MP4 (via argumen / pilih menu)
│
├── hasil/              # Output hasil transkripsi (.txt)
└── README.md
```

---

## 🧩 Penjelasan File

### `app.py` — Live Transcription (Realtime via Mikrofon)
Transkripsi suara secara **langsung dari mikrofon**, ditampilkan realtime di terminal, kemudian disimpan saat `Ctrl+C`.

```bash
python app.py
```
- Pilih ID mikrofon dari daftar
- Bicara → teks muncul realtime
- `Ctrl+C` → simpan ke `hasil/transkrip_YYYYMMDD_HHMMSS.txt`

---

### `app2.py` — Library Utama + Standalone Video Transcription
Berisi semua fungsi inti dan konfigurasi global. Bisa dijalankan langsung (interaktif pilih file video).

```bash
python app2.py
```
- Scan folder, pilih nomor video dari tabel
- Proses: Ekstrak Audio → Noise Reduction → Chunking → Transkripsi
- Simpan ke `hasil/`

---

### `run_video_mp4.py` — Runner Video MP4
Script peluncur yang menggunakan `app2.py` sebagai engine. Mendukung argumen langsung.

```bash
# Tampilkan menu pilih video
python run_video_mp4.py

# Langsung ke file tertentu
python run_video_mp4.py "nama_video.mp4"
python run_video_mp4.py "C:/path/to/video_rapat.mp4"
```

---

## ⚙️ Fitur Utama

### 🔇 Noise Reduction
- Library `noisereduce` — mengurangi noise stasioner (AC, kipas, hum ruangan)
- Normalisasi amplitude audio sebelum transkripsi
- Resampling akurat via `scipy.signal.resample_poly`

### 🛡️ Anti-Hallucination
| Parameter | Nilai | Fungsi |
|---|---|---|
| `compression_ratio_threshold` | `2.2` | Buang teks yang terlalu repetitif |
| `no_speech_threshold` | `0.6` | Abaikan segment tidak yakin |
| `logprob_threshold` | `-1.0` | Filter berdasarkan log-probability |
| `condition_on_previous_text` | `False` | Cegah carry-over halusinasi |
| `temperature` | `(0.0, 0.2, 0.4, 0.6)` | Fallback suhu bertahap |
| `is_hallucination()` | — | Deteksi frasa & pengulangan halusinasi |

### ⚡ Auto-detect GPU/CPU
- Menggunakan `torch.cuda.is_available()` — otomatis pilih CUDA jika tersedia
- Fallback ke CPU jika GPU tidak ada atau error

---

## 📦 Instalasi

### 1. Install Python dependencies
```bash
pip install openai-whisper noisereduce soundfile sounddevice numpy scipy rich
```

### 2. Install ffmpeg
Download dari [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) dan tambahkan ke PATH sistem.

Verifikasi:
```bash
ffmpeg -version
```

---

## 🚀 Quick Start

```bash
# Live transcription dari mikrofon
python app.py

# Transkripsi file video MP4
python run_video_mp4.py "video_rapat.mp4"
```

Hasil disimpan otomatis di folder `hasil/`.

---

## ⚙️ Konfigurasi

Ubah nilai di bagian `KONFIGURASI` dalam `app2.py`:

```python
MODEL_SIZE   = "medium"   # tiny | base | small | medium | large
LANGUAGE     = "id"       # Kode bahasa (id = Indonesia)
CHUNK_SECONDS = 30        # Durasi setiap chunk transkripsi (detik)
```

> **Model size vs akurasi:** `large` paling akurat tapi paling lambat. `medium` direkomendasikan untuk keseimbangan kecepatan & akurasi.

---

## 📝 Format Output

```
=== TRANSKRIPSI RAPAT ===
File Video  : C:\path\to\video.mp4
Dibuat      : 22 February 2026, 01:05:41
Model       : Whisper medium
========================================

Hasil transkripsi teks di sini...
```

---

## 🛠️ Teknologi

- [OpenAI Whisper](https://github.com/openai/whisper) — Speech-to-text engine
- [noisereduce](https://github.com/timsainburg/noisereduce) — Noise reduction
- [sounddevice](https://python-sounddevice.readthedocs.io/) — Input mikrofon realtime
- [ffmpeg](https://ffmpeg.org/) — Ekstrak audio dari video
- [Rich](https://github.com/Textualize/rich) — UI terminal
- [SciPy](https://scipy.org/) — Resampling audio
