<?php
/**
 * setup_password.php
 * Script SEKALI JALAN untuk mengubah semua password plain text
 * di database menjadi bcrypt hash.
 *
 * Cara pakai:
 *   Buka browser: http://localhost/notulensi_rapat/setup_password.php
 *   Setelah selesai, HAPUS file ini dari server!
 */

// Keamanan minimal: hanya bisa diakses via localhost
if (!in_array($_SERVER['REMOTE_ADDR'], ['127.0.0.1', '::1'])) {
    die('Akses ditolak. File ini hanya boleh dijalankan dari localhost.');
}

include_once 'proses/koneksi.php';

// Ambil semua user
$result = mysqli_query($conn, "SELECT id, email, password FROM users");
$updated = 0;
$skipped = 0;
$log     = [];

while ($row = mysqli_fetch_assoc($result)) {
    // Cek apakah password sudah dalam format hash bcrypt (diawali $2y$)
    if (str_starts_with($row['password'], '$2y$')) {
        $log[] = "⏭ <b>{$row['email']}</b> — sudah bcrypt, dilewati.";
        $skipped++;
        continue;
    }

    // Hash password lama dengan bcrypt
    $hashed = password_hash($row['password'], PASSWORD_DEFAULT);
    $hashed_esc = mysqli_real_escape_string($conn, $hashed);

    $update = mysqli_query($conn, "UPDATE users SET password = '$hashed_esc' WHERE id = {$row['id']}");

    if ($update) {
        $log[] = "✅ <b>{$row['email']}</b> — password berhasil di-hash.";
        $updated++;
    } else {
        $log[] = "❌ <b>{$row['email']}</b> — gagal update: " . mysqli_error($conn);
    }
}

mysqli_close($conn);
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Setup Password Hash</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7fc; padding: 40px; color: #1a2639; }
        .card { background: white; border-radius: 16px; padding: 28px 32px; max-width: 560px; margin: 0 auto;
                box-shadow: 0 8px 24px rgba(0,0,0,0.07); border: 1px solid #e2ebf5; }
        h2 { color: #0a2540; margin-bottom: 8px; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 40px; font-size: 0.8rem; font-weight: 600; }
        .success { background: #d1fae5; color: #065f46; }
        .info    { background: #dbeafe; color: #1e40af; }
        .log-item { padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; background: #f8fcff;
                    border: 1px solid #e2ebf5; font-size: 0.9rem; }
        .warning { background: #fef3c7; border: 1px solid #fde68a; border-radius: 12px;
                   padding: 14px 16px; margin-top: 20px; color: #92400e; font-size: 0.9rem; }
        hr { border: none; border-top: 1px solid #eef2f8; margin: 20px 0; }
    </style>
</head>
<body>
<div class="card">
    <h2>🔐 Setup Password Hash</h2>
    <p style="color:#6b7a8f; margin-bottom: 20px;">Proses hashing password database selesai.</p>

    <hr>

    <div style="display:flex; gap:12px; margin-bottom: 20px;">
        <span class="badge success">✅ <?php echo $updated; ?> diupdate</span>
        <span class="badge info">⏭ <?php echo $skipped; ?> dilewati</span>
    </div>

    <?php foreach ($log as $item): ?>
        <div class="log-item"><?php echo $item; ?></div>
    <?php endforeach; ?>

    <div class="warning">
        ⚠️ <strong>Penting!</strong> Setelah halaman ini berhasil, segera <strong>hapus file
        <code>setup_password.php</code></strong> dari server agar tidak bisa diakses orang lain.
    </div>
</div>
</body>
</html>
