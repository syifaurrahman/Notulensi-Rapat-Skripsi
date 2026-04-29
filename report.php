<?php
require_once 'cek_login.php';

// ── Konfigurasi DB ────────
define('DB_HOST', 'localhost');
define('DB_USER_DB', 'root');
define('DB_PASS_DB', '');
define('DB_NAME_DB', 'notulensi');

$conn = @mysqli_connect(DB_HOST, DB_USER_DB, DB_PASS_DB, DB_NAME_DB);

// Statistik
$total_docs = 0;
$total_live = 0;
$total_upload = 0;
$query_hasil = null;

if ($conn) {
    try {
        // Hitung statistik
        $res = mysqli_query($conn, "SELECT tipe_transkripsi, COUNT(*) as jml FROM notulensi_hasil GROUP BY tipe_transkripsi");
        if ($res) {
            while ($r = mysqli_fetch_assoc($res)) {
                $total_docs += $r['jml'];
                if ($r['tipe_transkripsi'] === 'Live')   $total_live   = $r['jml'];
                if ($r['tipe_transkripsi'] === 'Upload') $total_upload = $r['jml'];
            }
        }
        // Ambil semua data
        $query_hasil = mysqli_query($conn, "SELECT * FROM notulensi_hasil ORDER BY created_at DESC");
    } catch (mysqli_sql_exception $e) {
        $query_hasil = false;
    }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.5, user-scalable=yes">
    <title>Notulensi Rapat · Laporan Hasil Rapat</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/report.css">
    <!-- jsPDF untuk export PDF -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <style>
        /* ── Ringkasan Preview ─────────────────────────── */
        .ringkasan-preview {
            font-size: 0.8rem;
            color: #475569;
            line-height: 1.6;
            margin-top: 6px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .btn-detail {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #2463eb;
            background: #eef3ff;
            border: none;
            border-radius: 7px;
            padding: 5px 12px;
            cursor: pointer;
            transition: background 0.2s;
            white-space: nowrap;
        }
        .btn-detail:hover { background: #dbeafe; }
        .btn-detail:disabled, .btn-detail.disabled {
            background: #f1f5f9;
            color: #94a3b8;
            cursor: not-allowed;
        }

        /* ── Loading Spinner ───────────────────────────── */
        .spinner {
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid rgba(36, 99, 235, 0.3);
            border-radius: 50%;
            border-top-color: #2463eb;
            animation: spin 1s ease-in-out infinite;
            margin-right: 5px;
            vertical-align: middle;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .processing-text {
            color: #2463eb;
            font-size: 0.8rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            margin-top: 6px;
        }

        /* ── Modal ─────────────────────────────────────── */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(4px);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .modal-overlay.active { display: flex; }
        .modal-box {
            background: #fff;
            border-radius: 16px;
            width: 100%;
            max-width: 680px;
            max-height: 85vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 60px rgba(0,0,0,0.25);
            animation: modalIn 0.2s ease;
        }
        @keyframes modalIn {
            from { opacity:0; transform: scale(0.95) translateY(10px); }
            to   { opacity:1; transform: scale(1)    translateY(0); }
        }
        .modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 24px 16px;
            border-bottom: 1px solid #e2e8f0;
        }
        .modal-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
        }
        .modal-close {
            background: none;
            border: none;
            font-size: 1.2rem;
            color: #64748b;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            transition: background 0.2s;
        }
        .modal-close:hover { background: #f1f5f9; }
        .modal-body {
            padding: 20px 24px;
            overflow-y: auto;
            flex: 1;
        }
        .modal-section-label {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #2463eb;
            margin-bottom: 8px;
        }
        .modal-text {
            font-size: 0.88rem;
            line-height: 1.8;
            color: #334155;
            white-space: pre-wrap;
            word-break: break-word;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px 16px;
            max-height: 400px;
            overflow-y: auto;
        }
        .modal-text.summary-box {
            background: #f0fdf4;
            border-color: #86efac;
        }
        .modal-text.summary-box .section-title {
            font-weight: 700;
            font-size: 0.82rem;
            color: #059669;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 16px 0 6px 0;
            padding-bottom: 4px;
            border-bottom: 1px solid #d1fae5;
        }
        .modal-text.summary-box .section-title:first-child {
            margin-top: 0;
        }
        .modal-text.summary-box ul {
            margin: 4px 0 8px 0;
            padding-left: 18px;
        }
        .modal-text.summary-box ul li {
            margin-bottom: 3px;
            line-height: 1.7;
        }
        .modal-text.summary-box p {
            margin: 4px 0 8px 0;
            line-height: 1.7;
        }
        .modal-meta {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 12px;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }
        .modal-dl-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #2463eb;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: background 0.2s;
            margin-top: 14px;
        }
        .modal-dl-btn:hover { background: #1f4faf; }
        .modal-dl-btn.pdf-btn {
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        }
        .modal-dl-btn.pdf-btn:hover { background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%); }

        /* ── Filter Bar ────────────────────────────────── */
        .filter-bar {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 6px 14px;
            border-radius: 8px;
            border: 1.5px solid #dde5f5;
            background: #fff;
            font-size: 0.8rem;
            font-weight: 600;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s;
        }
        .filter-btn.active, .filter-btn:hover {
            background: #2463eb;
            color: #fff;
            border-color: #2463eb;
        }
    </style>
</head>

<body>

    <?php include 'sidebar.php'; ?>

    <!-- Modal Detail -->
    <div class="modal-overlay" id="detailModal">
        <div class="modal-box">
            <div class="modal-header">
                <div class="modal-title" id="modalJudul">Detail Rapat</div>
                <button class="modal-close" onclick="closeModal()"><i class="fas fa-xmark"></i></button>
            </div>
            <div class="modal-body">
                <!-- Ringkasan -->
                <div id="modalRingkasanWrap">
                    <div class="modal-section-label"><i class="fas fa-list-check"></i> Hasil Summarize</div>
                    <div class="modal-text summary-box" id="modalRingkasan">-</div>
                </div>

                <!-- Meta -->
                <div class="modal-meta" id="modalMeta"></div>

                <!-- Download -->
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button class="modal-dl-btn pdf-btn" id="modalDownloadPdfBtn" onclick="downloadSummaryPDF()">
                        <i class="fas fa-file-pdf"></i> Unduh Notulensi (.pdf)
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- MAIN CONTENT -->
    <main class="main-content">
        <!-- top bar -->
        <div class="top-bar">
            <div class="page-title">
                <h1>Report</h1>
                <div class="breadcrumb"><i class="fas fa-home"></i> Dashboard / Report / Hasil Rapat</div>
            </div>
            <div class="header-date">
                <i class="fas fa-file-pdf"></i>
                <span id="realtime-clock"></span>
            </div>
        </div>

        <!-- KPI Cards -->
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Total Dokumen</span>
                    <span class="kpi-number"><?= $total_docs ?></span>
                </div>
                <div class="kpi-icon" style="color:#2463eb;"><i class="fas fa-folder-open"></i></div>
            </div>
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Live Transkripsi</span>
                    <span class="kpi-number"><?= $total_live ?></span>
                </div>
                <div class="kpi-icon" style="color:#2463eb;"><i class="fas fa-microphone"></i></div>
            </div>
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Upload Transkripsi</span>
                    <span class="kpi-number"><?= $total_upload ?></span>
                </div>
                <div class="kpi-icon" style="color:#059669;"><i class="fas fa-film"></i></div>
            </div>
        </div>

        <!-- Header + Filter -->
        <div class="report-header">
            <h2><i class="fas fa-file-lines" style="color:#2463eb; margin-right: 8px;"></i> Hasil Rapat</h2>
        </div>
        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterTable('all', this)">Semua</button>
            <button class="filter-btn" onclick="filterTable('Live', this)"><i class="fas fa-microphone"></i> Live</button>
            <button class="filter-btn" onclick="filterTable('Upload', this)"><i class="fas fa-film"></i> Upload</button>
        </div>

        <!-- Tabel -->
        <div class="report-table">
            <div class="table-row header">
                <div class="table-cell">Judul Rapat</div>
                <div class="table-cell">Waktu</div>
                <div class="table-cell">Tipe</div>
                <div class="table-cell">Aksi</div>
            </div>

            <?php if ($query_hasil === false): ?>
                <div style="padding: 40px; text-align: center; color: #dc2626; border: 2px dashed #fca5a5; border-radius: 12px; margin: 20px;">
                    <i class="fas fa-exclamation-triangle fa-3x" style="margin-bottom: 12px;"></i><br>
                    <strong>Tabel Database Belum Dibuat!</strong><br><br>
                    Silakan jalankan file <b>migrate.php</b> terlebih dahulu.<br><br>
                    <a href="migrate.php" class="btn btn-primary" style="margin-top: 15px; display: inline-block;">Jalankan Migrasi Sekarang</a>
                </div>
            <?php elseif ($query_hasil && $total_docs > 0): ?>
                <?php while ($row = mysqli_fetch_assoc($query_hasil)): ?>
                    <?php
                        $time       = strtotime($row['waktu_rapat']);
                        $isLive     = $row['tipe_transkripsi'] === 'Live';
                        $colorStyle = $isLive ? 'color:#2463eb;background:#eef3ff;' : 'color:#059669;background:#ecfdf5;';
                        $iconClass  = $isLive ? 'fas fa-microphone' : 'fas fa-film';
                        $judul      = !empty($row['judul_rapat']) ? htmlspecialchars($row['judul_rapat']) : 'Tanpa Judul';
                        $ringkasan  = !empty($row['ringkasan'])   ? htmlspecialchars($row['ringkasan'])   : '';
                        $txtFile    = !empty($row['transkrip_txt']) ? htmlspecialchars($row['transkrip_txt']) : '';
                        $isProcessingSum = ($ringkasan === '[PROSES_SUMMARIZE]');
                        $isProcessingTxt = ($ringkasan === '[PROSES_TRANSKRIPSI]');
                        $isProcessing = ($isProcessingSum || $isProcessingTxt);

                        // Mencegah error / json-safe untuk modal
                        $modalTxt = 'Sedang memproses...';
                        if (!$isProcessing) $modalTxt = $ringkasan ?: 'Ringkasan tidak tersedia.';
                        $modalRingkasan = htmlspecialchars(json_encode($modalTxt), ENT_QUOTES, "UTF-8");
                        $modalJudul     = htmlspecialchars(json_encode($judul), ENT_QUOTES, "UTF-8");
                        $modalTxtFile   = htmlspecialchars(json_encode($txtFile), ENT_QUOTES, "UTF-8");
                        $modalWaktu     = htmlspecialchars(json_encode(date('j F Y, H:i', $time)), ENT_QUOTES, "UTF-8");
                        $modalTipe      = htmlspecialchars(json_encode($row['tipe_transkripsi']), ENT_QUOTES, "UTF-8");
                    ?>
                    <div class="table-row" data-tipe="<?= $row['tipe_transkripsi'] ?>" data-id="<?= $row['id'] ?>">
                        <div class="table-cell" data-label="Judul Rapat">
                            <span class="judul"><?= $judul ?></span>
                            <?php if ($isProcessing): ?>
                                <div class="processing-text" data-processing-id="<?= $row['id'] ?>">
                                    <div class="spinner"></div> 
                                    <span class="proc-label"><?php echo $isProcessingTxt ? 'Mentranskripsi Audio...' : 'Meringkas (LexRank & Ollama)...'; ?></span>
                                    <strong class="proc-pct" style="margin-left: 8px; color: #2463eb;">0%</strong>
                                </div>
                            <?php endif; ?>
                        </div>
                        <div class="table-cell" data-label="Waktu"><?= date('j F Y', $time) ?></div>
                        <div class="table-cell" data-label="Tipe">
                            <span style="<?= $colorStyle ?> padding:5px 10px;border-radius:6px;font-size:0.8rem;font-weight:500;">
                                <i class="<?= $iconClass ?>" style="margin-right:4px;"></i> <?= $row['tipe_transkripsi'] ?>
                            </span>
                        </div>
                        <div class="table-cell" data-label="Aksi">
                            <?php if ($isProcessing): ?>
                                <button class="btn-detail disabled" disabled title="Tunggu ringkasan selesai" data-processing-btn="<?= $row['id'] ?>">
                                    <div class="spinner"></div> <span class="btn-pct">Proses 0%</span>
                                </button>
                            <?php else: ?>
                                <button class="btn-detail"
                                    onclick="openModal(<?= $modalJudul ?>, <?= $modalRingkasan ?>, <?= $modalTxtFile ?>, <?= $modalWaktu ?>, <?= $modalTipe ?>)">
                                    <i class="fas fa-eye"></i> Detail
                                </button>
                            <?php endif; ?>
                        </div>
                    </div>
                <?php endwhile; ?>
            <?php else: ?>
                <div style="padding: 50px; text-align: center; color: #64748b;">
                    <i class="fas fa-folder-open fa-3x" style="margin-bottom:12px;opacity:0.4;"></i><br>
                    Belum ada hasil rapat yang tersimpan.<br>
                    <a href="notulensi_upload.php" style="color:#2463eb;font-weight:600;margin-top:10px;display:inline-block;">
                        <i class="fas fa-cloud-arrow-up"></i> Upload Video Rapat
                    </a>
                </div>
            <?php endif; ?>
        </div>

        <!-- Footer -->
        <div class="extra-footer">
            <span><i class="far fa-file-lines"></i> <?= $total_docs ?> dokumen tersedia</span>
        </div>
    </main>

    <script src="assets/js/realtime-clock.js"></script>
    <script>
        const FLASK_API = 'http://localhost:5000';

        // ── State untuk PDF export ────────────────────────
        let _modalState = { judul: '', ringkasan: '', waktu: '', tipe: '', txtFile: '' };

        // ── Modal ────────────────────────────────────────
        function openModal(judul, ringkasan, txtFile, waktu, tipe) {
            // Simpan state mentah untuk PDF
            _modalState = { judul, ringkasan, waktu, tipe, txtFile };

            document.getElementById('modalJudul').textContent  = judul;
            document.getElementById('modalRingkasan').innerHTML = formatRingkasan(ringkasan);

            const meta = document.getElementById('modalMeta');
            meta.innerHTML = `
                <span><i class="fas fa-clock"></i> ${waktu}</span>
                <span><i class="fas fa-tag"></i> ${tipe}</span>
                ${txtFile ? `<span><i class="fas fa-file-alt"></i> ${txtFile}</span>` : ''}
            `;

            // Tombol PDF selalu tampil
            const pdfBtn = document.getElementById('modalDownloadPdfBtn');
            if (pdfBtn) pdfBtn.style.display = 'inline-flex';

            document.getElementById('detailModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            document.getElementById('detailModal').classList.remove('active');
            document.body.style.overflow = '';
        }

        // Tutup modal klik overlay
        document.getElementById('detailModal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        // Tutup modal Esc
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

        // ── Format Ringkasan menjadi HTML bersih ─────────
        function formatRingkasan(text) {
            if (!text) return '<em style="color:#94a3b8;">Ringkasan tidak tersedia.</em>';

            // Strip remaining markdown bold/italic
            text = text.replace(/\*\*(.+?)\*\*/g, '$1');
            text = text.replace(/__(.+?)__/g, '$1');
            text = text.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '$1');
            text = text.replace(/#{1,6}\s*/gm, '');
            text = text.replace(/`([^`]+)`/g, '$1');

            const lines = text.split('\n');
            let html = '';
            let inList = false;

            for (let i = 0; i < lines.length; i++) {
                const line = lines[i].trim();

                // Baris kosong — tutup list jika ada, tambah spasi
                if (!line) {
                    if (inList) { html += '</ul>'; inList = false; }
                    continue;
                }

                // Deteksi judul bagian: baris ALL CAPS (min 3 char, tanpa bullet)
                if (/^[A-Z\s\/\-&()]{3,}$/.test(line) && !line.startsWith('-')) {
                    if (inList) { html += '</ul>'; inList = false; }
                    // Title case the section header
                    const titleText = line.replace(/\b\w+/g, w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
                    html += `<div class="section-title">${titleText}</div>`;
                    continue;
                }

                // Deteksi bullet point (- item atau * item)
                const bulletMatch = line.match(/^[-•*]\s+(.+)/);
                if (bulletMatch) {
                    if (!inList) { html += '<ul>'; inList = true; }
                    html += `<li>${bulletMatch[1]}</li>`;
                    continue;
                }

                // Deteksi numbered list (1. item)
                const numMatch = line.match(/^\d+[\.)]\s+(.+)/);
                if (numMatch) {
                    if (!inList) { html += '<ul>'; inList = true; }
                    html += `<li>${numMatch[1]}</li>`;
                    continue;
                }

                // Paragraf biasa
                if (inList) { html += '</ul>'; inList = false; }
                html += `<p>${line}</p>`;
            }

            if (inList) html += '</ul>';
            return html || `<p>${text}</p>`;
        }

        // ── Filter tabel ─────────────────────────────────
        function filterTable(tipe, btn) {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.table-row:not(.header)').forEach(row => {
                if (tipe === 'all' || row.dataset.tipe === tipe) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        // ── Auto-Refresh for Processing Summaries & Transcriptions ─────────
        function checkProcessingSummaries() {
            const processingElements = document.querySelectorAll('[data-processing-id]');
            if (processingElements.length === 0) return;

            processingElements.forEach(el => {
                const dbId = el.getAttribute('data-processing-id');
                fetch(`${FLASK_API}/api/check_summary/${dbId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success' && !data.is_processing) {
                            // Selesai diproses sepenuhnya! 
                            console.log(`ID ${dbId} selesai. Reloading...`);
                            window.location.reload();
                        } else if (data.status === 'success' && data.is_processing) {
                            // Coba update text agar user tau kalo udah pindah phase dari transkripsi -> summarize
                            const labelEl = el.querySelector('.proc-label');
                            if (labelEl && data.ringkasan === '[PROSES_SUMMARIZE]' && labelEl.textContent.includes('Mentranskripsi')) {
                                labelEl.textContent = 'Meringkas (LexRank & Ollama)...';
                                // Jump pct
                                if (progressMap[dbId] && progressMap[dbId] < 70) progressMap[dbId] = 70;
                            }
                        }
                    })
                    .catch(err => console.error('Error checking summary:', err));
            });
        }

        // ── Animasi Persentase Progress ─────────
        const progressMap = {};
        function updateFakePercentage() {
            document.querySelectorAll('[data-processing-id]').forEach(el => {
                const id = el.getAttribute('data-processing-id');
                const labelEl = el.querySelector('.proc-label');
                if (!labelEl) return;
                
                const labelText = labelEl.textContent;
                if (!progressMap[id]) progressMap[id] = 0;
                
                let limit = 70; // Fase Transkripsi -> max 70%
                if (labelText.includes('Meringkas')) limit = 99; // Fase Summarize -> max 99%

                if (progressMap[id] < limit) {
                    // Penambahan acak perlahan agar tampak responsif
                    progressMap[id] += Math.random() * 2;
                    if (progressMap[id] > limit) progressMap[id] = limit;
                }

                const displayPct = Math.floor(progressMap[id]) + '%';
                
                const pctEl = el.querySelector('.proc-pct');
                if (pctEl) pctEl.innerHTML = displayPct;

                const btnEl = document.querySelector(`[data-processing-btn="${id}"] .btn-pct`);
                if (btnEl) btnEl.innerHTML = 'Proses ' + displayPct;
            });
        }
        setInterval(updateFakePercentage, 800);

        // ── Generate & Download PDF Notulensi ────────────
        function downloadSummaryPDF() {
            try {
                if (typeof jspdf === 'undefined' && typeof window.jspdf === 'undefined') {
                    alert('Library jsPDF belum dimuat. Coba refresh halaman.');
                    return;
                }

                const { jsPDF } = window.jspdf;
                const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

                const { judul, ringkasan, waktu, tipe, txtFile } = _modalState;
                
                // Debug log
                console.log("Generating PDF for:", judul);

                const pageW   = doc.internal.pageSize.getWidth();
                const pageH   = doc.internal.pageSize.getHeight();
                const margin  = 20;
                const contentW = pageW - margin * 2;
                let y = 0;

                // ── Fungsi helper ─────────────────────────────
                function addPage() {
                    doc.addPage();
                    y = margin;
                    drawPageFooter();
                }

                function checkY(needed) {
                    if (y + needed > pageH - 20) addPage();
                }

                function drawPageFooter() {
                    const pg = doc.internal.getCurrentPageInfo().pageNumber;
                    doc.setFont('helvetica', 'normal');
                    doc.setFontSize(8);
                    doc.setTextColor(160, 160, 160);
                    doc.text('Sistem Notulensi Rapat — Dokumen Otomatis', margin, pageH - 10);
                    doc.text(`Halaman ${pg}`, pageW - margin, pageH - 10, { align: 'right' });
                    // Garis footer
                    doc.setDrawColor(220, 220, 220);
                    doc.line(margin, pageH - 14, pageW - margin, pageH - 14);
                }

                // ══ HEADER HALAMAN PERTAMA ══════════════════════
                // Background header biru
                doc.setFillColor(36, 99, 235);
                doc.rect(0, 0, pageW, 38, 'F');

                // Nama Sistem
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(13);
                doc.setTextColor(255, 255, 255);
                doc.text('SISTEM NOTULENSI RAPAT', margin, 14);

                // Sub-judul sistem
                doc.setFont('helvetica', 'normal');
                doc.setFontSize(8);
                doc.setTextColor(180, 210, 255);
                doc.text('Dokumen Ringkasan Rapat — Dihasilkan Otomatis oleh AI', margin, 21);

                // Tanggal cetak di kanan
                const now = new Date();
                const tglCetak = now.toLocaleDateString('id-ID', { day:'numeric', month:'long', year:'numeric' })
                               + '  ' + now.toLocaleTimeString('id-ID', { hour:'2-digit', minute:'2-digit' });
                doc.setFontSize(8);
                doc.setTextColor(200, 225, 255);
                doc.text(tglCetak, pageW - margin, 14, { align: 'right' });

                // Garis bawah header
                doc.setDrawColor(36, 99, 235);
                doc.setLineWidth(0.5);
                doc.line(0, 38, pageW, 38);

                y = 48;

                // ══ JUDUL RAPAT ══════════════════════════════════
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(16);
                doc.setTextColor(15, 23, 42);
                const judulLines = doc.splitTextToSize(judul || 'Tanpa Judul', contentW);
                checkY(judulLines.length * 8 + 4);
                doc.text(judulLines, margin, y);
                y += judulLines.length * 8 + 2;

                // Garis bawah judul
                doc.setDrawColor(36, 99, 235);
                doc.setLineWidth(1);
                doc.line(margin, y, margin + 40, y);
                doc.setLineWidth(0.2);
                doc.setDrawColor(220, 220, 220);
                doc.line(margin + 42, y, pageW - margin, y);
                y += 8;

                // ══ METADATA ═════════════════════════════════════
                // Box metadata dengan background abu muda
                const metaBoxH = 24;
                doc.setFillColor(248, 250, 252);
                doc.setDrawColor(226, 232, 240);
                doc.roundedRect(margin, y, contentW, metaBoxH, 3, 3, 'FD');

                doc.setFont('helvetica', 'normal');
                doc.setFontSize(8.5);
                doc.setTextColor(100, 116, 139);

                const metaY1 = y + 8;
                const metaY2 = y + 18;
                const col2   = margin + contentW / 2;

                // Baris 1: Waktu & Tipe
                doc.setFont('helvetica', 'bold');
                doc.text('Waktu Rapat', margin + 6, metaY1);
                doc.setFont('helvetica', 'normal');
                doc.setTextColor(30, 41, 59);
                doc.text(waktu || '-', margin + 32, metaY1);

                doc.setFont('helvetica', 'bold');
                doc.setTextColor(100, 116, 139);
                doc.text('Tipe', col2 + 2, metaY1);
                doc.setFont('helvetica', 'normal');
                doc.setTextColor(30, 41, 59);
                doc.text(tipe || '-', col2 + 16, metaY1);

                // Baris 2: Sumber file
                doc.setFont('helvetica', 'bold');
                doc.setTextColor(100, 116, 139);
                doc.text('Sumber', margin + 6, metaY2);
                doc.setFont('helvetica', 'normal');
                doc.setTextColor(30, 41, 59);
                const srcText = txtFile || 'Live Transcription';
                const srcLines = doc.splitTextToSize(srcText, contentW - 30);
                doc.text(srcLines[0], margin + 26, metaY2);

                y += metaBoxH + 10;

                // ══ LABEL RINGKASAN ═══════════════════════════════
                checkY(14);
                doc.setFillColor(36, 99, 235);
                doc.setDrawColor(36, 99, 235);
                doc.rect(margin, y, 3, 8, 'F');
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(10);
                doc.setTextColor(36, 99, 235);
                doc.text('HASIL RINGKASAN (SUMMARIZE)', margin + 6, y + 6);
                y += 14;

                // ══ ISI RINGKASAN ══════════════════════════════════
                const rawText = ringkasan || 'Ringkasan tidak tersedia.';
                const lines = rawText.split('\n');

                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i].trim();

                    if (!line) { y += 3; continue; }

                    // Deteksi judul bagian (ALL CAPS, min 3 char)
                    if (/^[A-Z\s\/\-&()]{3,}$/.test(line) && !line.startsWith('-')) {
                        checkY(14);
                        // Background highlight untuk section title
                        doc.setFillColor(239, 246, 255);
                        doc.rect(margin, y - 4, contentW, 10, 'F');
                        doc.setFont('helvetica', 'bold');
                        doc.setFontSize(9.5);
                        doc.setTextColor(15, 60, 140);
                        doc.text(line, margin + 3, y + 3);
                        y += 12;
                        // Garis tipis bawah section
                        doc.setDrawColor(190, 215, 255);
                        doc.setLineWidth(0.3);
                        doc.line(margin, y - 2, pageW - margin, y - 2);
                        y += 2;
                        continue;
                    }

                    // Bullet list (- item)
                    const bulletMatch = line.match(/^[-•*]\s+(.+)/);
                    if (bulletMatch) {
                        const txt = bulletMatch[1];
                        const wrapped = doc.splitTextToSize(txt, contentW - 8);
                        checkY(wrapped.length * 5.5 + 2);
                        doc.setFont('helvetica', 'normal');
                        doc.setFontSize(9);
                        doc.setTextColor(51, 65, 85);
                        // Bullet dot
                        doc.setFillColor(36, 99, 235);
                        doc.circle(margin + 2.5, y + 0.5, 0.9, 'F');
                        doc.text(wrapped, margin + 6, y + 1.5);
                        y += wrapped.length * 5.5 + 1.5;
                        continue;
                    }

                    // Numbered list (1. item)
                    const numMatch = line.match(/^(\d+)[.)\s]+(.+)/);
                    if (numMatch) {
                        const numStr = numMatch[1] + '.';
                        const txt    = numMatch[2];
                        const wrapped = doc.splitTextToSize(txt, contentW - 10);
                        checkY(wrapped.length * 5.5 + 2);
                        doc.setFont('helvetica', 'bold');
                        doc.setFontSize(9);
                        doc.setTextColor(36, 99, 235);
                        doc.text(numStr, margin + 1, y + 1.5);
                        doc.setFont('helvetica', 'normal');
                        doc.setTextColor(51, 65, 85);
                        doc.text(wrapped, margin + 8, y + 1.5);
                        y += wrapped.length * 5.5 + 1.5;
                        continue;
                    }

                    // Paragraf biasa
                    const wrapped = doc.splitTextToSize(line, contentW);
                    checkY(wrapped.length * 5.5 + 2);
                    doc.setFont('helvetica', 'normal');
                    doc.setFontSize(9);
                    doc.setTextColor(51, 65, 85);
                    doc.text(wrapped, margin, y + 1.5);
                    y += wrapped.length * 5.5 + 3;
                }

                // ══ FOOTER ═══════════════════════════════════════
                drawPageFooter();

                // ══ SIMPAN PDF ════════════════════════════════════
                const safeJudul = (judul || 'notulensi').replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50);
                const fileName = `Notulensi_${safeJudul}.pdf`;
                console.log("Saving as:", fileName);

                // Gunakan Data URI agar nama file dipatuhi di Chrome maupun Edge
                const dataUri = doc.output('datauristring');
                const link = document.createElement('a');
                link.href = dataUri;
                link.download = fileName;
                link.style.display = 'none';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

            } catch (err) {
                console.error("PDF Generation Error:", err);
                alert("Gagal membuat PDF: " + err.message);
            }
        }

        // Cek setiap 5 detik ke server
        setInterval(checkProcessingSummaries, 5000);
    </script>
</body>

</html>