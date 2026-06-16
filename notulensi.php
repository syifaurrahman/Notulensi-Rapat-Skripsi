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
        <!-- DEBUG PANEL: LexRank Ranking (muncul setelah summarize selesai) -->
        <div id="lexrankDebugPanel" style="display:none; margin-top:16px;">
            <div style="background:#1e1e2e; border-radius:16px; overflow:hidden; border:1px solid #313145;">
                <div style="display:flex; align-items:center; justify-content:space-between;
                            padding:12px 18px; background:#252538; border-bottom:1px solid #313145;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#22d3ee;display:inline-block;
                                     box-shadow:0 0 6px #22d3ee;"></span>
                        <span style="font-family:'Courier New',monospace; font-size:0.78rem;
                                     color:#94a3b8; font-weight:600; letter-spacing:.05em;">
                            DEBUG · LexRank Sentence Ranking
                        </span>
                    </div>
                    <span style="font-size:0.7rem;color:#475569;font-family:monospace;"
                          id="lexrankTotalCount"></span>
                </div>
                <div id="lexrankDebugList"
                     style="max-height:260px; overflow-y:auto; padding:10px 0;
                            font-family:'Courier New',monospace; font-size:0.75rem;">
                </div>
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
        // ── LexRank Debug Panel ──────────────────────────────
        function renderLexrankDebug(ranked) {
            const panel = document.getElementById('lexrankDebugPanel');
            const list  = document.getElementById('lexrankDebugList');
            const count = document.getElementById('lexrankTotalCount');
            if (!panel || !list || !Array.isArray(ranked) || ranked.length === 0) return;

            count.textContent = ranked.length + ' kalimat';
            list.innerHTML = '';

            ranked.forEach(item => {
                const scoreBar = Math.round((item.score || 0) * 100);
                const isTop3   = item.rank <= 3;
                const rankColor = item.rank === 1 ? '#fbbf24'
                                : item.rank === 2 ? '#94a3b8'
                                : item.rank === 3 ? '#cd7c3a'
                                : '#475569';

                const row = document.createElement('div');
                row.style.cssText = `
                    display:flex; align-items:flex-start; gap:10px;
                    padding:7px 16px;
                    border-bottom:1px solid #252538;
                    ${isTop3 ? 'background:rgba(34,211,238,0.04);' : ''}
                `;
                row.innerHTML = `
                    <span style="min-width:28px;text-align:right;font-weight:700;
                                 color:${rankColor};font-size:0.8rem;margin-top:1px;">
                        ${item.rank}.
                    </span>
                    <div style="flex:1; min-width:0;">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                            <div style="flex:1;height:4px;background:#2a2a3e;border-radius:2px;overflow:hidden;">
                                <div style="height:100%;width:${scoreBar}%;
                                            background:${isTop3 ? '#22d3ee' : '#334155'};
                                            border-radius:2px;transition:width .4s;"></div>
                            </div>
                            <span style="font-size:0.68rem;color:${isTop3 ? '#22d3ee' : '#475569'};
                                         min-width:38px;text-align:right;">
                                ${(item.score || 0).toFixed(4)}
                            </span>
                        </div>
                        <div style="color:${isTop3 ? '#e2e8f0' : '#64748b'};
                                    font-size:0.72rem;line-height:1.5;word-break:break-word;
                                    white-space:normal;font-family:'Inter',sans-serif;">
                            ${item.sentence || ''}
                        </div>
                    </div>
                `;
                list.appendChild(row);
            });

            panel.style.display = 'block';
        }

        // Hook ke event summarize_done dari live-transcription.js
        document.addEventListener('lexrank_debug_ready', function(e) {
            if (e.detail && Array.isArray(e.detail)) {
                renderLexrankDebug(e.detail);
            }
        });

        // Jam real-time: ticker interval
        let _waktuTicker = null;

        function _formatWaktu() {
            const b = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];
            const h = ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'];
            const now  = new Date();
            const hari = h[now.getDay()];
            const tgl  = now.getDate();
            const bln  = b[now.getMonth()];
            const thn  = now.getFullYear();
            const jam  = String(now.getHours()).padStart(2, '0');
            const mnt  = String(now.getMinutes()).padStart(2, '0');
            const dtk  = String(now.getSeconds()).padStart(2, '0');
            return `${hari}, ${tgl} ${bln} ${thn} · ${jam}:${mnt}:${dtk}`;
        }

        function _mulaiTickerWaktu() {
            const waktuInput = document.getElementById('waktu-rapat');
            if (!waktuInput) return;
            // Langsung isi sekali
            waktuInput.value = _formatWaktu();
            // Perbarui setiap detik
            if (_waktuTicker) clearInterval(_waktuTicker);
            _waktuTicker = setInterval(() => {
                waktuInput.value = _formatWaktu();
            }, 1000);
        }

        function _stopTickerWaktu() {
            if (_waktuTicker) { clearInterval(_waktuTicker); _waktuTicker = null; }
            const waktuInput = document.getElementById('waktu-rapat');
            if (waktuInput) waktuInput.value = '';
        }

        // Tombol "Automatic set" tetap bisa dipakai manual
        function setWaktuRealtime() { _mulaiTickerWaktu(); }

        // Auto-isi waktu: mulai ticker saat judul diketik, stop + kosongkan saat dihapus
        document.addEventListener('DOMContentLoaded', () => {
            const meetingInput = document.getElementById('meetingName');
            if (meetingInput) {
                meetingInput.addEventListener('input', function() {
                    if (this.value.trim() !== '') {
                        _mulaiTickerWaktu();
                    } else {
                        _stopTickerWaktu();
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