"""
app.py — Entry Point Utama
==========================
File ini adalah satu-satunya yang perlu dijalankan:

  python app.py

Untuk mengubah konfigurasi (model, bahasa, threshold VAD, dll),
edit parameter di dalam Config() di bawah ini.
Tidak perlu menyentuh file lain.
"""

from config import Config
from live_app import LiveTranscriptionApp


if __name__ == "__main__":
    # ── Konfigurasi ─────────────────────────────────────────────────────
    # Edit di sini untuk mengubah perilaku aplikasi.
    # Semua opsi tersedia di config.py (dengan penjelasan masing-masing).
    config = Config(
        model_size      = "small",   # tiny | base | small | medium | large
        language        = "id",      # Bahasa Indonesia
        # use_gpu otomatis: pakai GPU jika CUDA tersedia, CPU jika tidak
        use_autocorrect = True,      # Auto-correct dengan LanguageTool
        vad_threshold   = 0.01,      # Sensitivitas VAD (naikkan jika banyak noise)
        debug_rms       = True,      # Tampilkan nilai RMS di log (set False untuk tampilan bersih)
        min_process_sec = 2.5,       # Detik audio minimal sebelum diproses
        silence_pause_sec = 1.2,     # Detik hening sebelum kalimat di-commit
    )
    # ────────────────────────────────────────────────────────────────────

    app = LiveTranscriptionApp(config)
    app.run()