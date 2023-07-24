-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 24, 2023 at 05:17 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_student`
--

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(100) NOT NULL,
  `f_name` varchar(100) NOT NULL,
  `l_name` varchar(100) NOT NULL,
  `nrc` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `hobby` varchar(100) NOT NULL,
  `gender` varchar(100) NOT NULL,
  `photo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `f_name`, `l_name`, `nrc`, `email`, `phone`, `address`, `city`, `hobby`, `gender`, `photo`) VALUES
(1, 'Isaiah', 'Walton', '5/PFI(N)149717', 'sarah@gmail.com', '5174611313', 'Mayangone', 'Yangon', '', '', 'database.jpg'),
(2, 'Craig', 'Marsh', '12/DHI(N)737084', 'kevin@gmail.com', '743-230-8351', 'Kyauk Myaung', 'Myitkyina', 'reading', 'female', ''),
(3, 'Thomas', 'Coleman', '1/KDO(N)151330', 'rodney@gmail.com', '731.573.7174', 'Sanchaung', 'Mandalay', 'reading', 'female', ''),
(4, 'Scott', 'Johnson', '3/KVB(N)745247', 'joann@gmail.com', '(892)460-6676', 'Tamwe', 'Myitkyina', 'reading', 'male', ''),
(5, 'Michelle', 'Lopez', '8/PVT(N)937727', 'melind@gmail.com', '(510)968-3814', 'Kyauk Myaung', 'Naypyidaw', 'reading', 'male', ''),
(6, 'Michael', 'Arellano', '5/DHS(N)825697', 'amber@gmail.com', '+1-350-748-5204', 'Sanchaung', 'Taunggyi', 'reading', 'female', ''),
(7, 'John', 'Best', '1/YRL(N)110053', 'jeremy@gmail.com', '977.939.3015', 'Kyauk Myaung', 'Myitkyina', 'reading', 'female', ''),
(8, 'Lacey', 'Diaz', '5/PNF(N)341535', 'jorge@gmail.com', '+1-248-737-8091', 'Tamwe', 'Taunggyi', 'reading', 'female', ''),
(9, 'Elaine', 'Flowers', '12/DTL(N)054054', 'kriste@gmail.com', '+1-423-673-4946', 'Mayangone', 'Yangon', 'walking', 'male', ''),
(10, 'Heather', 'Torres', '14/RID(N)456113', 'joseph@gmail.com', '001-920-903-4619', 'Mayangone', 'Yangon', 'reading', 'male', ''),
(11, 'Melanie', 'Benson', '1/CSC(N)869142', 'cassie@gmail.com', '884-603-8165', 'Bahan', 'Yangon', 'walking', 'male', ''),
(12, 'Crystal', 'Johnson', '14/ERP(N)776338', 'laura@gmail.com', '001-360-451-2092', 'Mayangone', 'Mandalay', 'reading', 'female', ''),
(13, 'John', 'Romero', '3/LKH(N)839447', 'alison@gmail.com', '593-515-9695', 'Mayangone', 'Myitkyina', 'walking', 'male', ''),
(14, 'Lisa', 'Bell', '3/GTX(N)325971', 'ryan@gmail.com', '507.882.1935', 'Bahan', 'Myitkyina', 'reading', 'male', ''),
(15, 'Joshua', 'Rios', '14/UKR(N)870244', 'dawn@gmail.com', '4215266831', 'Sanchaung', 'Myitkyina', 'reading', 'female', ''),
(16, 'Kayla', 'Brown', '1/BDS(N)207751', 'thomas@gmail.com', '872.763.7445', 'Bahan', 'Yangon', 'walking', 'male', ''),
(17, 'Nicole', 'Thomas', '14/JSO(N)962316', 'joseph@gmail.com', '001-216-838-7364', 'Sanchaung', 'Yangon', 'walking', 'male', ''),
(18, 'Ryan', 'Humphrey', '12/FNM(N)306756', 'kevin@gmail.com', '2757713174', 'Bahan', 'Taunggyi', 'reading', 'male', ''),
(19, 'Lori', 'Norris', '3/DET(N)640374', 'regina@gmail.com', '408.907.0172', 'Mayangone', 'Yangon', 'reading', 'female', ''),
(20, 'Christopher', 'Burgess', '12/JZI(N)420016', 'meagan@gmail.com', '847.565.6907', 'Bahan', 'Myitkyina', 'reading', 'male', ''),
(21, 'DB', 'MS', '6/MMM(N)009387576', 'db@gmail.com', '0998285767', '1, st township', 'Yangon', 'reading,walking', 'Female', 'database.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` int(100) NOT NULL,
  `maths` varchar(100) NOT NULL,
  `arts` varchar(100) NOT NULL,
  `physics` varchar(100) NOT NULL,
  `year` varchar(100) NOT NULL,
  `student_id` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`id`, `maths`, `arts`, `physics`, `year`, `student_id`) VALUES
(1, '100', '100', '100', '100', 21),
(2, '100', '100', '100', '100', 21);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
