<?php
require_once 'cek_login.php';

// Hanya Admin (level = 1) yang boleh akses halaman Notulensi
if ($level_user != 1) {
    header("Location: dashboard.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.5, user-scalable=yes">
    <title>Notulensi Rapat · Fixed Sidebar</title>
    <!-- Font Awesome 6 (free) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Font: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>

<body>
    <?php include 'sidebar.php'; ?>

    <!-- MAIN CONTENT - BISA DI SCROLL -->
    <main class="main-content">
        <!-- top bar -->
        <div class="top-bar">
            <div class="page-title">
                <h1>Notulensi</h1>
                <div class="breadcrumb"> Setup notulensi rapat</div>
            </div>
            <div class="header-date">
                <i class="fas fa-microphone"></i>
                <span id="realtime-clock"></span>
            </div>
        </div>

        <!-- MEETING SETUP CARD -->
        <div class="setup-card">
            <div class="section-label">
                <i class="fas fa-gear"></i> MEETING SETUP
            </div>
            <div class="setup-grid">
                <!-- kolom kiri: nama rapat + waktu -->
                <div class="meeting-info-card">
                    <div class="input-group">
                        <div class="input-label"><i class="far fa-pen-to-square"></i> Masukkan nama Rapat</div>
                        <input class="input-field" type="text" placeholder="cth: Sprint Planning - Marketing"
                            value="Evaluasi Proyek AI">
                    </div>
                    <div class="input-group">
                        <div class="input-label"><i class="far fa-clock"></i> Waktu</div>
                        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
                            <input id="waktu-rapat" class="input-field" style="width: auto; flex:1;"
                                type="text" placeholder="Pilih waktu" readonly>
                            <span class="automatic-badge" onclick="setTanggalHariIni()">
                                <i class="fas fa-robot"></i> Automatic set
                            </span>
                        </div>
                    </div>
                </div>
                <!-- kolom kanan: Audio Control -->
                <div class="audio-section">
                    <div style="font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                        <i class="fas fa-headphones" style="color:#2463eb;"></i> Audio Control
                    </div>

                    <!-- status : idle -->
                    <div class="status-row">
                        <span class="status-label"><i class="far fa-circle"></i> Status</span>
                        <span class="status-value idle"><i class="fas fa-pause-circle"></i> idle</span>
                    </div>

                    <!-- pilih microphone -->
                    <div class="microphone-selector">
                        <span><i class="fas fa-microphone"></i> Microphone</span>
                        <select>
                            <option>--Pilih Microphone--</option>
                            <option>Built-in Microphone (Realtek)</option>
                            <option>Headset (Jabra Evolve)</option>
                            <option>USB Microphone (Yeti)</option>
                        </select>
                    </div>

                    <!-- action buttons Start / End Listening -->
                    <div class="action-buttons">
                        <span class="btn btn-primary"><i class="fas fa-play"></i> Start Listening</span>
                        <span class="btn btn-outline"><i class="fas fa-stop"></i> End Listening</span>
                    </div>
                    <div style="margin-top: 14px; font-size:0.75rem; color:#6d8ab0;">
                        <i class="fas fa-info-circle"></i> Klik Start untuk memulai transkripsi langsung
                    </div>
                </div>
            </div>
        </div>

        <!-- UPLOAD VIDEO RAPAT CARD -->
        <div class="setup-card upload-video-card">
            <div class="section-label">
                <i class="fas fa-film"></i> Upload Video Rapat
            </div>
            <div class="upload-video-body">
                <!-- Drop zone -->
                <input id="inputVideoFile" type="file" accept="video/*" style="display:none;">
                <label class="upload-dropzone-label" for="inputVideoFile">
                    <div class="upload-dropzone" id="uploadDropzone">
                        <div class="upload-dropzone-icon">
                            <i class="fas fa-cloud-arrow-up"></i>
                        </div>
                        <span class="upload-dropzone-title">Drag &amp; drop video rapat di sini</span>
                        <span class="upload-dropzone-sub">atau klik untuk memilih file dari komputer</span>
                        <span class="btn btn-outline upload-browse-btn">
                            <i class="fas fa-folder-open"></i> Browse File
                        </span>
                    </div>
                </label>
                <!-- Format info -->
                <div class="upload-format-info">
                    <i class="fas fa-circle-info"></i>
                    Format didukung: <strong>MP4, MOV, AVI, MKV, WEBM</strong> &nbsp;·&nbsp; Ukuran maks: <strong>500 MB</strong>
                </div>
            </div>
        </div>

        <!-- LIVE TRANSCRIPTION CARD -->
        <div class="transcript-card">
            <div class="transcript-header">
                <h2><i class="fas fa-pen-clip" style="color:#2463eb; margin-right: 8px;"></i> Live Transcription</h2>
                <span class="live-badge"><i class="fas fa-circle"></i> LIVE</span>
            </div>

            <div class="transcript-content">
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                    cillum dolore eu fugiat nulla pariatur, sed ut perspiciatis unde omnis iste natus error sit
                    voluptatem accusantium doloremque laudantium, totam rem aperiam.
                </p>
                <p>
                    👤 Andi: Menurut saya kita perlu memprioritaskan fitur AI. Lorem ipsum dolor sit amet, consectetur
                    adipiscing elit.
                    👤 Budi: Setuju, tetapi harus diperhatikan alokasi sumber daya.
                </p>
                <p>
                    <span style="color:#4f7092;">[transkrip berlanjut ...]</span> Ut enim ad minim veniam, quis nostrud
                    exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </p>
            </div>

            <div class="footnote">
                <span><i class="far fa-clock"></i> 00:12:47 durasi</span>
                <span><i class="fas fa-save"></i> auto-save aktif</span>
            </div>
        </div>

        <!-- tombol simpan notulensi -->
        <div class="action-footer">
            <span class="btn btn-outline"><i class="fas fa-times"></i> Batal</span>
            <span class="btn btn-primary" style="background: #1f4faf;"><i class="fas fa-check"></i> Simpan
                Notulen</span>
        </div>
    </main>
    <script>
        const BULAN = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];

        function setTanggalHariIni() {
            const now   = new Date();
            const tgl   = now.getDate();
            const bulan = BULAN[now.getMonth()];
            const tahun = now.getFullYear();
            document.getElementById('waktu-rapat').value = `${tgl} ${bulan} ${tahun}`;
        }

        // Auto-isi saat halaman pertama kali dibuka
        document.addEventListener('DOMContentLoaded', setTanggalHariIni);
    </script>
</body>

</html>