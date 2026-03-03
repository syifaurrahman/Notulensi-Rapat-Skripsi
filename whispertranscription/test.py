import whisper
import sounddevice as sd
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
import queue
import sys
import datetime
import os

console = Console()

def select_mic():
    table = Table(title="Daftar Microphone Tersedia")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Nama Device", style="magenta")
    table.add_column("Default Sample Rate", justify="right", style="green")

    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            table.add_row(str(i), dev['name'], f"{int(dev['default_samplerate'])} Hz")
    
    console.print(table)
    try:
        choice = int(console.input("[bold yellow]Masukkan ID Mic: [/bold yellow]"))
        device_info = sd.query_devices(choice, 'input')
        return choice, int(device_info['default_samplerate'])
    except Exception as e:
        console.print(f"[bold red]Error: {e}. Pakai default.[/bold red]")
        return None, 16000

# --- KONFIGURASI ---
DEVICE_ID, MIC_SAMPLERATE = select_mic()
WHISPER_SAMPLERATE = 16000
MODEL_SIZE = "base"
VAD_THRESHOLD = 0.005  # Ambil nilai volume minimal (0.001 - 0.02) agar bising tipis tidak masuk
audio_queue = queue.Queue()

console.print(f"\n[bold green]Memuat Whisper {MODEL_SIZE}...[/bold green]")
# Pastikan kamu menggunakan .to("cuda") jika menggunakan GPU Nvidia, 
# Hapus .to("cuda") jika hanya menggunakan CPU.
model = whisper.load_model(MODEL_SIZE).to("cuda")

def audio_callback(indata, frames, time, status):
    if status:
        console.log(status)
    audio_queue.put(indata.copy())

stream = sd.InputStream(
    device=DEVICE_ID, channels=1, samplerate=MIC_SAMPLERATE, 
    callback=audio_callback, blocksize=int(MIC_SAMPLERATE * 0.1)
)

audio_buffer = np.zeros(0, dtype='float32')
history_text = ""
current_text = ""
is_speaking = False

with stream:
    console.print(f"[bold cyan]Mic Aktif. Noise Gate: {VAD_THRESHOLD}[/bold cyan]")
    console.print("[dim]Tekan Ctrl+C untuk berhenti dan menyimpan teks.[/dim]\n")
    
    with Live(console=console, refresh_per_second=10) as live:
        try:
            while True:
                while not audio_queue.empty():
                    chunk = audio_queue.get()
                    audio_buffer = np.concatenate((audio_buffer, chunk.flatten()))

                # Proses setiap kali ada minimal 1 detik audio untuk responsivitas
                if len(audio_buffer) >= MIC_SAMPLERATE * 1.0:
                    
                    # 1. Cek Volume (VAD) hanya pada 1 detik terakhir
                    latest_audio = audio_buffer[-int(MIC_SAMPLERATE):]
                    rms = np.sqrt(np.mean(latest_audio**2))
                    
                    if rms < VAD_THRESHOLD:
                        # --- MODE HENING (SILENCE) ---
                        if is_speaking:
                            # Jika sebelumnya ada orang bicara, berarti ini akhir kalimat.
                            if current_text:
                                history_text += current_text + " "
                                current_text = ""
                            
                            # Kosongkan buffer agar kalimat berikutnya mulai dari nol
                            audio_buffer = np.zeros(0, dtype='float32')
                            is_speaking = False
                        
                        # Tampilkan history + indikator hening
                        display_text = history_text + "\n[dim]... (Hening / Menunggu suara) ...[/dim]"
                        live.update(Panel(display_text, title="Whisper Live", border_style="yellow"))
                        
                        # Jaga buffer hening tetap kecil agar memori tidak penuh
                        if len(audio_buffer) > MIC_SAMPLERATE:
                            audio_buffer = audio_buffer[-int(MIC_SAMPLERATE):]
                            
                    else:
                        # --- MODE BERBICARA (SPEAKING) ---
                        is_speaking = True
                        
                        # 2. Resample seluruh buffer yang sedang berjalan
                        if MIC_SAMPLERATE != WHISPER_SAMPLERATE:
                            indices = np.linspace(0, len(audio_buffer) - 1, int(len(audio_buffer) * WHISPER_SAMPLERATE / MIC_SAMPLERATE))
                            input_audio = audio_buffer[indices.astype(int)]
                        else:
                            input_audio = audio_buffer
                        
                        # 3. Transkripsi buffer aktif dengan Filter Anti-Looping
                        result = model.transcribe(
                            input_audio,
                            language="id",
                            fp16=True, # Ubah ke False jika pakai CPU
                            beam_size=5, # Naikkan ke 5 agar Whisper memikirkan ulang kalimatnya (tidak asal tebak)
                            temperature=(0.0, 0.2, 0.4), # Beri Whisper opsi suhu jika dia mulai berhalusinasi
                            condition_on_previous_text=False, # [PENTING] Mencegah kata berulang dari kalimat sebelumnya
                            compression_ratio_threshold=2.4,  # [PENTING] Fitur bawaan Whisper untuk membuang teks yang berulang-ulang
                            no_speech_threshold=0.6, 
                            logprob_threshold=-1.0 
                        )
                        
                        current_text = result["text"].strip()
                        
                        # Tampilkan history + teks yang sedang dikoreksi secara live
                        display_text = f"{history_text} [bold green]{current_text}[/bold green]"
                        live.update(Panel(display_text, title="[bold green]Suara Terdeteksi[/bold green]", border_style="green"))
                        
                        # Batasi buffer maksimal (15 detik) agar prosesor/GPU tidak kewalahan
                        if len(audio_buffer) > MIC_SAMPLERATE * 15:
                            history_text += current_text + " "
                            current_text = ""
                            audio_buffer = np.zeros(0, dtype='float32')

        except KeyboardInterrupt:
            # --- PENYIMPANAN HASIL (SAAT CTRL+C) ---
            final_result = (history_text + current_text).strip()
            live.update(Panel(final_result, title="[bold cyan]Transkripsi Selesai[/bold cyan]", border_style="cyan"))
            
            # Simpan ke file teks jika ada hasilnya
            if final_result:
                # Menentukan direktori penyimpanan
                save_dir = r"D:\TEST\hasil"
                
                # Membuat folder jika belum ada
                os.makedirs(save_dir, exist_ok=True)
                
                # Menggabungkan path folder dengan nama file
                filename = os.path.join(save_dir, f"transkrip_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(final_result)
                console.print(f"\n[bold green]✓ Hasil disimpan ke:[/bold green] {filename}")
            
            console.print("\n[bold red]Program dihentikan.[/bold red]")
