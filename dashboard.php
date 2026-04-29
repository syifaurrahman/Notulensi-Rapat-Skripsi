<?php
require_once 'cek_login.php';

// Ambil flash message login sukses
$login_success = '';
if (isset($_SESSION['login_success'])) {
    $login_success = $_SESSION['login_success'];
    unset($_SESSION['login_success']);
}

// ── Konfigurasi DB ────────
define('DB_HOST', 'localhost');
define('DB_USER_DB', 'root');
define('DB_PASS_DB', '');
define('DB_NAME_DB', 'notulensi');

$conn = @mysqli_connect(DB_HOST, DB_USER_DB, DB_PASS_DB, DB_NAME_DB);

$total_meetings = 0;
$meetings_this_week = 0;
$meetings_last_week = 0;
$recent_meetings = [];

if ($conn) {
    // Total Meetings
    $res = mysqli_query($conn, "SELECT COUNT(*) as jml FROM notulensi_hasil");
    if ($res && $row = mysqli_fetch_assoc($res)) {
        $total_meetings = $row['jml'];
    }

    // Meetings This Week
    $res = mysqli_query($conn, "SELECT COUNT(*) as jml FROM notulensi_hasil WHERE YEARWEEK(waktu_rapat, 1) = YEARWEEK(CURDATE(), 1)");
    if ($res && $row = mysqli_fetch_assoc($res)) {
        $meetings_this_week = $row['jml'];
    }

    // Meetings Last Week
    $res = mysqli_query($conn, "SELECT COUNT(*) as jml FROM notulensi_hasil WHERE YEARWEEK(waktu_rapat, 1) = YEARWEEK(CURDATE() - INTERVAL 1 WEEK, 1)");
    if ($res && $row = mysqli_fetch_assoc($res)) {
        $meetings_last_week = $row['jml'];
    }

    // Recent meetings (limit 5)
    $res = mysqli_query($conn, "SELECT * FROM notulensi_hasil ORDER BY created_at DESC LIMIT 5");
    if ($res) {
        while ($row = mysqli_fetch_assoc($res)) {
            $recent_meetings[] = $row;
        }
    }
}

// Menghitung perbedaan
$diff = $meetings_this_week - $meetings_last_week;
$diff_text = "";
$diff_icon = "";
$diff_style = "";

if ($diff > 0) {
    $diff_text = "+$diff dari minggu lalu";
    $diff_icon = "fa-arrow-up";
    $diff_style = "color: #059669; background: #ecfdf5;";
} elseif ($diff < 0) {
    $diff_text = "$diff dari minggu lalu";
    $diff_icon = "fa-arrow-down";
    $diff_style = "color: #dc2626; background: #fef2f2;";
} else {
    $diff_text = "Sama dengan minggu lalu";
    $diff_icon = "fa-minus";
    $diff_style = "color: #64748b; background: #f1f5f9; border-color: transparent;";
}
?>

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
                <i class="fas fa-calendar-check"></i>
                <span id="realtime-clock"></span>
            </div>
        </div>

        <!-- KPI CARDS : Total Meetings & Meeting This Week -->
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Total Meetings</span>
                    <span class="kpi-number"><?= $total_meetings ?></span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-left">
                    <span class="kpi-label">Meeting This Week</span>
                    <span class="kpi-number"><?= $meetings_this_week ?></span>
                </div>
                <div class="kpi-badge" style="<?= $diff_style ?>">
                    <i class="fas <?= $diff_icon ?>"></i> <?= $diff_text ?>
                </div>
            </div>
        </div>

        <!-- Recent meetings header with "View All >" (kiri & kanan) -->
        <div class="recent-header">
            <h2>Recent meetings</h2>
            <a href="report.php" class="view-all-link"><i class="fas fa-arrow-right"></i> View All</a>
        </div>

        <!-- LIST MEETINGS -->
        <div class="meeting-list">
            <?php if (count($recent_meetings) > 0): ?>
                <?php foreach ($recent_meetings as $idx => $meeting): ?>
                    <?php
                        $judul = !empty($meeting['judul_rapat']) ? htmlspecialchars($meeting['judul_rapat']) : 'Tanpa Judul';
                        $waktu = strtotime($meeting['waktu_rapat']);
                        $isLive = $meeting['tipe_transkripsi'] === 'Live';
                        
                        // Icon based on type
                        $iconClass = $isLive ? 'fa-microphone' : 'fa-film';
                        
                        // Format durasi
                        $durasiDetik = isset($meeting['durasi_detik']) ? (int)$meeting['durasi_detik'] : 0;
                        if ($durasiDetik < 60) {
                            $durStr = $durasiDetik . " secs";
                        } elseif ($durasiDetik < 3600) {
                            $durStr = floor($durasiDetik / 60) . " mins";
                        } else {
                            $jam = floor($durasiDetik / 3600);
                            $menit = floor(($durasiDetik % 3600) / 60);
                            $durStr = $menit > 0 ? "{$jam} hr {$menit} mins" : "{$jam} hr";
                        }
                    ?>
                    <div class="meeting-item">
                        <div class="meeting-left">
                            <div class="meeting-title">
                                <i class="fas <?= $iconClass ?>" style="margin-right: 8px; color: #cbd5e1; font-size: 0.9em;"></i>
                                <?= $judul ?>
                            </div>
                            <div class="meeting-meta">
                                <span class="meta-item"><i class="far fa-calendar"></i> <?= date('j F Y', $waktu) ?></span>
                            </div>
                        </div>
                        <div class="meeting-right">
                            <?php if ($meeting['ringkasan'] === '[PROSES_TRANSKRIPSI]' || $meeting['ringkasan'] === '[PROSES_SUMMARIZE]'): ?>
                                <span class="duration-pill" style="background:#eef2ff; color:#2463eb;"><i class="fas fa-circle-notch fa-spin"></i> Processing</span>
                            <?php else: ?>
                                <span class="duration-pill"><i class="far fa-clock"></i> <?= $durStr ?></span>
                            <?php endif; ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php else: ?>
                <div style="padding: 30px; text-align: center; color: #94a3b8; background: #fff; border-radius: 16px; border: 1px dashed #cbd5e1;">
                    <i class="fas fa-folder-open fa-2x" style="margin-bottom:12px;opacity:0.5;"></i><br>
                    Belum ada rapat.<br>
                    <a href="notulensi_upload.php" style="color:#2463eb;font-weight:600;font-size:0.9rem;margin-top:8px;display:inline-block;">+ Tambah Rapat Baru</a>
                </div>
            <?php endif; ?>
        </div>
    </main>

    <!-- Popup Alert JS -->
    <script src="assets/js/popup-alert.js"></script>
    <?php if ($login_success): ?>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            showPopup('<?php echo addslashes(htmlspecialchars($login_success)); ?>', 'success');
        });
    </script>
    <?php endif; ?>
</body>
</html>