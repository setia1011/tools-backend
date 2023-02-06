-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.33 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for db_tools
CREATE DATABASE IF NOT EXISTS `db_tools` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `db_tools`;

-- Dumping structure for table db_tools.alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.alembic_version: ~1 rows (approximately)
DELETE FROM `alembic_version`;
INSERT INTO `alembic_version` (`version_num`) VALUES
	('62f0aff1b5d7');

-- Dumping structure for table db_tools.ques
CREATE TABLE IF NOT EXISTS `ques` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` int(11) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  `question_status` enum('enabled','disabled') NOT NULL DEFAULT 'enabled',
  PRIMARY KEY (`id`),
  KEY `ix_ques_id` (`id`),
  KEY `ix_ques_question_id` (`question_id`),
  KEY `ix_ques_session_id` (`session_id`),
  CONSTRAINT `ques_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `ques_question` (`id`),
  CONSTRAINT `ques_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `ques_session` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.ques: ~2 rows (approximately)
DELETE FROM `ques`;
INSERT INTO `ques` (`id`, `session_id`, `question_id`, `question_status`) VALUES
	(1, 1, 1, 'enabled'),
	(2, 1, 2, 'enabled');

-- Dumping structure for table db_tools.ques_answer
CREATE TABLE IF NOT EXISTS `ques_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `answer` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_ques_answer_answer` (`answer`),
  KEY `ix_ques_answer_id` (`id`),
  KEY `ix_ques_answer_question_id` (`question_id`),
  CONSTRAINT `ques_answer_ibfk_1` FOREIGN KEY (`answer`) REFERENCES `ques_option` (`id`),
  CONSTRAINT `ques_answer_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `ques_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.ques_answer: ~2 rows (approximately)
DELETE FROM `ques_answer`;
INSERT INTO `ques_answer` (`id`, `question_id`, `answer`) VALUES
	(1, 1, 1),
	(2, 2, 3);

-- Dumping structure for table db_tools.ques_category
CREATE TABLE IF NOT EXISTS `ques_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(255) NOT NULL,
  `category_description` text,
  PRIMARY KEY (`id`),
  KEY `ix_ques_category_category` (`category`),
  KEY `ix_ques_category_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.ques_category: ~1 rows (approximately)
DELETE FROM `ques_category`;
INSERT INTO `ques_category` (`id`, `category`, `category_description`) VALUES
	(1, 'Test', 'Test category');

-- Dumping structure for table db_tools.ques_option
CREATE TABLE IF NOT EXISTS `ques_option` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `option` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_ques_option_id` (`id`),
  KEY `ix_ques_option_option` (`option`),
  KEY `ix_ques_option_question_id` (`question_id`),
  CONSTRAINT `ques_option_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `ques_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.ques_option: ~7 rows (approximately)
DELETE FROM `ques_option`;
INSERT INTO `ques_option` (`id`, `question_id`, `option`) VALUES
	(1, 1, 'Option A'),
	(2, 1, 'Option B'),
	(3, 1, 'Option C'),
	(4, 2, 'Option A'),
	(5, 2, 'Option B'),
	(6, 2, 'Option C'),
	(7, 2, 'Option D');

-- Dumping structure for table db_tools.ques_question
CREATE TABLE IF NOT EXISTS `ques_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `question` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_ques_question_category_id` (`category_id`),
  KEY `ix_ques_question_id` (`id`),
  KEY `ix_ques_question_question` (`question`),
  CONSTRAINT `ques_question_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `ques_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.ques_question: ~5 rows (approximately)
DELETE FROM `ques_question`;
INSERT INTO `ques_question` (`id`, `category_id`, `question`) VALUES
	(1, 1, 'Test question 1'),
	(2, 1, 'Test question 2'),
	(3, 1, 'Test question 3'),
	(4, 1, 'Test question 4'),
	(5, 1, 'Test question 4');

-- Dumping structure for table db_tools.ques_session
CREATE TABLE IF NOT EXISTS `ques_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session` varchar(500) NOT NULL,
  `session_description` text,
  PRIMARY KEY (`id`),
  KEY `ix_ques_session_id` (`id`),
  KEY `ix_ques_session_session` (`session`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table db_tools.ques_session: ~1 rows (approximately)
DELETE FROM `ques_session`;
INSERT INTO `ques_session` (`id`, `session`, `session_description`) VALUES
	(1, 'Session 1', 'Session 1 guess');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
