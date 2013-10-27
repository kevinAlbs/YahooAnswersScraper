-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 27, 2013 at 03:20 PM
-- Server version: 5.5.32
-- PHP Version: 5.4.6-1ubuntu1.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ya`
--

-- --------------------------------------------------------

--
-- Table structure for table `answer`
--

CREATE TABLE IF NOT EXISTS `answer` (
  `arbitrary_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time_posted` datetime DEFAULT NULL,
  `content` text,
  `upvotes` int(11) DEFAULT NULL,
  `is_best` tinyint(4) DEFAULT NULL,
  `qid` varchar(200) NOT NULL,
  PRIMARY KEY (`arbitrary_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=103242 ;

-- --------------------------------------------------------

--
-- Table structure for table `question`
--

CREATE TABLE IF NOT EXISTS `question` (
  `id` varchar(200) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `subject` text,
  `content` text,
  `datetime` datetime DEFAULT NULL,
  `specific_category` varchar(100) DEFAULT NULL,
  `category_id` varchar(50) DEFAULT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `user_nickname` varchar(200) DEFAULT NULL,
  `num_answers` int(11) DEFAULT NULL,
  `num_comments` int(11) DEFAULT NULL,
  `chosen_answer_id` varchar(100) DEFAULT NULL,
  `chosen_answer_timestamp` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `chosen_answer_award_timestamp` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `category` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
