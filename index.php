<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notulen Rapat · Sidebar Dashboard</title>
    <!-- Font Awesome 6 (free) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Font: Inter (modern & clean) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">

</head>

<body>

    <?php include 'sidebar.php'; ?>
    <!-- MAIN CONTENT (dashboard) -->
    <main class="main-content">
        <!-- top bar with page greeting & date -->
        <div class="top-bar">
            <div class="page-title">
                <h1>Dashboard</h1>
                <p>Ringkasan notulen dan aktivitas rapat</p>
            </div>
            <div class="header-date">
                <i class="fas fa-calendar-check"></i> 17 Feb 2026 · Senin
            </div>
        </div>

        <!-- KPI CARDS : Total Meetings 20 & Meeting This Week 5 -->
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Total Meetings</span>
                    <span class="kpi-number">20</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Meeting This Week</span>
                    <span class="kpi-number">5</span>
                </div>
                <div class="kpi-badge">
                    <i class="fas fa-arrow-up"></i> +2 dari minggu lalu
                </div>
            </div>
        </div>

        <!-- Recent meetings header with "View All >" (kiri & kanan) -->
        <div class="recent-header">
            <h2>Recent meetings</h2>
            <span class="view-all-link"><i class="fas fa-arrow-right"></i> View All</span>
        </div>

        <!-- LIST MEETINGS (sesuai gambar: 3 item + draft di tengah) -->
        <div class="meeting-list">
            <!-- 1. Rapat Tim Marketing · 22 Apr 2024 · 45 mins -->
            <div class="meeting-item">
                <div class="meeting-left">
                    <div class="meeting-title">Rapat Tim Marketing</div>
                    <div class="meeting-meta">
                        <span class="meta-item"><i class="far fa-calendar"></i> 22 Apr 2024</span>
                    </div>
                </div>
                <div class="meeting-right">
                    <span class="duration-pill"><i class="far fa-clock"></i> 45 mins</span>
                </div>
            </div>

            <!-- 2. Evaluasi Proyek AI + Draft · 20 Apr 2024 · 60 mins -->
            <div class="meeting-item">
                <div class="meeting-left">
                    <div class="meeting-title">
                        Evaluasi Proyek AI
                    </div>
                    <div class="meeting-meta">
                        <span class="meta-item"><i class="far fa-calendar"></i> 20 Apr 2024</span>
                    </div>
                </div>
                <div class="meeting-right">
                    <span class="duration-pill"><i class="far fa-clock"></i> 60 mins</span>
                </div>
            </div>

            <!-- 3. Rapat Pengembangan Produk · 18 Apr 2024 · 75 mins -->
            <div class="meeting-item">
                <div class="meeting-left">
                    <div class="meeting-title">Rapat Pengembangan Produk</div>
                    <div class="meeting-meta">
                        <span class="meta-item"><i class="far fa-calendar"></i> 18 Apr 2024</span>
                    </div>
                </div>
                <div class="meeting-right">
                    <span class="duration-pill"><i class="far fa-clock"></i> 75 mins</span>
                </div>
            </div>
        </div>
    </main>

    <script src=""></script>
    
</body>
</html>