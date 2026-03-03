<?php
require_once 'cek_login.php';
require_once 'proses/koneksi.php';

// Semua user yang sudah login boleh akses halaman ini
// (Admin: lihat semua user + tambah user | User: hanya lihat & ubah password sendiri)

// ---- Ambil data user untuk ditampilkan ----
if ($level_user == 1) {
    // Admin: tampilkan semua user
    $query_users = "SELECT id, nama, email, level FROM users ORDER BY level ASC, nama ASC";
} else {
    // User biasa: hanya tampilkan akun sendiri
    $query_users = "SELECT id, nama, email, level FROM users WHERE id = $id_user LIMIT 1";
}
$result_users = mysqli_query($conn, $query_users);

// ---- Pesan feedback (ubah password) ----
$feedback = '';
if (isset($_SESSION['pw_success'])) {
    $feedback = 'success';
    unset($_SESSION['pw_success']);
} elseif (isset($_SESSION['pw_error'])) {
    $feedback = $_SESSION['pw_error'];
    unset($_SESSION['pw_error']);
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pengaturan · Notulensi Rapat</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>

<body>
    <?php include 'sidebar.php'; ?>

    <main class="main-content">
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="page-title">
                <h1>Pengaturan</h1>
                <div class="breadcrumb">
                    <i class="fas fa-home"></i>
                    <?php echo ($level_user == 1) ? 'Dashboard / Pengaturan Akun' : 'Dashboard / Akun Saya'; ?>
                </div>
            </div>
            <div class="header-date">
                <i class="fas fa-calendar"></i>
                <span id="realtime-clock"></span>
            </div>
        </div>

        <div class="settings-container">

            <!-- ============================================
                 CARD: TAMBAH USER — hanya Admin (level=1)
                 ============================================ -->
            <?php if ($level_user == 1): ?>
            <div class="settings-card">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-user-plus"></i>
                    </div>
                    <h2>Tambah User Baru</h2>
                </div>

                <form action="proses/proses_tambah_user.php" method="POST">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="new_nama">
                                <i class="fas fa-user"></i> Nama
                            </label>
                            <input type="text" id="new_nama" name="nama" class="form-input" placeholder="Nama lengkap" required>
                        </div>
                        <div class="form-group">
                            <label for="new_email">
                                <i class="fas fa-envelope"></i> Email
                            </label>
                            <input type="email" id="new_email" name="email" class="form-input" placeholder="email@domain.com" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="new_password">
                                <i class="fas fa-lock"></i> Password
                            </label>
                            <div class="password-input">
                                <input type="password" id="new_password" name="password" class="form-input" placeholder="Minimal 8 karakter" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="new_level">
                                <i class="fas fa-shield-alt"></i> Level
                            </label>
                            <select id="new_level" name="level" class="form-input">
                                <option value="2">User</option>
                                <option value="1">Admin</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-user-plus"></i> Tambah User
                        </button>
                    </div>
                </form>
            </div>
            <?php endif; ?>

            <!-- ============================================
                 CARD: DAFTAR PENGGUNA
                 Admin: semua user | User: akun sendiri saja
                 ============================================ -->
            <div class="settings-card">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-<?php echo ($level_user == 1) ? 'users' : 'user-circle'; ?>"></i>
                    </div>
                    <h2><?php echo ($level_user == 1) ? 'Daftar Pengguna' : 'Akun Saya'; ?></h2>
                </div>

                <!-- Feedback ubah password -->
                <?php if ($feedback === 'success'): ?>
                <div class="alert-feedback success">
                    <i class="fas fa-check-circle"></i> Password berhasil diubah!
                </div>
                <?php elseif ($feedback !== ''): ?>
                <div class="alert-feedback error">
                    <i class="fas fa-exclamation-circle"></i> <?php echo htmlspecialchars($feedback); ?>
                </div>
                <?php endif; ?>

                <div class="user-list">
                    <?php if (mysqli_num_rows($result_users) > 0):
                        while ($u = mysqli_fetch_assoc($result_users)):
                            // Warna avatar berdasarkan level
                            $bg  = ($u['level'] == 1) ? '#e9f0fc' : '#f0fdf4';
                            $clr = ($u['level'] == 1) ? '#2463eb' : '#059669';
                            $inisial_u = strtoupper(substr($u['nama'], 0, 2));
                            $badge_label = ($u['level'] == 1) ? 'Administrator' : 'User';
                            $is_self = ($u['id'] == $id_user);
                    ?>
                    <div class="user-item">
                        <div class="user-avatar-small" style="background:<?php echo $bg; ?>; color:<?php echo $clr; ?>;">
                            <?php echo htmlspecialchars($inisial_u); ?>
                        </div>
                        <div class="user-info">
                            <div class="user-email">
                                <?php echo htmlspecialchars($u['email']); ?>
                                <?php if ($is_self): ?>
                                    <span style="font-size:0.7rem; color:#2463eb; font-weight:600; margin-left:6px;">(Saya)</span>
                                <?php endif; ?>
                            </div>
                            <div class="user-role-badge" style="background:<?php echo $bg; ?>; color:<?php echo $clr; ?>;">
                                <?php echo $badge_label; ?>
                            </div>
                        </div>
                        <div class="user-actions">
                            <!-- Tombol ubah password — hanya untuk akun sendiri, atau admin bisa ubah semua -->
                            <?php if ($is_self || $level_user == 1): ?>
                            <button class="btn-icon"
                                onclick="toggleChangePassword(<?php echo $u['id']; ?>)"
                                title="Ubah Password">
                                <i class="fas fa-key"></i>
                                <span>Ubah Password</span>
                            </button>
                            <?php endif; ?>

                            <!-- Tombol hapus — hanya Admin, dan tidak bisa hapus diri sendiri -->
                            <?php if ($level_user == 1 && !$is_self): ?>
                            <button class="btn-icon delete"
                                onclick="confirmDelete(<?php echo $u['id']; ?>, '<?php echo htmlspecialchars($u['email']); ?>')"
                                title="Hapus User">
                                <i class="fas fa-trash"></i>
                            </button>
                            <?php endif; ?>
                        </div>
                    </div>

                    <!-- Form ubah password (tersembunyi, muncul saat tombol diklik) -->
                    <?php if ($is_self || $level_user == 1): ?>
                    <div class="pw-form" id="pw-form-<?php echo $u['id']; ?>" style="display:none;">
                        <form action="proses/proses_ubah_password.php" method="POST"
                              style="background:#f8fcff; border:1.5px solid #e2ebf5; border-radius:16px; padding:18px 20px; margin-bottom:8px;">
                            <input type="hidden" name="target_id" value="<?php echo $u['id']; ?>">
                            <div class="form-row">
                                <div class="form-group">
                                    <label><i class="fas fa-lock"></i> Password Baru</label>
                                    <div class="password-input">
                                        <input type="password" name="new_password" class="form-input"
                                               placeholder="Minimal 5 karakter" required>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label><i class="fas fa-lock"></i> Konfirmasi Password</label>
                                    <div class="password-input">
                                        <input type="password" name="confirm_password" class="form-input"
                                               placeholder="Ulangi password baru" required>
                                    </div>
                                </div>
                            </div>
                            <div class="form-actions" style="gap:8px;">
                                <button type="button" class="btn btn-outline"
                                        onclick="toggleChangePassword(<?php echo $u['id']; ?>)">
                                    Batal
                                </button>
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-save"></i> Simpan Password
                                </button>
                            </div>
                        </form>
                    </div>
                    <?php endif; ?>

                    <?php endwhile; else: ?>
                    <p style="color:#6b7a8f; font-size:0.9rem; padding: 8px 0;">Tidak ada data pengguna.</p>
                    <?php endif; ?>
                </div>
            </div>

        </div><!-- /settings-container -->
    </main>

    <script>
        function toggleChangePassword(userId) {
            const form = document.getElementById('pw-form-' + userId);
            if (form) {
                form.style.display = (form.style.display === 'none') ? 'block' : 'none';
            }
        }

        function confirmDelete(userId, email) {
            if (confirm('Hapus user "' + email + '"? Tindakan ini tidak bisa dibatalkan.')) {
                window.location.href = 'proses/proses_hapus_user.php?id=' + userId;
            }
        }
    </script>

    <!-- Popup Alert JS -->
    <script src="assets/js/popup-alert.js"></script>
    <?php if ($feedback === 'success'): ?>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            showPopup('Password berhasil diubah!', 'success');
        });
    </script>
    <?php elseif ($feedback !== ''): ?>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            showPopup('<?php echo addslashes(htmlspecialchars($feedback)); ?>', 'error');
        });
    </script>
    <?php endif; ?>
</body>

</html>