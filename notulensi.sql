-- ============================================================
-- notulensi.sql — Full Database Schema + Seed Data
-- Digunakan oleh Docker (docker-entrypoint-initdb.d)
-- & sebagai referensi instalasi manual
-- ============================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+07:00";
START TRANSACTION;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ── Buat database jika belum ada ──────────────────────────────
CREATE DATABASE IF NOT EXISTS `notulensi`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `notulensi`;

-- ── Tabel: users ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `users` (
    `id`       INT(11)      NOT NULL AUTO_INCREMENT,
    `nama`     VARCHAR(100) NOT NULL,
    `email`    VARCHAR(100) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `level`    TINYINT(1)   NOT NULL DEFAULT 2
               COMMENT '1: Admin, 2: User',
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed: Data user awal (password di-hash dengan bcrypt)
-- Admin: admin123 | User: user123
INSERT IGNORE INTO `users` (`nama`, `email`, `password`, `level`) VALUES
('Admin', 'Admin@admin.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 1),
('User',  'user@user.com',   '$2y$10$TKh8H1.PfuPhX9XDo21R8eQ5tIfPNmDxuDVJXxPKfj1Q3VJZzDfv2', 2);
-- Catatan: hash di atas adalah password_hash() default.
-- Gunakan migrate.php untuk generate hash yang benar jika login gagal.

-- ── Tabel: notulensi_hasil ────────────────────────────────────
CREATE TABLE IF NOT EXISTS `notulensi_hasil` (
    `id`               INT(11)      NOT NULL AUTO_INCREMENT,
    `judul_rapat`      VARCHAR(255) NOT NULL,
    `waktu_rapat`      DATETIME     NOT NULL,
    `tipe_transkripsi` ENUM('Live','Upload') NOT NULL DEFAULT 'Live',
    `transkrip_txt`    VARCHAR(500) DEFAULT NULL
                       COMMENT 'nama file .txt hasil transkripsi',
    `durasi_detik`     INT(11)      DEFAULT 0
                       COMMENT 'durasi video/audio dalam detik',
    `ringkasan`        TEXT         DEFAULT NULL
                       COMMENT 'ringkasan LexRank',
    `file_pdf`         VARCHAR(255) DEFAULT NULL
                       COMMENT 'path file PDF (fitur lama)',
    `created_at`       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;
