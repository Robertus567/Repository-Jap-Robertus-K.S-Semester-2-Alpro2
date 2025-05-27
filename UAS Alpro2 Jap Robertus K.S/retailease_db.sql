-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for retailese_db
CREATE DATABASE IF NOT EXISTS `retailese_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `retailese_db`;

-- Dumping structure for table retailese_db.kulakan
CREATE TABLE IF NOT EXISTS `kulakan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_toko` varchar(255) NOT NULL,
  `nama_barang` varchar(255) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `tanggal` date NOT NULL,
  `catatan` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table retailese_db.kulakan: ~11 rows (approximately)
INSERT INTO `kulakan` (`id`, `nama_toko`, `nama_barang`, `harga`, `tanggal`, `catatan`, `created_at`) VALUES
	(1, 'Toko Glory', 'Indomie (1 dus)', 138000.00, '2025-05-23', 'Kadang dikasi diskon sama ciciknya', '2025-05-22 18:43:58'),
	(2, 'Bu Slamet', 'Indomie (1 dus)', 130000.00, '2025-05-23', '', '2025-05-22 18:44:35'),
	(3, 'Bu Joko', 'Indomie', 3000.00, '2025-05-26', '', '2025-05-26 05:10:57'),
	(4, 'Toko Sumber Rezeki', 'Indomie', 4000.00, '2025-05-26', '', '2025-05-26 10:59:41'),
	(5, 'Bu Joko', 'Beras', 17000.00, '2025-05-26', '', '2025-05-26 13:42:41'),
	(6, 'Toko Sumber Rezeki', 'Beras', 18000.00, '2025-05-26', '', '2025-05-26 13:43:18'),
	(7, 'Pak Budi', 'Beras', 14000.00, '2025-05-26', '', '2025-05-26 14:01:33'),
	(8, 'Bu Joko', 'Kertas A3', 20000.00, '2025-05-27', '', '2025-05-26 19:32:23'),
	(9, 'Toko Sumber Rezeki', 'Kertas A3', 10000.00, '2025-05-27', '', '2025-05-26 19:32:41'),
	(10, 'Toko Sumber Rezeki', 'Es batu', 2000.00, '2025-05-27', '', '2025-05-26 20:14:44'),
	(11, 'Bu Slamet', 'Es batu', 20000.00, '2025-05-27', '', '2025-05-26 20:14:56');

-- Dumping structure for table retailese_db.penjualan
CREATE TABLE IF NOT EXISTS `penjualan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_barang` varchar(255) NOT NULL,
  `harga_satuan` decimal(10,2) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `total_harga` decimal(10,2) NOT NULL,
  `tanggal_penjualan` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table retailese_db.penjualan: ~26 rows (approximately)
INSERT INTO `penjualan` (`id`, `nama_barang`, `harga_satuan`, `jumlah`, `total_harga`, `tanggal_penjualan`, `created_at`) VALUES
	(1, 'Telur/kg', 30000.00, 4, 120000.00, '2025-05-24', '2025-05-24 13:44:27'),
	(2, 'Gula (Gulaku)/kg', 18000.00, 2, 36000.00, '2025-05-24', '2025-05-24 13:44:55'),
	(3, 'Garam (Kapal) / 250 g', 2800.00, 2, 5600.00, '2025-05-24', '2025-05-24 13:45:03'),
	(4, 'Royco Sapi (1 Sachet)', 500.00, 10, 5000.00, '2025-05-24', '2025-05-24 13:45:20'),
	(5, 'Daia (1 sachet)', 1000.00, 1, 1000.00, '2025-05-24', '2025-05-24 13:45:26'),
	(6, 'Beras (C4 Super) / kg', 15000.00, 5, 75000.00, '2025-05-24', '2025-05-24 13:45:43'),
	(7, 'Air Mineral Cleo 600 ML', 3000.00, 3, 9000.00, '2025-05-25', '2025-05-25 13:47:27'),
	(8, 'Susu Chocolatos (Per Sachet)', 2500.00, 2, 5000.00, '2025-05-25', '2025-05-25 13:47:36'),
	(9, 'Gula (Gulaku)/kg', 18000.00, 3, 54000.00, '2025-05-25', '2025-05-25 13:47:52'),
	(10, 'Telur/kg', 30000.00, 6, 180000.00, '2025-05-25', '2025-05-25 13:47:58'),
	(11, 'Beras (C4 Super) / kg', 15000.00, 6, 90000.00, '2025-05-26', '2025-05-26 13:49:27'),
	(12, 'Superstar ( per bungkus)', 1500.00, 2, 3000.00, '2025-05-26', '2025-05-26 13:49:33'),
	(13, 'Nextar (per bungkus)', 3000.00, 1, 3000.00, '2025-05-26', '2025-05-26 13:49:37'),
	(14, 'Molto (1 renceng)', 12000.00, 3, 36000.00, '2025-05-26', '2025-05-26 05:07:39'),
	(15, 'Telur/kg', 30000.00, 1, 30000.00, '2025-05-26', '2025-05-26 05:11:37'),
	(16, 'Telur/kg', 30000.00, 3, 90000.00, '2025-05-26', '2025-05-26 05:12:14'),
	(17, 'Susu Hilo ( 1 sachet )', 3500.00, 2, 7000.00, '2025-05-26', '2025-05-26 11:00:48'),
	(18, 'Susu Hilo ( 1 sachet )', 3500.00, 2, 7000.00, '2025-05-26', '2025-05-26 11:02:41'),
	(19, 'Soffel', 500.00, 31, 15500.00, '2025-05-26', '2025-05-26 11:08:05'),
	(21, 'Beras (C4 Super) / kg', 15000.00, 2, 30000.00, '2025-05-26', '2025-05-26 13:58:51'),
	(22, 'Beras (C4 Super) / kg', 15000.00, 10, 150000.00, '2025-05-26', '2025-05-26 13:59:35'),
	(23, 'Beras (C4 Super) / kg', 15000.00, 10, 150000.00, '2025-05-26', '2025-05-26 14:00:00'),
	(24, 'Beras (C4 Super) / kg', 15000.00, 20, 300000.00, '2025-05-26', '2025-05-26 14:00:29'),
	(25, 'A', 2000.00, 1, 2000.00, '2025-05-27', '2025-05-26 19:33:13'),
	(26, 'A', 2000.00, 2, 4000.00, '2025-05-27', '2025-05-26 19:51:18'),
	(27, 'CC', 10000.00, 10, 100000.00, '2025-05-27', '2025-05-26 20:13:11');

-- Dumping structure for table retailese_db.stok_barang
CREATE TABLE IF NOT EXISTS `stok_barang` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `tanggal_kadaluarsa` date NOT NULL,
  `tanggal_masuk` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table retailese_db.stok_barang: ~19 rows (approximately)
INSERT INTO `stok_barang` (`id`, `nama`, `harga`, `jumlah`, `tanggal_kadaluarsa`, `tanggal_masuk`, `created_at`) VALUES
	(1, 'Air Mineral Cleo 600 ML', 3000.00, 11, '2026-10-15', '2025-05-22', '2025-05-22 16:49:56'),
	(2, 'Lifeboy (1 bungkus)', 3500.00, 10, '2026-04-22', '2025-05-22', '2025-05-22 16:51:23'),
	(3, 'Beras (C4 Super) / kg', 15000.00, 80, '2026-07-10', '2025-05-22', '2025-05-22 16:58:13'),
	(4, 'Telur/kg', 30000.00, 12, '2025-05-30', '2025-05-23', '2025-05-22 17:05:15'),
	(5, 'Gula (Gulaku)/kg', 18000.00, 11, '2027-02-19', '2025-05-23', '2025-05-22 17:11:29'),
	(6, 'Nextar (per bungkus)', 3000.00, 14, '2025-06-14', '2025-05-23', '2025-05-22 17:17:04'),
	(7, 'Superstar ( per bungkus)', 1500.00, 6, '2026-02-10', '2025-05-23', '2025-05-22 17:24:15'),
	(8, 'Garam (Kapal) / 250 g', 2800.00, 18, '2028-08-30', '2025-05-23', '2025-05-22 17:32:05'),
	(9, 'Lux (1 bungkus)', 5000.00, 12, '2027-02-04', '2025-05-23', '2025-05-22 17:34:39'),
	(10, 'Wafer Nabati ( per bungkus)', 2500.00, 11, '2025-07-07', '2025-05-23', '2025-05-22 17:50:18'),
	(11, 'Nutri Sari (per sachet)', 1500.00, 22, '2025-09-02', '2025-05-23', '2025-05-22 17:54:22'),
	(12, 'Susu Milo (per sachet)', 3500.00, 14, '2026-03-21', '2025-05-23', '2025-05-22 18:00:39'),
	(13, 'Susu Hilo ( 1 sachet )', 3500.00, 12, '2026-04-14', '2025-05-23', '2025-05-22 18:03:49'),
	(14, 'Susu Chocolatos (Per Sachet)', 2500.00, 10, '2026-04-26', '2025-05-23', '2025-05-22 18:06:02'),
	(15, 'Royco Sapi (1 Sachet)', 500.00, 10, '2026-02-04', '2025-05-23', '2025-05-22 18:08:27'),
	(16, 'Royco Ayam (1 Sachet)', 500.00, 17, '2026-05-02', '2025-05-23', '2025-05-22 18:10:25'),
	(17, 'Daia (1 sachet)', 1000.00, 13, '2027-02-14', '2025-05-23', '2025-05-22 18:11:21'),
	(18, 'BengBeng (1 bungkus)', 2500.00, 4, '2026-02-02', '2025-05-23', '2025-05-22 18:15:26'),
	(19, 'Sunlight', 5000.00, 7, '2026-07-19', '2025-05-23', '2025-05-22 18:17:19');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
