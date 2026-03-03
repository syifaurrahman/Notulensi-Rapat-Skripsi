<?php
require_once 'cek_login.php'; // Session sudah di-start di sini
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.5, user-scalable=yes">
    <title>Notulensi Rapat · Laporan Hasil Rapat</title>
    <!-- Font Awesome 6 (free) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Font: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/report.css">
</head>

<body>

    <?php include 'sidebar.php'; ?>

    <!-- MAIN CONTENT - SCROLLABLE (HALAMAN REPORT) -->
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

        <!-- KPI Cards (opsional, untuk konteks report) -->
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Dokumen PDF</span>
                    <span class="kpi-number">45</span>
                </div>
                <div class="kpi-badge">
                    <i class="fas fa-arrow-up"></i> +12 bulan ini
                </div>
            </div>
        </div>

        <!-- Header Report: Hasil Rapat + Searching -->
        <div class="report-header">
            <h2><i class="fas fa-file-lines" style="color:#2463eb; margin-right: 8px;"></i> Hasil Rapat</h2>
        </div>

        <!-- Tabel Hasil Rapat dengan Button PDF -->
        <div class="report-table">
            <!-- Header Tabel -->
            <div class="table-row header">
                <div class="table-cell">Judul Rapat</div>
                <div class="table-cell">Waktu</div>
                <div class="table-cell">Kesimpulan Rapat</div>
                <div class="table-cell"> </div>
            </div>

            <!-- Row 1: Rapat Tim Marketing -->
            <div class="table-row">
                <div class="table-cell" data-label="Judul Rapat">
                    <span class="judul">Rapat Tim Marketing</span>
                    <div class="sub-judul">Evaluasi Q1 2026</div>
                </div>
                <div class="table-cell" data-label="Waktu">5 Jan 2026 · 10:30</div>
                <div class="table-cell" data-label="Kesimpulan">Kesimpulan Rapat</div>
                <div class="table-cell" data-label=" ">
                    <button class="btn-pdf" onclick="alert('Download PDF: Rapat Tim Marketing - Evaluasi Q1 2026')">
                        <i class="fas fa-file-pdf"></i> PDF ↓
                    </button>
                </div>
            </div>

            <!-- Row 2: Evaluasi Proyek AI -->
            <div class="table-row">
                <div class="table-cell" data-label="Judul Rapat">
                    <span class="judul">Evaluasi Proyek AI</span>
                    <div class="sub-judul">Sprint Review</div>
                </div>
                <div class="table-cell" data-label="Waktu">5 Jan 2026 · 14:00</div>
                <div class="table-cell" data-label="Kesimpulan">Kesimpulan Rapat</div>
                <div class="table-cell" data-label=" ">
                    <button class="btn-pdf" onclick="alert('Download PDF: Evaluasi Proyek AI - Sprint Review')">
                        <i class="fas fa-file-pdf"></i> PDF ↓
                    </button>
                </div>
            </div>

            <!-- Row 3: Rapat Pengembangan Produk -->
            <div class="table-row">
                <div class="table-cell" data-label="Judul Rapat">
                    <span class="judul">Rapat Pengembangan Produk</span>
                    <div class="sub-judul">Fitur Baru</div>
                </div>
                <div class="table-cell" data-label="Waktu">4 Jan 2026 · 09:15</div>
                <div class="table-cell" data-label="Kesimpulan">Kesimpulan Rapat</div>
                <div class="table-cell" data-label=" ">
                    <button class="btn-pdf" onclick="alert('Download PDF: Rapat Pengembangan Produk - Fitur Baru')">
                        <i class="fas fa-file-pdf"></i> PDF ↓
                    </button>
                </div>
            </div>

            <!-- Row 4: Daily Standup -->
            <div class="table-row">
                <div class="table-cell" data-label="Judul Rapat">
                    <span class="judul">Daily Standup</span>
                    <div class="sub-judul">Tim Engineering</div>
                </div>
                <div class="table-cell" data-label="Waktu">3 Jan 2026 · 08:30</div>
                <div class="table-cell" data-label="Kesimpulan">Kesimpulan Rapat</div>
                <div class="table-cell" data-label=" ">
                    <button class="btn-pdf" onclick="alert('Download PDF: Daily Standup - Tim Engineering')">
                        <i class="fas fa-file-pdf"></i> PDF ↓
                    </button>
                </div>
            </div>
        </div>

        <!-- Pagination: | 1 | 2 | 3 | ... | 67 | 68 | -->
        <div class="pagination">
            <span class="pagination-item"><i class="fas fa-chevron-left"></i></span>
            <span class="pagination-item active">1</span>
            <span class="pagination-item">2</span>
            <span class="pagination-item">3</span>
            <span class="pagination-item dots">...</span>
            <span class="pagination-item">67</span>
            <span class="pagination-item">68</span>
            <span class="pagination-item"><i class="fas fa-chevron-right"></i></span>
        </div>

        <!-- Footer kecil -->
        <div class="extra-footer">
            <span><i class="far fa-file-pdf"></i> 45 dokumen tersedia</span>
        </div>
    </main>
</body>

</html>