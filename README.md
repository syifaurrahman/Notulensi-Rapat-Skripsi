# Notulensi Rapat Skripsi

Aplikasi manajemen notulensi rapat otomatis menggunakan teknologi transkripsi suara ke teks. Proyek ini dirancang untuk memudahkan pencatatan hasil rapat secara real-time maupun melalui unggahan video.

## 🚀 Fitur Utama

- **Dashboard Interaktif**: Ringkasan aktivitas rapat, statistik mingguan, dan daftar rapat terbaru.
- **Live Transcription**: Transkripsi langsung dari mikrofon saat rapat berlangsung.
- **Upload Video Rapat**: Unggah file video (MP4, MOV, AVI, dll.) untuk mendapatkan transkripsi otomatis.
- **Manajemen Notulensi**: Simpan, lihat, dan kelola hasil notulensi rapat dengan mudah.
- **Sistem Pengguna**: Login aman dengan tingkatan akses (Admin/User).
- **Database Migration**: Skrip otomatis untuk setup database dan data awal.

## 🛠️ Tech Stack

- **Backend**: PHP (Vanilla)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, Font Awesome, Google Fonts (Inter)
- **Database**: MySQL
- **Transcription Engine**: Python with OpenAI Whisper (terletak di folder `whispertranscription`)
- **Summarization**: LexRank + Ollama (LLM lokal)

---

## 🐳 Cara Menjalankan dengan Docker (Direkomendasikan)

### Persyaratan
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — satu-satunya yang perlu diinstall

### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/syifaurrahman/Notulensi-Rapat-Skripsi.git
cd Notulensi-Rapat-Skripsi

# 2. Jalankan semua container
docker compose up --build -d

# 3. Download model AI untuk summarization (jalankan SEKALI)
docker exec notulensi_ollama ollama pull llama3.2:3b

# 4. Buka aplikasi di browser
# http://localhost
```

### Login Bawaan
| Email | Password | Level |
|-------|----------|-------|
| `Admin@admin.com` | `admin1234` | Admin |
| `user@user.com` | `user1234` | User |

### Menghentikan Aplikasi
```bash
docker compose down
```

---

## 📋 Persyaratan Sistem (Tanpa Docker / Manual)

- PHP 8.x
- MySQL / MariaDB
- Laragon atau XAMPP (untuk Windows)
- Python 3.10+ (untuk fitur transkripsi)
- FFmpeg (diperlukan oleh Whisper)
- Ollama + model llama3.2:3b

## 🔧 Instalasi Manual (tanpa Docker)

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/syifaurrahman/Notulensi-Rapat-Skripsi.git
   cd Notulensi-Rapat-Skripsi
   ```

2. **Setup Database**:
   - Pastikan MySQL Anda berjalan.
   - Buka browser dan jalankan `http://localhost/notulensi_rapat/migrate.php`

3. **Setup Python**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install openai-whisper flask flask-socketio flask-cors noisereduce soundfile sounddevice numpy scipy scikit-learn rich pymysql
   ```

4. **Jalankan Python Server**:
   ```bash
   python whispertranscription/server.py
   ```

## ⚠️ Catatan
Proyek ini masih dalam tahap pengembangan (belum sempurna). Beberapa fitur mungkin memerlukan konfigurasi manual tambahan pada bagian mesin transkripsi Python.

---
Dikembangkan oleh [Syifaurrahman](https://github.com/syifaurrahman)


## 📋 Persyaratan Sistem

- PHP 8.x
- MySQL / MariaDB
- Laragon atau XAMPP (untuk Windows)
- Python 3.10+ (untuk fitur transkripsi)
- FFmpeg (diperlukan oleh Whisper)

## 🔧 Instalasi

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/syifaurrahman/Notulensi-Rapat-Skripsi.git
   cd Notulensi-Rapat-Skripsi
   ```

2. **Setup Database**:
   - Pastikan MySQL Anda berjalan.
   - Buka browser dan jalankan `http://localhost/notulensi_rapat/migrate.php` atau jalankan via terminal:
     ```bash
     php migrate.php
     ```
   - Ini akan membuat database `notulensi` dan tabel yang diperlukan.

3. **Setup Whisper (Opsional untuk Transkripsi)**:
   - Masuk ke folder transkripsi: `cd whispertranscription`
   - Buat virtual environment dan instal dependensi (sesuaikan dengan panduan di folder tersebut).

## 📖 Cara Penggunaan

1. Login menggunakan akun default:
   - **Email**: `Admin@admin.com`
   - **Password**: `admin1234`
2. Navigasi ke menu **Notulensi** untuk memulai transkripsi langsung atau unggah video rapat.
3. Hasil transkripsi dapat disimpan dan dilihat di menu **Report** (jika tersedia) atau Dashboard.

## ⚠️ Catatan
Proyek ini masih dalam tahap pengembangan (belum sempurna). Beberapa fitur mungkin memerlukan konfigurasi manual tambahan pada bagian mesin transkripsi Python.

---
Dikembangkan oleh [Syifaurrahman](https://github.com/syifaurrahman)
