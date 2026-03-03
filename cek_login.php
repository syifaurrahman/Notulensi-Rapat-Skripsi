<?php
// cek_login.php - letakkan di folder root (sama dengan dashboard.php)
session_start();

// Cek apakah user sudah login
if (!isset($_SESSION['id'])) {
    header("Location: login.php");
    exit();
}

// Ambil data session
$id_user = $_SESSION['id'];
$nama_user = $_SESSION['nama'];
$email_user = $_SESSION['email'];
$level_user = $_SESSION['level']; // 1 = Admin, 2 = User

// Fungsi untuk mengecek halaman aktif
function isActive($page) {
    $current_page = basename($_SERVER['PHP_SELF']);
    return $current_page == $page ? 'active' : '';
}

// Inisial untuk avatar
$inisial = '';
$kata = explode(' ', $nama_user);
if (count($kata) > 1) {
    $inisial = strtoupper(substr($kata[0], 0, 1) . substr($kata[1], 0, 1));
} else {
    $inisial = strtoupper(substr($nama_user, 0, 2));
}
?>