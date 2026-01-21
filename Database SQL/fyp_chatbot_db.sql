/******************************************************************************
 * PROJECT NAME: NLP Chatbot for Zainab Technical Training Institute
 * FILE NAME:    fyp_database.sql
 * AUTHOR:       Muhammad Arslan Akhtar (VUID:BC210414509)
 * DESCRIPTION:  Database Schema and Seed Data for FYP.
 * Contains tables for Courses, Registrations, Schedules, 
 * and Certificates.
 *****************************************************************************/

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+05:00"; -- Set to Pakistan Standard Time

-- --------------------------------------------------------
-- Database Creation
-- --------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `fyp_chatbot_db`;
USE `fyp_chatbot_db`;

-- --------------------------------------------------------
-- Table 1: COURSES
-- Stores static details of all training programs.
-- --------------------------------------------------------
DROP TABLE IF EXISTS `courses`;

CREATE TABLE `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) DEFAULT NULL,
  `duration` varchar(50) DEFAULT NULL,
  `fee` varchar(50) DEFAULT NULL,
  `mode` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table `courses`
INSERT INTO `courses` (`id`, `course_name`, `duration`, `fee`, `mode`, `is_active`) VALUES
(1, 'Python Programming', '4 weeks', '8000 PKR', 'Online', 1),
(2, 'Web Development', '6 weeks', '12000 PKR', 'On Campus', 1),
(3, 'Data Science', '8 weeks', '18000 PKR', 'Hybrid', 1),
(4, 'Graphic Designing', '6 weeks', '10000 PKR', 'Online', 1),
(5, 'MS Office Professional', '3 weeks', '5000 PKR', 'On Campus', 1);

-- --------------------------------------------------------
-- Table 2: SCHEDULES
-- Stores class timings and days for each course.
-- --------------------------------------------------------
DROP TABLE IF EXISTS `schedules`;

CREATE TABLE `schedules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) DEFAULT NULL,
  `days` varchar(100) DEFAULT NULL,
  `timing` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table `schedules`
INSERT INTO `schedules` (`id`, `course_name`, `days`, `timing`) VALUES
(1, 'Python Programming', 'Monday, Wednesday, Friday', '6:00 PM – 8:00 PM'),
(2, 'Web Development', 'Tuesday, Thursday, Saturday', '3:00 PM – 5:00 PM'),
(3, 'Data Science', 'Saturday, Sunday', '11:00 AM – 2:00 PM'),
(4, 'Graphic Designing', 'Monday, Thursday', '4:00 PM – 6:00 PM'),
(5, 'MS Office Professional', 'Monday to Friday', '9:00 AM – 10:30 AM');

-- --------------------------------------------------------
-- Table 3: REGISTRATIONS
-- Captures student enrollment data dynamically.
-- --------------------------------------------------------
DROP TABLE IF EXISTS `registrations`;

CREATE TABLE `registrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `course_selected` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping sample data for table `registrations` (For Demonstration)
INSERT INTO `registrations` (`student_name`, `email`, `phone`, `course_selected`) VALUES
('Arslan', 'arslan@example.com', '03001234567', 'Web Development'),
('Ayesha', 'ayesha@example.com', '03331234567', 'Graphic Designing');

-- --------------------------------------------------------
-- Table 4: CERTIFICATES
-- Stores certification status for students.
-- --------------------------------------------------------
DROP TABLE IF EXISTS `certificates`;

CREATE TABLE `certificates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table `certificates`
INSERT INTO `certificates` (`id`, `email`, `course_name`, `status`) VALUES
(4, 'arslan@example.com', 'Python Programming', 'Completed'),
(5, 'arslan@example.com', 'Web Development', 'In Progress'),
(6, 'student1@example.com', 'Data Science', 'Completed');

COMMIT;