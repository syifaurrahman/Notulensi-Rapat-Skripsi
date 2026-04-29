<?php
/**
 * proses_upload_transkripsi.php
 * Handler upload video → panggil Python Whisper → kembalikan JSON hasil
 */

session_start();
header('Content-Type: application/json; charset=utf-8');

// Auth check
if (!isset($_SESSION['email'])) {
    echo json_encode(['status' => 'error', 'message' => 'Unauthorized']);
    exit;
}

// Hanya menerima POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'Method tidak valid']);
    exit;
}

// ── Konfigurasi Path ───────────────────────────────────────────────────────
// Path absolut ke Python dalam virtual environment (sama seperti Live Whisper)
$pythonBin  = 'C:\\laragon\\www\\notulensi_rapat\\whispertranscription\\.env\\Scripts\\python.exe';
$scriptPath = 'C:\\laragon\\www\\notulensi_rapat\\whispertranscription\\transcribe_api.py';
$uploadDir  = 'C:\\laragon\\www\\notulensi_rapat\\whispertranscription\\uploads\\';

// ── Validasi File Upload ───────────────────────────────────────────────────
if (!isset($_FILES['video_file']) || $_FILES['video_file']['error'] !== UPLOAD_ERR_OK) {
    $errCode = $_FILES['video_file']['error'] ?? -1;
    echo json_encode(['status' => 'error', 'message' => 'File tidak ditemukan atau gagal diunggah (kode: ' . $errCode . ')']);
    exit;
}

$file     = $_FILES['video_file'];
$maxBytes = 500 * 1024 * 1024; // 500 MB

// Cek ukuran
if ($file['size'] > $maxBytes) {
    echo json_encode(['status' => 'error', 'message' => 'Ukuran file melebihi batas 500 MB']);
    exit;
}

// Cek ekstensi
$allowedExt = ['mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', 'mp3'];
$ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
if (!in_array($ext, $allowedExt)) {
    echo json_encode(['status' => 'error', 'message' => 'Format file tidak didukung: ' . $ext]);
    exit;
}

// ── Simpan File Sementara ──────────────────────────────────────────────────
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

$uniqueName   = 'upload_' . time() . '_' . rand(100, 999) . '.' . $ext;
$tempFilePath = $uploadDir . $uniqueName;

if (!move_uploaded_file($file['tmp_name'], $tempFilePath)) {
    echo json_encode(['status' => 'error', 'message' => 'Gagal menyimpan file sementara']);
    exit;
}

// ── Jalankan Python Whisper ────────────────────────────────────────────────
// Escape path untuk keamanan
$escapedPython = escapeshellarg($pythonBin);
$escapedScript = escapeshellarg($scriptPath);
$escapedFile   = escapeshellarg($tempFilePath);

// Set timeout (PHP default exec tidak ada timeout, tapi set max_execution_time)
set_time_limit(0); // Nonaktifkan timeout PHP untuk proses panjang

$command = "$escapedPython $escapedScript $escapedFile 2>&1";
$output  = [];
$retCode = 0;

exec($command, $output, $retCode);

// Hapus file upload sementara setelah selesai
@unlink($tempFilePath);

// ── Parse Output JSON dari Python ─────────────────────────────────────────
$rawOutput = implode("\n", $output);

// Cari baris JSON terakhir (Python mungkin print log lain sebelumnya)
$jsonLine = '';
foreach (array_reverse($output) as $line) {
    $line = trim($line);
    if ($line && $line[0] === '{') {
        $jsonLine = $line;
        break;
    }
}

if (empty($jsonLine)) {
    echo json_encode([
        'status'  => 'error',
        'message' => 'Tidak ada output dari Python.',
        'raw'     => $rawOutput
    ]);
    exit;
}

$result = json_decode($jsonLine, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    echo json_encode([
        'status'  => 'error',
        'message' => 'Output Python tidak valid (bukan JSON).',
        'raw'     => $rawOutput
    ]);
    exit;
}

// Kembalikan hasil ke frontend
echo json_encode($result, JSON_UNESCAPED_UNICODE);
