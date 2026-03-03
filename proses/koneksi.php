<?php
// koneksi.php
$host = 'localhost'; // default laragon
$username = 'root'; // default laragon
$password = ''; // default laragon (kosong)
$database = 'notulensi'; // nama database Anda

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