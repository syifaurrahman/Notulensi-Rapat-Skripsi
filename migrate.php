<?php
/**
 * ============================================================
 *  DATABASE MIGRATION SCRIPT - Notulensi Rapat
 * ============================================================
 *  Jalankan file ini SEKALI untuk:
 *    1. Membuat database `notulensi` (jika belum ada)
 *    2. Membuat tabel `users`
 *    3. Mengisi data awal (seeder)
 * 
 *  Cara pakai:
 *    - Buka browser: http://localhost/notulensi_rapat/migrate.php
 *    - ATAU jalankan via CLI: php migrate.php
 * ============================================================
 */

// ── Konfigurasi koneksi (sesuaikan jika perlu) ────────────────
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');           // Laragon default: kosong
define('DB_NAME', 'notulensi');
define('DB_CHARSET', 'utf8mb4');

// ── Helper output ─────────────────────────────────────────────
$isCli = PHP_SAPI === 'cli';

function log_msg(string $type, string $msg): void
{
    global $isCli;
    $icons = ['OK' => '✅', 'INFO' => 'ℹ️ ', 'ERROR' => '❌', 'SKIP' => '⏭️ '];
    $icon  = $icons[$type] ?? '•';

    if ($isCli) {
        echo "[$type] $msg\n";
    } else {
        $color = match ($type) {
            'OK'    => '#22c55e',
            'ERROR' => '#ef4444',
            'SKIP'  => '#f59e0b',
            default => '#60a5fa',
        };
        echo "<p style='margin:4px 0; color:{$color};'>{$icon} <b>[{$type}]</b> " . htmlspecialchars($msg) . "</p>\n";
    }
}

// ── Header output HTML ────────────────────────────────────────
if (!$isCli) {
    echo <<<HTML
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Database Migration</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #0f172a; color: #e2e8f0; min-height: 100vh;
      display: flex; align-items: center; justify-content: center; padding: 2rem;
    }
    .card {
      background: #1e293b; border: 1px solid #334155; border-radius: 12px;
      padding: 2rem; max-width: 680px; width: 100%;
      box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }
    h1 { font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: .25rem; }
    .subtitle { color: #94a3b8; font-size: .875rem; margin-bottom: 1.5rem; }
    .log-box {
      background: #0f172a; border: 1px solid #1e293b; border-radius: 8px;
      padding: 1rem; min-height: 120px; font-size: .875rem; line-height: 1.8;
    }
    .divider { border: none; border-top: 1px solid #334155; margin: 1.25rem 0; }
    .footer { color: #64748b; font-size: .75rem; margin-top: 1rem; }
    a.btn {
      display: inline-block; margin-top: 1rem; padding: .6rem 1.4rem;
      background: #3b82f6; color: #fff; border-radius: 8px;
      text-decoration: none; font-size: .875rem; font-weight: 600;
      transition: background .2s;
    }
    a.btn:hover { background: #2563eb; }
  </style>
</head>
<body>
<div class="card">
  <h1>🗄️ Database Migration</h1>
  <p class="subtitle">Notulensi Rapat &mdash; menjalankan migrasi…</p>
  <div class="log-box">
HTML;
}

// ════════════════════════════════════════════════════════════
//  LANGKAH 1 – Koneksi ke MySQL (tanpa memilih database dulu)
// ════════════════════════════════════════════════════════════
log_msg('INFO', "Menghubungkan ke MySQL di " . DB_HOST . " sebagai " . DB_USER . " …");

$conn = @mysqli_connect(DB_HOST, DB_USER, DB_PASS);
if (!$conn) {
    log_msg('ERROR', "Koneksi gagal: " . mysqli_connect_error());
    if (!$isCli) { echo "</div></div></body></html>"; }
    exit(1);
}
log_msg('OK', "Koneksi ke MySQL berhasil.");

// ════════════════════════════════════════════════════════════
//  LANGKAH 2 – Buat database jika belum ada
// ════════════════════════════════════════════════════════════
$dbName = DB_NAME;
$sql    = "CREATE DATABASE IF NOT EXISTS `{$dbName}` 
           CHARACTER SET " . DB_CHARSET . " 
           COLLATE " . DB_CHARSET . "_unicode_ci";

if (mysqli_query($conn, $sql)) {
    log_msg('OK', "Database `{$dbName}` siap digunakan.");
} else {
    log_msg('ERROR', "Gagal membuat database: " . mysqli_error($conn));
    mysqli_close($conn);
    if (!$isCli) { echo "</div></div></body></html>"; }
    exit(1);
}

// Pilih database
mysqli_select_db($conn, $dbName);
mysqli_set_charset($conn, DB_CHARSET);
mysqli_query($conn, "SET time_zone = '+07:00'");

// ════════════════════════════════════════════════════════════
//  LANGKAH 3 – Definisi migrasi (tabel + indeks)
// ════════════════════════════════════════════════════════════
$migrations = [

    // ── Tabel users ──────────────────────────────────────────
    'users' => [
        'create' => "CREATE TABLE IF NOT EXISTS `users` (
            `id`       INT(11)      NOT NULL AUTO_INCREMENT,
            `nama`     VARCHAR(100) NOT NULL,
            `email`    VARCHAR(100) NOT NULL,
            `password` VARCHAR(255) NOT NULL,
            `level`    TINYINT(1)   NOT NULL DEFAULT 2
                       COMMENT '1: Admin, 2: User',
            PRIMARY KEY (`id`),
            UNIQUE KEY `email` (`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=" . DB_CHARSET . " COLLATE=" . DB_CHARSET . "_unicode_ci",

        // Data awal (seeder) — password di-hash dengan password_hash()
        'seed' => [
            [
                'check' => "SELECT id FROM `users` WHERE `email` = 'Admin@admin.com' LIMIT 1",
                'insert' => "INSERT INTO `users` (`nama`, `email`, `password`, `level`) VALUES
                             ('Admin', 'Admin@admin.com', '" . password_hash('admin123', PASSWORD_BCRYPT) . "', 1)",
                'label'  => "Admin (Admin@admin.com)",
            ],
            [
                'check' => "SELECT id FROM `users` WHERE `email` = 'user@user.com' LIMIT 1",
                'insert' => "INSERT INTO `users` (`nama`, `email`, `password`, `level`) VALUES
                             ('User', 'user@user.com', '" . password_hash('user123', PASSWORD_BCRYPT) . "', 2)",
                'label'  => "User (user@user.com)",
            ],
        ],
    ],

    // ── (Tambahkan tabel baru di sini jika diperlukan) ────────
    // 'nama_tabel' => [ 'create' => "CREATE TABLE IF NOT EXISTS ...", 'seed' => [] ],

];

// ════════════════════════════════════════════════════════════
//  LANGKAH 4 – Jalankan migrasi
// ════════════════════════════════════════════════════════════
$totalOk    = 0;
$totalError = 0;

foreach ($migrations as $table => $def) {

    log_msg('INFO', "── Migrasi tabel `{$table}` …");

    // Buat tabel
    if (mysqli_query($conn, $def['create'])) {
        log_msg('OK', "Tabel `{$table}` berhasil dibuat / sudah ada.");
        $totalOk++;
    } else {
        log_msg('ERROR', "Gagal membuat tabel `{$table}`: " . mysqli_error($conn));
        $totalError++;
        continue;
    }

    // Jalankan seeder
    if (!empty($def['seed'])) {
        foreach ($def['seed'] as $row) {
            $exists = mysqli_query($conn, $row['check']);
            if ($exists && mysqli_num_rows($exists) > 0) {
                log_msg('SKIP', "Data sudah ada: {$row['label']}");
            } elseif (mysqli_query($conn, $row['insert'])) {
                log_msg('OK', "Data ditambahkan: {$row['label']}");
                $totalOk++;
            } else {
                log_msg('ERROR', "Gagal seed `{$row['label']}`: " . mysqli_error($conn));
                $totalError++;
            }
        }
    }
}

// ════════════════════════════════════════════════════════════
//  LANGKAH 5 – Ringkasan
// ════════════════════════════════════════════════════════════
mysqli_close($conn);

if (!$isCli) { echo "<hr class='divider'>"; }

if ($totalError === 0) {
    log_msg('OK', "Migrasi selesai! {$totalOk} operasi berhasil, 0 error.");
} else {
    log_msg('ERROR', "Migrasi selesai dengan {$totalError} error. Cek log di atas.");
}

// ── Footer HTML ───────────────────────────────────────────────
if (!$isCli) {
    echo <<<HTML
  </div><!-- /.log-box -->
  <p class="footer">
    ⚠️ <strong>Keamanan:</strong> hapus atau proteksi file <code>migrate.php</code> setelah migrasi selesai.
  </p>
  <a class="btn" href="index.php">← Kembali ke Aplikasi</a>
</div>
</body>
</html>
HTML;
}
