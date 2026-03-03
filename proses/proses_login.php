<?php
session_start();

// Jika sudah login, langsung ke dashboard
if (isset($_SESSION['id'])) {
    header("Location: ../dashboard.php");
    exit();
}

// Include koneksi
include_once "koneksi.php";

// Pastikan request dari form POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("Location: ../login.php");
    exit();
}

// Ambil dan bersihkan input
$email    = trim($_POST['email']    ?? '');
$password = trim($_POST['password'] ?? '');

// Validasi tidak kosong
if (empty($email) || empty($password)) {
    $_SESSION['login_error'] = 'Email dan Password harus diisi!';
    header("Location: ../login.php");
    exit();
}

// Escape hanya email, password diverifikasi lewat PHP (bukan SQL)
$email_esc = mysqli_real_escape_string($conn, $email);

// Query hanya berdasarkan email — password dicek via password_verify()
$query  = "SELECT * FROM users WHERE email = '$email_esc' LIMIT 1";
$result = mysqli_query($conn, $query);

if (!$result) {
    $_SESSION['login_error'] = 'Terjadi kesalahan sistem. Silakan coba lagi.';
    header("Location: ../login.php");
    exit();
}

if (mysqli_num_rows($result) > 0) {
    $data = mysqli_fetch_assoc($result);

    // Verifikasi password: support bcrypt hash DAN plain text (transisi)
    $password_valid = password_verify($password, $data['password'])
                   || $data['password'] === $password; // fallback plain text sementara

    if ($password_valid) {
        // Jika masih plain text, auto-upgrade ke bcrypt saat login
        if ($data['password'] === $password) {
            $new_hash     = password_hash($password, PASSWORD_DEFAULT);
            $new_hash_esc = mysqli_real_escape_string($conn, $new_hash);
            mysqli_query($conn, "UPDATE users SET password='$new_hash_esc' WHERE id={$data['id']}");
        }

        // Set session
        $_SESSION['id']    = $data['id'];
        $_SESSION['nama']  = $data['nama'];
        $_SESSION['email'] = $data['email'];
        $_SESSION['level'] = $data['level'];

        // Flash message: berhasil login
        $_SESSION['login_success'] = 'Selamat datang, ' . $data['nama'] . '!';

        header("Location: ../dashboard.php");
        exit();

    } else {
        // Email ditemukan tapi password salah
        $_SESSION['login_error'] = 'Email atau Password salah!';
        header("Location: ../login.php");
        exit();
    }

} else {
    // Email tidak ditemukan
    $_SESSION['login_error'] = 'Email atau Password salah!';
    header("Location: ../login.php");
    exit();
}
?>
