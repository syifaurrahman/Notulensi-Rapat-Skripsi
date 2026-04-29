<?php
session_start();
header('Content-Type: application/json');

// Pastikan request dari user yang login
if (!isset($_SESSION['email'])) {
    echo json_encode(['status' => 'error', 'message' => 'Unauthorized']);
    exit;
}

// ── Konfigurasi DB (Sesuaikan dengan migrate.php) ────────
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'notulensi');

$conn = @mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if (!$conn) {
    echo json_encode(['status' => 'error', 'message' => 'Koneksi database gagal']);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Ambil data POST
    $judul_rapat = isset($_POST['judul_rapat']) ? mysqli_real_escape_string($conn, $_POST['judul_rapat']) : 'Tanpa Judul';
    $tipe = isset($_POST['tipe_transkripsi']) ? mysqli_real_escape_string($conn, $_POST['tipe_transkripsi']) : 'Live';
    
    // Set waktu ke saat ini (sesuai zona waktu server)
    date_default_timezone_set('Asia/Jakarta');
    $waktu_rapat = date('Y-m-d H:i:s');
    
    // Periksa file PDF
    if (!isset($_FILES['pdf_file']) || $_FILES['pdf_file']['error'] !== UPLOAD_ERR_OK) {
        echo json_encode(['status' => 'error', 'message' => 'File PDF tidak ditemukan atau gagal diunggah']);
        exit;
    }

    // Direktori tujuan
    $uploadDir = '../assets/pdf/';
    if (!is_dir($uploadDir)) {
        if(!mkdir($uploadDir, 0777, true)) {
            echo json_encode(['status' => 'error', 'message' => 'Gagal membuat folder PDF']);
            exit;
        }
    }

    // Buat nama unik dan pindahkan file
    $filename = 'transkrip_' . time() . '_' . rand(100, 999) . '.pdf';
    $targetPath = $uploadDir . $filename;
    
    if (move_uploaded_file($_FILES['pdf_file']['tmp_name'], $targetPath)) {
        
        // Simpan path ke DB (relative)
        $dbPath = 'assets/pdf/' . $filename;
        
        $sql = "INSERT INTO notulensi_hasil (judul_rapat, waktu_rapat, tipe_transkripsi, file_pdf) 
                VALUES ('$judul_rapat', '$waktu_rapat', '$tipe', '$dbPath')";
                
        if (mysqli_query($conn, $sql)) {
            echo json_encode(['status' => 'success', 'message' => 'Berhasil disimpan', 'file_path' => $dbPath]);
        } else {
            // Hapus file jika query DB gagal
            unlink($targetPath);
            echo json_encode(['status' => 'error', 'message' => 'Gagal menyimpan ke database: ' . mysqli_error($conn)]);
        }
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Gagal memindahkan file yang diunggah']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid method']);
}
