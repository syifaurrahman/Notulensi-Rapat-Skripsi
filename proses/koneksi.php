<?php
// koneksi.php — Docker-aware database connection
// Menggunakan environment variable jika tersedia (Docker),
// fallback ke localhost (Laragon/XAMPP)

$host     = getenv('DB_HOST') ?: 'localhost';
$username = getenv('DB_USER') ?: 'root';
$password = getenv('DB_PASS') ?: '';
$database = getenv('DB_NAME') ?: 'notulensi';

// Buat koneksi
$conn = mysqli_connect($host, $username, $password, $database);

// Cek koneksi
if (!$conn) {
    die("Koneksi database gagal: " . mysqli_connect_error());
}

// Set charset ke UTF-8
mysqli_set_charset($conn, "utf8");

// Untuk mengatasi error time zone (opsional)
mysqli_query($conn, "SET time_zone = '+07:00'");
?>