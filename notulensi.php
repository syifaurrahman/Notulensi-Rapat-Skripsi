<?php
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
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
    <title>Live Transcription · Notulensi Rapat</title>
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

    <!-- MAIN CONTENT -->
    <main class="main-content">
        <!-- top bar -->
        <div class="top-bar">
            <div class="page-title">
                <h1>Live Transcription</h1>
                <div class="breadcrumb">Notulensi &rsaquo; Transkripsi langsung dari mikrofon</div>
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
                        <input id="meetingName" class="input-field" type="text"
                            placeholder="cth: Sprint Planning - Marketing" value="">
                    </div>
                    <div class="input-group">
                        <div class="input-label"><i class="far fa-clock"></i> Waktu</div>
                        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
                            <input id="waktu-rapat" class="input-field" style="width: auto; flex:1;" type="text"
                                placeholder="Pilih waktu" readonly>
                            <span class="automatic-badge" onclick="setWaktuRealtime()">
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
                        <span class="status-value idle" id="statusValue">
                            <i class="fas fa-pause-circle" id="statusIcon"></i> Idle
                        </span>
                    </div>

                    <!-- pilih microphone (dynamic from browser API) -->
                    <div class="microphone-selector">
                        <span><i class="fas fa-microphone"></i> Microphone</span>
                        <select id="micSelect">
                            <option value="">Mendeteksi mikrofon...</option>
                        </select>
                    </div>

                    <!-- action buttons Start / End Listening -->
                    <div class="action-buttons">
                        <button class="btn btn-primary" id="startBtn" type="button">
                            <i class="fas fa-play"></i> Start Listening
                        </button>
                        <button class="btn btn-outline btn-disabled" id="stopBtn" type="button" disabled>
                            <i class="fas fa-stop"></i> End Listening
                        </button>
                    </div>
                    <div style="margin-top: 14px; font-size:0.75rem; color:#6d8ab0;">
                        <i class="fas fa-info-circle"></i> Klik Start untuk memulai transkripsi langsung.
                        Pastikan <strong>web_server.py</strong> sudah berjalan di terminal.
                    </div>
                </div>
            </div>
        </div>

        <!-- LIVE TRANSCRIPTION CARD -->
        <div class="transcript-card">
            <div class="transcript-header">
                <h2><i class="fas fa-pen-clip" style="color:#2463eb; margin-right: 8px;"></i> Live Transcription</h2>
                <span class="live-badge" id="liveBadge"><i class="fas fa-circle"></i> LIVE</span>
            </div>

            <div class="transcript-content" id="transcriptContent">
                <p class="transcript-placeholder">
                    <i class="fas fa-microphone-slash"></i>
                    Klik <strong>Start Listening</strong> untuk memulai transkripsi langsung.
                </p>
            </div>

            <div class="footnote">
                <span><i class="far fa-clock"></i> <span id="durationDisplay">00:00:00</span> durasi</span>
                <span class="save-info"><i class="fas fa-save"></i> auto-save aktif</span>
            </div>
        </div>

        <!-- tombol simpan notulensi -->
        <div class="action-footer">
            <span id="resetBtn" class="btn btn-outline" onclick="window.resetTranscription()">
                <i class="fas fa-redo"></i> Reset
            </span>
            <span class="btn btn-primary" style="background: #1f4faf;" onclick="saveNotulensi()">
                <i class="fas fa-check"></i> Simpan Notulen
            </span>
        </div>

        <!-- RINGKASAN PANEL (muncul setelah summarize selesai) -->
        <div id="summaryPanel" class="transcript-card" style="display:none; margin-top:24px; border-left:4px solid #2463eb;">
            <div class="transcript-header" style="margin-bottom:12px;">
                <h2><i class="fas fa-brain" style="color:#2463eb; margin-right:8px;"></i> Ringkasan Otomatis (LexRank)</h2>
                <a id="summaryReportLink" href="report.php" target="_blank"
                   style="display:none; align-items:center; gap:6px; font-size:0.8rem;
                          background:#2463eb; color:#fff; padding:6px 14px; border-radius:8px;
                          text-decoration:none; font-weight:600;">
                    <i class="fas fa-external-link-alt"></i> Lihat di Report
                </a>
            </div>
            <div id="summaryContent" class="transcript-content"
                 style="background:#f0f6ff; min-height:80px; font-size:0.93rem; line-height:1.75;">
                <p class="transcript-placeholder">
                    <i class="fas fa-spinner fa-spin"></i> Sedang memproses ringkasan...
                </p>
            </div>
        </div>
    </main>

    <!-- Socket.IO Client Library -->
    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
    <!-- jsPDF Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <!-- Live Transcription JS -->
    <script src="assets/js/live-transcription.js"></script>
    <!-- Clock & Utilities -->
    <script>
        // Fungsi memperbarui waktu ketika ditekan / otomatis
        function setWaktuRealtime() {
            const b = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];
            const h = ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'];
            
            const now   = new Date();
            const hari  = h[now.getDay()];
            const tgl   = now.getDate();
            const bulan = b[now.getMonth()];
            const tahun = now.getFullYear();
            const jam   = String(now.getHours()).padStart(2, '0');
            const mnt   = String(now.getMinutes()).padStart(2, '0');
            
            const waktuInput = document.getElementById('waktu-rapat');
            if (waktuInput) {
                waktuInput.value = `${hari}, ${tgl} ${bulan} ${tahun} · ${jam}:${mnt}`;
            }
        }
        
        // Auto-isi waktu HANYA SAAT user mulai mengetik nama rapat pertama kali
        document.addEventListener('DOMContentLoaded', () => {
            const meetingInput = document.getElementById('meetingName');
            if(meetingInput) {
                meetingInput.addEventListener('input', function() {
                    const waktuInput = document.getElementById('waktu-rapat');
                    if(this.value.trim() !== '' && waktuInput.value === '') {
                        setWaktuRealtime();
                    }
                });
            }
        });

        // Reset transcription — dipanggil langsung dari window.resetTranscription() di live-transcription.js

        // Save notulensi terintegrasi di live-transcription.js
        function saveNotulensi() {
            if (typeof processSaveNotulensi === 'function') {
                processSaveNotulensi();
            } else {
                alert('Fungsi simpan belum siap.');
            }
        }
    </script>
</body>

</html>