<?php
// proses/proses_logout.php
session_start();

// Hapus semua data session
session_unset();
session_destroy();

// Redirect ke halaman login (path relatif dari folder /proses/)
header("Location: ../login.php");
exit();
?>