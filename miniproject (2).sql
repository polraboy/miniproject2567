-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 15, 2024 at 06:00 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `miniproject`
--

-- --------------------------------------------------------

--
-- Table structure for table `coffee_menu`
--

CREATE TABLE `coffee_menu` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `coffee_menu`
--

INSERT INTO `coffee_menu` (`id`, `name`, `price`, `description`, `image_path`) VALUES
(8, 'Espresso hot', 45.00, 'ร้อนมากๆ', 'coffee_images/what-is-espresso-765702-hero-03_cropped-ffbc0c7cf45a46ff846843040c8f370c.jpg'),
(12, 'โอเลี้ยง', 20.00, 'โอเลี้ยงยกล้อ ', 'coffee_images/e0873963-0fa0-4aa2-8c17-3d08f259ba78.jpg'),
(13, 'คาปูชิโน่', 50.00, 'ดีด3วัน3คืน', 'coffee_images/640px-Cappuccino_at_Sightglass_Coffee.jpg'),
(14, 'โกโก้', 50.00, 'เย็นนะจ้ะ', 'coffee_images/-769x1024.jpg'),
(15, 'ชาเขียว', 60.00, 'หอมอย่างกับอยู่บนดอย', 'coffee_images/jpg');

-- --------------------------------------------------------

--
-- Table structure for table `completed_orders`
--

CREATE TABLE `completed_orders` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `table_id` varchar(10) NOT NULL,
  `coffee_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `service_type` enum('table','self') NOT NULL,
  `order_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `completed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `completed_orders`
--

INSERT INTO `completed_orders` (`id`, `order_id`, `table_id`, `coffee_id`, `quantity`, `price`, `service_type`, `order_time`, `completed_at`) VALUES
(23, 15, '1', 12, 2, 20.00, 'self', '2024-09-12 06:17:30', '2024-09-13 15:12:02'),
(24, 16, '1', 8, 2, 45.00, 'self', '2024-09-12 06:17:30', '2024-09-13 15:12:02'),
(25, 17, '1', 13, 2, 50.00, 'self', '2024-09-12 06:17:30', '2024-09-13 15:12:02'),
(26, 18, '1', 15, 1, 60.00, 'self', '2024-09-12 06:17:30', '2024-09-13 15:12:02'),
(27, 19, '1', 13, 2, 50.00, 'self', '2024-09-12 06:29:08', '2024-09-13 15:12:02'),
(28, 20, '1', 12, 2, 20.00, 'table', '2024-09-12 06:34:18', '2024-09-13 15:12:02');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `cus_id` int(11) NOT NULL,
  `cus_name` text NOT NULL,
  `cus_username` varchar(24) NOT NULL,
  `cus_password` varchar(12) NOT NULL,
  `cus_phone` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`cus_id`, `cus_name`, `cus_username`, `cus_password`, `cus_phone`) VALUES
(1, 'นาย ชวนากร หมื่นวงษ์', 'polra', 'pp123321', 828143656),
(3, 'chawanakorn changya', 'admin01', 'pp123321', 952203838);

-- --------------------------------------------------------

--
-- Table structure for table `daily_sales`
--

CREATE TABLE `daily_sales` (
  `id` int(11) NOT NULL,
  `sale_date` date NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `details` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `daily_sales`
--

INSERT INTO `daily_sales` (`id`, `sale_date`, `total_amount`, `created_at`, `details`) VALUES
(19, '2024-09-13', 430.00, '2024-09-13 15:12:02', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `table_id` varchar(10) NOT NULL,
  `coffee_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `order_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `service_type` enum('table','self') NOT NULL DEFAULT 'table',
  `status` enum('active','completed') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `table_id`, `coffee_id`, `quantity`, `order_time`, `service_type`, `status`) VALUES
(13, '2', 12, 1, '2024-09-11 04:16:11', 'self', 'active'),
(14, '2', 12, 1, '2024-09-12 04:29:31', 'self', 'active'),
(15, '1', 12, 2, '2024-09-12 06:17:30', 'self', 'completed'),
(16, '1', 8, 2, '2024-09-12 06:17:30', 'self', 'completed'),
(17, '1', 13, 2, '2024-09-12 06:17:30', 'self', 'completed'),
(18, '1', 15, 1, '2024-09-12 06:17:30', 'self', 'completed'),
(19, '1', 13, 2, '2024-09-12 06:29:08', 'self', 'completed'),
(20, '1', 12, 2, '2024-09-12 06:34:18', 'table', 'completed'),
(21, '1', 13, 2, '2024-09-15 15:50:53', 'self', 'active'),
(22, '1', 13, 1, '2024-09-15 15:55:00', 'table', 'active'),
(23, '1', 13, 2, '2024-09-15 15:55:11', 'self', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `tables`
--

CREATE TABLE `tables` (
  `table_id` varchar(10) NOT NULL,
  `table_qrcode` varchar(255) NOT NULL,
  `table_capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tables`
--

INSERT INTO `tables` (`table_id`, `table_qrcode`, `table_capacity`) VALUES
('1', 'http://127.0.0.1:5000/generate_qr/1', 4),
('2', 'http://127.0.0.1:5000/generate_qr/2', 4),
('3', 'http://127.0.0.1:5000/generate_qr/3', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `coffee_menu`
--
ALTER TABLE `coffee_menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `completed_orders`
--
ALTER TABLE `completed_orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `completed_orders_ibfk_1` (`order_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`cus_id`);

--
-- Indexes for table `daily_sales`
--
ALTER TABLE `daily_sales`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sale_date` (`sale_date`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `table_id` (`table_id`),
  ADD KEY `coffee_id` (`coffee_id`);

--
-- Indexes for table `tables`
--
ALTER TABLE `tables`
  ADD PRIMARY KEY (`table_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `coffee_menu`
--
ALTER TABLE `coffee_menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `completed_orders`
--
ALTER TABLE `completed_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `cus_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `daily_sales`
--
ALTER TABLE `daily_sales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `completed_orders`
--
ALTER TABLE `completed_orders`
  ADD CONSTRAINT `completed_orders_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `tables` (`table_id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`coffee_id`) REFERENCES `coffee_menu` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
