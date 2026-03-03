<?php
// proses/proses_hapus_user.php
session_start();
include_once 'koneksi.php';

// Harus sudah login
if (!isset($_SESSION['id'])) {
    header("Location: ../login.php");
    exit();
}

// Hanya Admin yang boleh hapus user
if ((int) $_SESSION['level'] != 1) {
    header("Location: ../pengaturan.php");
    exit();
}

$target_id  = (int) ($_GET['id'] ?? 0);
$current_id = (int) $_SESSION['id'];

// Tidak boleh hapus diri sendiri
if ($target_id == $current_id || $target_id <= 0) {
    header("Location: ../pengaturan.php");
    exit();
}

$query = "DELETE FROM users WHERE id = $target_id";
mysqli_query($conn, $query);

header("Location: ../pengaturan.php");
exit();
?>
