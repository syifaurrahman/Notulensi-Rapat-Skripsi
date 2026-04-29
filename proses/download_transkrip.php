<?php
/**
 * download_transkrip.php
 * Endpoint download file .txt hasil transkripsi dari folder whispertranscription/hasil/
 */

session_start();

if (!isset($_SESSION['email'])) {
    http_response_code(403);
    exit('Unauthorized');
}

$filename = isset($_GET['file']) ? basename($_GET['file']) : '';

if (empty($filename)) {
    http_response_code(400);
    exit('Nama file tidak valid');
}

// Hanya boleh file .txt
if (pathinfo($filename, PATHINFO_EXTENSION) !== 'txt') {
    http_response_code(400);
    exit('Tipe file tidak diizinkan');
}

$filePath = 'C:\\laragon\\www\\notulensi_rapat\\whispertranscription\\hasil\\' . $filename;

if (!file_exists($filePath)) {
    http_response_code(404);
    exit('File tidak ditemukan: ' . $filename);
}

header('Content-Type: text/plain; charset=utf-8');
header('Content-Disposition: attachment; filename="' . $filename . '"');
header('Content-Length: ' . filesize($filePath));
header('Cache-Control: no-store');

readfile($filePath);
exit;
