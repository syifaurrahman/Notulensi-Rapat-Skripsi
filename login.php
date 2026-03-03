<?php
session_start();
$error = '';
if (isset($_SESSION['login_error'])) {
    $error = $_SESSION['login_error'];
    unset($_SESSION['login_error']);
}
?>
<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Notulensia</title>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts - Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="assets/css/base.css">
    <link rel="stylesheet" href="assets/css/login.css">
</head>

<body class="login-page">
    <div class="login-container">
        <!-- Left Side - Illustration -->
        <div class="login-illustration">
            <div class="illustration-content">
                <i class="fas fa-pen-fancy illustration-icon"></i>
                <h2>Notulensia</h2>
                <p>Catat, Kelola, dan Bagikan Notulen Rapat dengan Mudah</p>
                <div class="feature-list">
                    <div class="feature-item">
                        <i class="fas fa-check-circle"></i>
                        <span>Transkripsi Otomatis</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-check-circle"></i>
                        <span>Rangkum Hasil Rapat</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Side - Login Card -->
        <div class="login-card">
            <div class="login-header">
                <div class="logo-area">
                    <div class="logo-icon">
                        <i class="fas fa-pen-fancy"></i>
                    </div>
                    <span class="logo-text">Notulensia</span>
                </div>
                <h1 class="login-title">Selamat Datang Kembali</h1>
                <p class="login-subtitle">Silakan masuk ke akun Anda untuk melanjutkan</p>
            </div>

            <!-- Perbaiki form action - sesuaikan dengan struktur folder -->
            <form class="login-form" method="POST" action="proses/proses_login.php">
                <!-- Email Field -->
                <div class="form-group">
                    <label class="form-label">
                        <i class="fas fa-envelope"></i>
                        Email
                    </label>
                    <input type="email" class="form-input" id="email" name="email" placeholder="Masukkan email Anda"
                        required>
                </div>

                <!-- Password Field -->
                <div class="form-group">
                    <label class="form-label">
                        <i class="fas fa-lock"></i>
                        Password
                    </label>
                    <div class="password-wrapper">
                        <input type="password" class="form-input" id="password" name="password"
                            placeholder="Masukkan password Anda" required>
                        <button type="button" class="password-toggle" id="togglePassword">
                            <i class="far fa-eye"></i>
                        </button>
                    </div>
                </div>

                <!-- Remember Me & Forgot Password -->
                <div class="form-options">
                    <label class="checkbox-label">
                        <input type="checkbox" class="checkbox" name="remember" checked>
                        <span>Ingat saya</span>
                    </label>
                    <a href="#" class="forgot-link">Lupa Password?</a>
                </div>

                <!-- Login Button -->
                <button type="submit" class="btn btn-primary btn-login">
                    <i class="fas fa-sign-in-alt"></i>
                    Masuk
                </button>

                <!-- Error Message -->
                <?php if ($error): ?>
                <div class="demo-info" style="background:#fee2e2; border-color:#fecaca; color:#991b1b;">
                    <i class="fas fa-exclamation-circle" style="color:#dc2626;"></i>
                    <span><?php echo htmlspecialchars($error); ?></span>
                </div>
                <?php endif; ?>

                <!-- Demo Info -->
                <div class="demo-info">
                    <i class="fas fa-info-circle"></i>
                    <span>Demo: Admin@admin.com / admin123 &nbsp;|&nbsp; user@user.com / user123</span>
                </div>
            </form>

            <div class="login-footer">
                <p>© 2024 Notulensia. Semua hak dilindungi.</p>
            </div>
        </div>
    </div>

    <script>
        // Toggle Password Visibility
        document.getElementById('togglePassword').addEventListener('click', function () {
            const passwordInput = document.getElementById('password');
            const icon = this.querySelector('i');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    </script>

    <!-- Popup Alert JS -->
    <script src="assets/js/popup-alert.js"></script>
    <?php if ($error): ?>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            showPopup('<?php echo addslashes(htmlspecialchars($error)); ?>', 'error');
        });
    </script>
    <?php endif; ?>
</body>

</html>