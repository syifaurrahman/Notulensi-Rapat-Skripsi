<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pengaturan · Notulensi Rapat</title>
    <!-- Font Awesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Font: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap"
        rel="stylesheet">
    <!-- CSS Files -->
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/sidebar.css">
</head>

<body>

    <aside class="sidebar">
        <div class="logo-area">
            <span class="logo-icon"><i class="fas fa-pen-to-square"></i></span>
            <span class="logo-text">Notulensia</span>
        </div>

        <div class="nav-menu">
            <!-- Dashboard - semua level -->
            <a href="dashboard.php" class="nav-item <?php echo isActive('dashboard.php'); ?>">
                <i class="fas fa-th-large"></i>
                <span>Dashboard</span>
            </a>

            <!-- Notulensi - hanya Admin (level = 1) -->
            <?php if ($level_user == 1): ?>
                <a href="notulensi.php" class="nav-item <?php echo isActive('notulensi.php'); ?>">
                    <i class="fas fa-file-alt"></i>
                    <span>Notulensi</span>
                </a>
            <?php endif; ?>

            <!-- Report - semua level -->
            <a href="report.php" class="nav-item <?php echo isActive('report.php'); ?>">
                <i class="fas fa-chart-pie"></i>
                <span>Report</span>
            </a>

            <!-- Pengaturan - semua level -->
            <a href="pengaturan.php" class="nav-item <?php echo isActive('pengaturan.php'); ?>">
                <i class="fas fa-cog"></i>
                <span>Pengaturan</span>
            </a>
        </div>

        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar"><?php echo $inisial; ?></div>
                <div class="user-details">
                    <span class="user-name"><?php echo $nama_user; ?></span>
                    <span class="user-role"><?php echo ($level_user == 1) ? 'Admin' : 'User'; ?></span>
                </div>
            </div>
            <a href="proses/proses_logout.php" class="logout-btn">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        </div>
    </aside>
    <script src="assets/js/realtime-clock.js"></script>
</body>

</html>