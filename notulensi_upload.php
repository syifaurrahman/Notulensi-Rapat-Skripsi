<?php
require_once 'cek_login.php';

if ($level_user != 1) {
    header("Location: dashboard.php");
    exit();
}

// Cek apakah Unified Server (Flask port 5000) sudah berjalan
$serverOnline = false;
$ch = curl_init('http://localhost:5000/status');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 2);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
$resp = curl_exec($ch);
curl_close($ch);
if ($resp) {
    $json = json_decode($resp, true);
    $serverOnline = isset($json['status']) && $json['status'] === 'online';
}

// Ambil antrean proses dari DB
define('DB_HOST', 'localhost');
define('DB_USER_DB', 'root');
define('DB_PASS_DB', '');
define('DB_NAME_DB', 'notulensi');
$conn = @mysqli_connect(DB_HOST, DB_USER_DB, DB_PASS_DB, DB_NAME_DB);
$active_processes = [];
if ($conn) {
    $res = mysqli_query($conn, "SELECT id, judul_rapat, ringkasan, created_at FROM notulensi_hasil WHERE ringkasan IN ('[PROSES_TRANSKRIPSI]', '[PROSES_SUMMARIZE]') ORDER BY id DESC");
    if ($res) {
        while ($r = mysqli_fetch_assoc($res)) {
            $active_processes[] = $r;
        }
    }
    mysqli_close($conn);
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.5, user-scalable=yes">
    <title>Upload Video · Notulensi Rapat</title>
    <!-- Unified Whisper Server: http://localhost:5000 (Live + Upload) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        /* ── Progress Bar ─────────────────────────────────── */
        .upload-progress-wrap {
            display: none;
            margin-top: 20px;
        }
        .upload-progress-label {
            font-size: 0.82rem;
            color: #6d8ab0;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .upload-progress-bar-track {
            width: 100%;
            height: 8px;
            background: #e2eaf5;
            border-radius: 99px;
            overflow: hidden;
        }
        .upload-progress-bar-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #2463eb, #60a5fa);
            border-radius: 99px;
            transition: width 0.4s ease;
            animation: progressPulse 1.5s infinite;
        }
        @keyframes progressPulse {
            0%   { opacity: 1; }
            50%  { opacity: 0.6; }
            100% { opacity: 1; }
        }
        .progress-status-text {
            font-size: 0.78rem;
            color: #6d8ab0;
            margin-top: 6px;
            text-align: center;
        }

        /* ── Hasil Transkripsi Card ───────────────────────── */
        #hasilCard {
            display: none;
            margin-top: 20px;
        }
        .hasil-text-box {
            background: #f0f4fb;
            border: 1px solid #dde5f5;
            border-radius: 10px;
            padding: 16px 20px;
            font-size: 0.9rem;
            line-height: 1.8;
            color: #1e293b;
            max-height: 350px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
        }
        .hasil-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
            font-size: 0.78rem;
            color: #6d8ab0;
        }
        .hasil-filename {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .btn-download-txt {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #2463eb;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 7px 16px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: background 0.2s;
        }
        .btn-download-txt:hover { background: #1f4faf; }

        /* ── Error Box ───────────────────────────────────── */
        .upload-error-box {
            display: none;
            margin-top: 14px;
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 10px;
            padding: 12px 16px;
            color: #991b1b;
            font-size: 0.85rem;
        }
        .upload-error-box i { margin-right: 6px; }

        /* ── Reset area baru ─────────────────────────────── */
        #resetUploadBtn {
            display: none;
            margin-top: 12px;
        }
    </style>
</head>

<body>
    <?php include 'sidebar.php'; ?>

    <main class="main-content">
        <!-- top bar -->
        <div class="top-bar">
            <div class="page-title">
                <h1>Upload Video Rapat</h1>
                <div class="breadcrumb">Notulensi &rsaquo; Upload video rapat untuk di-transkripsikan</div>
            </div>
            <div class="header-date">
                <i class="fas fa-cloud-arrow-up"></i>
                <span id="realtime-clock"></span>
            </div>
        </div>

        <!-- STATUS SERVER BADGE -->
        <?php if (!$serverOnline): ?>
        <div style="background:#fef3c7;border:1px solid #fcd34d;border-radius:10px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;gap:10px;font-size:0.85rem;color:#92400e;">
            <i class="fas fa-triangle-exclamation"></i>
            <span><strong>Upload Server belum berjalan.</strong> Jalankan terlebih dahulu:<br>
            <code style="background:#fff7ed;padding:2px 8px;border-radius:4px;">cd whispertranscription &amp;&amp; python server.py</code></span>
        </div>
        <?php else: ?>
        <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:10px 16px;margin-bottom:16px;display:flex;align-items:center;gap:10px;font-size:0.85rem;color:#166534;">
            <i class="fas fa-circle-check"></i> <strong>Upload Server online</strong> &nbsp;·&nbsp; Model: <strong><?php echo htmlspecialchars($json['model'] ?? 'small'); ?></strong>
        </div>
        <?php endif; ?>

        <!-- ACTIVE PROCESSES (Background Tracking) -->
        <?php if (!empty($active_processes)): ?>
        <div class="setup-card" id="processCard" style="border: 1px solid #93c5fd; background:#eff6ff;">
            <div class="section-label" style="color: #1e40af;">
                <i class="fas fa-microchip fa-spin"></i> Proses Berjalan (Background)
            </div>
            <div id="activeProcessList">
                <?php foreach ($active_processes as $p): ?>
                    <div class="active-job-item" data-processing-id="<?= $p['id'] ?>" style="background:white; border-radius:8px; padding:12px 16px; margin-bottom:10px; border:1px solid #bfdbfe; box-shadow:0 2px 4px rgba(0,0,0,0.02); display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight:600; font-size:0.9rem; color:#1e293b;"><?= htmlspecialchars($p['judul_rapat'] ?: 'Tanpa Judul') ?></div>
                            <div class="job-status-text" style="font-size:0.8rem; color:#2463eb; margin-top:4px;">
                                <i class="fas fa-circle-notch fa-spin"></i> 
                                <?= $p['ringkasan'] === '[PROSES_TRANSKRIPSI]' ? 'Mentranskripsi Audio (Whisper)...' : 'Meringkas (LexRank & Ollama)...' ?>
                            </div>
                        </div>
                        <a href="report.php" class="btn btn-outline" style="font-size:0.75rem; padding:6px 12px;">Lihat Report</a>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>

        <!-- UPLOAD VIDEO RAPAT CARD -->
        <div class="setup-card upload-video-card">
            <div class="section-label">
                <i class="fas fa-film"></i> Upload Video Rapat
            </div>
            <div class="upload-video-body">
                <!-- Drop zone -->
                <input id="inputVideoFile" type="file" accept="video/*,audio/*" style="display:none;">
                <label class="upload-dropzone-label" for="inputVideoFile" id="dropzoneLabel">
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
                    Format didukung: <strong>MP4, MOV, AVI, MKV, WEBM, MP3</strong> &nbsp;·&nbsp; Ukuran maks: <strong>500 MB</strong>
                </div>
            </div>
        </div>

        <!-- INPUT JUDUL RAPAT -->
        <div class="setup-card" id="judulCard">
            <div class="section-label">
                <i class="fas fa-tag"></i> Judul Rapat
            </div>
            <div style="padding: 4px 0 8px;">
                <input type="text"
                       id="inputJudulRapat"
                       placeholder="Contoh: Rapat Divisi Teknologi — 13 April 2026"
                       style="width:100%; padding:10px 14px; border:1.5px solid #dde5f5; border-radius:10px;
                              font-size:0.9rem; font-family:inherit; color:#1e293b; outline:none;
                              transition:border-color 0.2s;"
                       onfocus="this.style.borderColor='#2463eb'"
                       onblur="this.style.borderColor='#dde5f5'">
                <div style="font-size:0.75rem;color:#6d8ab0;margin-top:6px;">
                    Opsional — jika kosong, nama file video akan digunakan sebagai judul.
                </div>
            </div>
        </div>

        <!-- FILE SELECTED PREVIEW -->
        <div class="setup-card" id="filePreviewCard" style="display:none;">
            <div class="section-label">
                <i class="fas fa-video"></i> File Terpilih
            </div>
            <div class="file-preview-body">
                <div class="file-preview-info">
                    <div class="file-preview-icon">
                        <i class="fas fa-file-video"></i>
                    </div>
                    <div class="file-preview-details">
                        <span class="file-preview-name" id="fileName">-</span>
                        <span class="file-preview-size" id="fileSize">-</span>
                    </div>
                    <button class="btn btn-outline file-remove-btn" id="removeFileBtn" type="button">
                        <i class="fas fa-trash-alt"></i> Hapus
                    </button>
                </div>

                <!-- Progress Bar (muncul saat upload) -->
                <div class="upload-progress-wrap" id="progressWrap">
                    <div class="upload-progress-label">
                        <i class="fas fa-cog fa-spin"></i>
                        <span id="progressLabel">Mengunggah file...</span>
                    </div>
                    <div class="upload-progress-bar-track">
                        <div class="upload-progress-bar-fill" id="progressBar"></div>
                    </div>
                    <div class="progress-status-text" id="progressStatus">Mohon tunggu, proses ini mungkin memerlukan beberapa menit...</div>
                </div>

                <!-- Error Box -->
                <div class="upload-error-box" id="errorBox">
                    <i class="fas fa-circle-exclamation"></i>
                    <span id="errorMessage">Terjadi kesalahan.</span>
                </div>
            </div>
        </div>

        <!-- RINGKASAN CARD -->
        <div class="setup-card" id="ringkasanCard" style="display:none;">
            <div class="section-label">
                <i class="fas fa-list-check"></i> Ringkasan Otomatis (LexRank)
            </div>
            <div class="hasil-text-box" id="ringkasanTextBox" style="background:#f0fdf4;border-color:#86efac;"></div>
            <div style="font-size:0.75rem;color:#6d8ab0;margin-top:8px;">
                <i class="fas fa-circle-info"></i> Ringkasan di atas telah disimpan ke database dan dapat dilihat di halaman <a href="report.php" style="color:#2463eb;">Report</a>.
            </div>
        </div>

        <!-- HASIL TRANSKRIPSI CARD -->
        <div class="setup-card" id="hasilCard">
            <div class="section-label">
                <i class="fas fa-file-lines"></i> Hasil Transkripsi
            </div>
            <div class="hasil-text-box" id="hasilTextBox"></div>
            <div class="hasil-meta">
                <div class="hasil-filename">
                    <i class="fas fa-file-alt"></i>
                    <span id="hasilFileName">-</span>
                </div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <span id="hasilCharCount" style="font-size:0.78rem; color:#6d8ab0;"></span>
                    <a id="btnDownloadTxt" href="#" class="btn-download-txt" download>
                        <i class="fas fa-download"></i> Unduh .txt
                    </a>
                </div>
            </div>
        </div>

        <!-- ACTION FOOTER -->
        <div class="action-footer">
            <a href="notulensi.php" class="btn btn-outline"><i class="fas fa-arrow-left"></i> Kembali ke Live</a>
            <button class="btn btn-outline" id="resetUploadBtn" onclick="resetUpload()">
                <i class="fas fa-redo"></i> Upload Baru
            </button>
            <button class="btn btn-primary" id="uploadBtn" style="background: #1f4faf;" disabled>
                <i class="fas fa-cloud-arrow-up"></i> Upload &amp; Transkripsi
            </button>
        </div>
    </main>

    <script src="assets/js/realtime-clock.js"></script>
    <script>
        // ── Elemen ──────────────────────────────────────────
        const inputFile     = document.getElementById('inputVideoFile');
        const dropzone      = document.getElementById('uploadDropzone');
        const dropzoneLabel = document.getElementById('dropzoneLabel');
        const previewCard   = document.getElementById('filePreviewCard');
        const fileNameEl    = document.getElementById('fileName');
        const fileSizeEl    = document.getElementById('fileSize');
        const removeBtn     = document.getElementById('removeFileBtn');
        const uploadBtn     = document.getElementById('uploadBtn');
        const progressWrap  = document.getElementById('progressWrap');
        const progressBar   = document.getElementById('progressBar');
        const progressLabel = document.getElementById('progressLabel');
        const progressStatus= document.getElementById('progressStatus');
        const errorBox      = document.getElementById('errorBox');
        const errorMessage  = document.getElementById('errorMessage');
        const hasilCard     = document.getElementById('hasilCard');
        const hasilTextBox  = document.getElementById('hasilTextBox');
        const hasilFileName = document.getElementById('hasilFileName');
        const hasilCharCount= document.getElementById('hasilCharCount');
        const btnDownloadTxt= document.getElementById('btnDownloadTxt');
        const resetBtn      = document.getElementById('resetUploadBtn');
        const ringkasanCard = document.getElementById('ringkasanCard');
        const ringkasanBox  = document.getElementById('ringkasanTextBox');
        const inputJudul    = document.getElementById('inputJudulRapat');

        let selectedFile = null;

        // ── Format bytes ────────────────────────────────────
        function formatBytes(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // ── Tampilkan preview file ───────────────────────────
        function showFilePreview(file) {
            selectedFile = file;
            fileNameEl.textContent = file.name;
            fileSizeEl.textContent = formatBytes(file.size);
            previewCard.style.display = 'block';
            uploadBtn.disabled = false;
            hasilCard.style.display = 'none';
            errorBox.style.display = 'none';
            resetBtn.style.display = 'none';
        }

        // ── Hapus file ───────────────────────────────────────
        function clearFile() {
            inputFile.value = '';
            selectedFile = null;
            previewCard.style.display   = 'none';
            uploadBtn.disabled          = true;
            progressWrap.style.display  = 'none';
            hasilCard.style.display     = 'none';
            ringkasanCard.style.display = 'none';
            errorBox.style.display      = 'none';
            resetBtn.style.display      = 'none';
        }

        // ── Reset untuk upload baru ──────────────────────────
        function resetUpload() {
            clearFile();
            hasilCard.style.display     = 'none';
            ringkasanCard.style.display = 'none';
            if (inputJudul) inputJudul.value = '';
        }

        // ── File input change ────────────────────────────────
        inputFile.addEventListener('change', function () {
            if (this.files.length > 0) showFilePreview(this.files[0]);
        });

        removeBtn.addEventListener('click', clearFile);

        // ── Drag & drop ──────────────────────────────────────
        ['dragenter', 'dragover'].forEach(evt => {
            dropzone.addEventListener(evt, (e) => {
                e.preventDefault();
                dropzone.classList.add('dragover');
            });
        });
        ['dragleave', 'drop'].forEach(evt => {
            dropzone.addEventListener(evt, (e) => {
                e.preventDefault();
                dropzone.classList.remove('dragover');
            });
        });
        dropzone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) showFilePreview(files[0]);
        });

        // ── Animasi progress palsu (tidak bisa ukur waktu Python) ──
        let _progressInterval = null;
        function startFakeProgress() {
            let pct = 0;
            progressBar.style.width = '0%';
            _progressInterval = setInterval(() => {
                // Naik cepat ke 30%, kemudian lambat sampai 90%
                if (pct < 30)      pct += 3;
                else if (pct < 70) pct += 0.8;
                else if (pct < 90) pct += 0.2;
                progressBar.style.width = pct + '%';
            }, 600);
        }
        function stopFakeProgress(success) {
            clearInterval(_progressInterval);
            progressBar.style.width = success ? '100%' : '0%';
        }

        // ── Tombol Upload & Transkripsi ──────────────────────
        // ── URL Flask API ──────────────────────────────────────
        const FLASK_API = 'http://localhost:5000';

        uploadBtn.addEventListener('click', function () {
            if (!selectedFile) return;

            // UI: tampilkan progress, nonaktifkan tombol
            uploadBtn.disabled       = true;
            removeBtn.disabled       = true;
            dropzoneLabel.style.pointerEvents = 'none';
            progressWrap.style.display = 'block';
            errorBox.style.display     = 'none';
            hasilCard.style.display    = 'none';

            progressLabel.textContent  = 'Mengunggah file ke Server...';
            progressStatus.textContent = 'Menyiapkan antrian background task...';
            startFakeProgress();

            const formData = new FormData();
            formData.append('video_file', selectedFile);
            // Sertakan judul rapat
            if (inputJudul && inputJudul.value.trim()) {
                formData.append('judul_rapat', inputJudul.value.trim());
            }

            fetch(`${FLASK_API}/transcribe`, {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                stopFakeProgress(data.status === 'success');

                if (data.status === 'success') {
                    progressLabel.textContent  = '✓ File terkirim! Proses berjalan di background.';
                    progressBar.style.animation = 'none';
                    progressBar.style.opacity   = '1';

                    // OPSI A: Auto-Reload ke diri sendiri agar card Active Processes muncul!
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);

                } else {
                    // Error
                    stopFakeProgress(false);
                    errorBox.style.display = 'block';
                    errorMessage.textContent = data.message || 'Transkripsi gagal.';
                    uploadBtn.disabled = false;
                    removeBtn.disabled = false;
                    dropzoneLabel.style.pointerEvents = '';
                }
            })
            .catch(err => {
                stopFakeProgress(false);
                errorBox.style.display = 'block';
                errorMessage.textContent = 'Koneksi gagal: ' + err.message;
                uploadBtn.disabled = false;
                removeBtn.disabled = false;
                dropzoneLabel.style.pointerEvents = '';
            });
        });

        // ── Auto-Refresh for Processing Cards ─────────
        function checkProcessingSummaries() {
            const elements = document.querySelectorAll('.active-job-item');
            if (elements.length === 0) return;

            elements.forEach(el => {
                const dbId = el.getAttribute('data-processing-id');
                const statusText = el.querySelector('.job-status-text');

                fetch(`${FLASK_API}/api/check_summary/${dbId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success' && !data.is_processing) {
                            // Selesai diproses sepenuhnya!
                            statusText.innerHTML = '<i class="fas fa-check-circle" style="color:#059669;"></i> Selesai! Klik Lihat Report.';
                            statusText.style.color = '#059669';
                            el.style.backgroundColor = '#ecfdf5';
                            el.style.borderColor = '#6ee7b7';

                            // ── Tampilkan debug ranking LexRank ──
                            if (Array.isArray(data.lexrank_debug) && data.lexrank_debug.length > 0) {
                                renderUploadLexrankDebug(data.lexrank_debug, dbId);
                            }
                        } else if (data.status === 'success' && data.is_processing) {
                            const currentText = statusText.textContent.trim();
                            if (data.ringkasan === '[PROSES_SUMMARIZE]' && currentText.includes('Mentranskripsi')) {
                                statusText.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Meringkas (LexRank & Ollama)...';
                            }
                        }
                    })
                    .catch(e => console.log(e));
            });
        }
        setInterval(checkProcessingSummaries, 5000);

        // ── Render LexRank Debug Panel (Upload) ────────
        function renderUploadLexrankDebug(ranked, dbId) {
            // Cek apakah panel untuk job ini sudah ada
            if (document.getElementById('lexrankDebugPanel_' + dbId)) return;

            const panel = document.createElement('div');
            panel.id = 'lexrankDebugPanel_' + dbId;
            panel.style.cssText = 'margin-top:16px;';
            panel.innerHTML = `
                <div style="background:#1e1e2e;border-radius:16px;overflow:hidden;border:1px solid #313145;">
                    <div style="display:flex;align-items:center;justify-content:space-between;
                                padding:12px 18px;background:#252538;border-bottom:1px solid #313145;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <span style="width:8px;height:8px;border-radius:50%;background:#22d3ee;
                                         display:inline-block;box-shadow:0 0 6px #22d3ee;"></span>
                            <span style="font-family:'Courier New',monospace;font-size:0.78rem;
                                         color:#94a3b8;font-weight:600;letter-spacing:.05em;">
                                DEBUG · LexRank Sentence Ranking
                            </span>
                        </div>
                        <span style="font-size:0.7rem;color:#475569;font-family:monospace;">
                            ${ranked.length} kalimat
                        </span>
                    </div>
                    <div id="lexrankList_${dbId}"
                         style="max-height:260px;overflow-y:auto;padding:10px 0;
                                font-family:'Courier New',monospace;font-size:0.75rem;">
                    </div>
                </div>
            `;

            // Masukkan panel setelah activeProcessList
            const container = document.getElementById('activeProcessList');
            if (container) container.appendChild(panel);

            const list = document.getElementById('lexrankList_' + dbId);
            if (!list) return;

            ranked.forEach(item => {
                const scoreBar = Math.round((item.score || 0) * 100);
                const isTop3   = item.rank <= 3;
                const rankColor = item.rank === 1 ? '#fbbf24'
                                : item.rank === 2 ? '#94a3b8'
                                : item.rank === 3 ? '#cd7c3a'
                                : '#475569';

                const row = document.createElement('div');
                row.style.cssText = `
                    display:flex;align-items:flex-start;gap:10px;
                    padding:7px 16px;border-bottom:1px solid #252538;
                    ${isTop3 ? 'background:rgba(34,211,238,0.04);' : ''}
                `;
                row.innerHTML = `
                    <span style="min-width:28px;text-align:right;font-weight:700;
                                 color:${rankColor};font-size:0.8rem;margin-top:1px;">
                        ${item.rank}.
                    </span>
                    <div style="flex:1;min-width:0;">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                            <div style="flex:1;height:4px;background:#2a2a3e;border-radius:2px;overflow:hidden;">
                                <div style="height:100%;width:${scoreBar}%;
                                            background:${isTop3 ? '#22d3ee' : '#334155'};
                                            border-radius:2px;"></div>
                            </div>
                            <span style="font-size:0.68rem;color:${isTop3 ? '#22d3ee' : '#475569'};
                                         min-width:38px;text-align:right;">
                                ${(item.score || 0).toFixed(4)}
                            </span>
                        </div>
                        <div style="color:${isTop3 ? '#e2e8f0' : '#64748b'};
                                    font-size:0.72rem;line-height:1.5;word-break:break-word;
                                    white-space:normal;font-family:'Inter',sans-serif;">
                            ${item.sentence ? item.sentence.replace(/</g,'&lt;').replace(/>/g,'&gt;') : ''}
                        </div>
                    </div>
                `;
                list.appendChild(row);
            });
        }
    </script>
</body>

</html>
