<?php
/**
 * insert_llm_only.php — Script PHP untuk memasukkan hasil ringkasan LLM murni ke database
 */

define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'notulensi');

$conn = @mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if (!$conn) {
    die("[ERROR] Koneksi database gagal: " . mysqli_connect_error() . "\n");
}

$summary_file = __DIR__ . '/hasil_summarize/LLM_only.txt';
if (!file_exists($summary_file)) {
    die("[ERROR] File ringkasan tidak ditemukan: $summary_file\n");
}

// Baca ringkasan, skip header pembatas (baris 1 s.d. 4)
$lines = file($summary_file);
$clean_summary_lines = array_slice($lines, 4);
$ringkasan = implode("", $clean_summary_lines);

// Metadata rapat (berdasarkan transkrip asli)
$judul_rapat = "Zoom Meeting Psikologi Sosial I C 2022 02 23 13 15 57 (LLM Only)";
$waktu_rapat = "2026-06-09 20:08:19";
$tipe_transkripsi = "Upload";
$transkrip_txt = "whisper transkrip psikologi.txt";
$durasi_detik = 0;

$judul_rapat_esc = mysqli_real_escape_string($conn, $judul_rapat);
$waktu_rapat_esc = mysqli_real_escape_string($conn, $waktu_rapat);
$tipe_transkripsi_esc = mysqli_real_escape_string($conn, $tipe_transkripsi);
$transkrip_txt_esc = mysqli_real_escape_string($conn, $transkrip_txt);
$ringkasan_esc = mysqli_real_escape_string($conn, $ringkasan);

$sql = "INSERT INTO `notulensi_hasil` (`judul_rapat`, `waktu_rapat`, `tipe_transkripsi`, `transkrip_txt`, `durasi_detik`, `ringkasan`, `file_pdf`, `created_at`) 
        VALUES ('$judul_rapat_esc', '$waktu_rapat_esc', '$tipe_transkripsi_esc', '$transkrip_txt_esc', $durasi_detik, '$ringkasan_esc', '', NOW())";

if (mysqli_query($conn, $sql)) {
    echo "[SUCCESS] Data LLM Only berhasil dimasukkan ke tabel notulensi_hasil!\n";
    echo "          ID Data: " . mysqli_insert_id($conn) . "\n";
} else {
    echo "[ERROR] Gagal memasukkan data: " . mysqli_error($conn) . "\n";
}

mysqli_close($conn);
