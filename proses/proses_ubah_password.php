<?php
// proses/proses_ubah_password.php
session_start();
include_once 'koneksi.php';

// Harus sudah login
if (!isset($_SESSION['id'])) {
    header("Location: ../login.php");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("Location: ../pengaturan.php");
    exit();
}

$current_id   = (int) $_SESSION['id'];
$level        = (int) $_SESSION['level'];
$target_id    = (int) ($_POST['target_id'] ?? 0);
$new_password = trim($_POST['new_password']     ?? '');
$confirm      = trim($_POST['confirm_password'] ?? '');

// Keamanan: User biasa hanya boleh ubah password dirinya sendiri
if ($level != 1 && $target_id != $current_id) {
    $_SESSION['pw_error'] = 'Anda tidak memiliki izin untuk mengubah password user lain.';
    header("Location: ../pengaturan.php");
    exit();
}

// Validasi password
if (strlen($new_password) < 5) {
    $_SESSION['pw_error'] = 'Password minimal 5 karakter.';
    header("Location: ../pengaturan.php");
    exit();
}

if ($new_password !== $confirm) {
    $_SESSION['pw_error'] = 'Konfirmasi password tidak cocok.';
    header("Location: ../pengaturan.php");
    exit();
}

// Hash password baru dengan bcrypt sebelum disimpan
$hashed     = password_hash($new_password, PASSWORD_DEFAULT);
$hashed_esc = mysqli_real_escape_string($conn, $hashed);
$query      = "UPDATE users SET password = '$hashed_esc' WHERE id = $target_id";
$result     = mysqli_query($conn, $query);

if ($result) {
    $_SESSION['pw_success'] = true;
} else {
    $_SESSION['pw_error'] = 'Gagal mengubah password. Silakan coba lagi.';
}

header("Location: ../pengaturan.php");
exit();
?>
