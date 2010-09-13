-- phpMyAdmin SQL Dump
-- version 3.3.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 13, 2010 at 05:04 PM
-- Server version: 5.1.41
-- PHP Version: 5.3.2-1ubuntu4.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `twitter_bookmarks`
--

-- --------------------------------------------------------

--
-- Table structure for table `analyseddata`
--

CREATE TABLE IF NOT EXISTS `analyseddata` (
  `pid` varchar(10) NOT NULL,
  `datetime` varchar(100) NOT NULL,
  `wordfreqexpected` varchar(500) NOT NULL,
  `wordfrequnexpected` varchar(500) NOT NULL,
  `totaltweets` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pid`,`datetime`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `keywords`
--

CREATE TABLE IF NOT EXISTS `keywords` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) NOT NULL,
  `keyword` varchar(200) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

--
-- Table structure for table `programmes`
--

CREATE TABLE IF NOT EXISTS `programmes` (
  `pid` varchar(10) NOT NULL,
  `channel` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `expectedstart` varchar(100) NOT NULL,
  `timediff` int(11) NOT NULL DEFAULT '0',
  `duration` int(11) NOT NULL DEFAULT '0',
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `analysed` tinyint(1) NOT NULL DEFAULT '0',
  `totaltweets` int(11) NOT NULL DEFAULT '0',
  `meantweets` float NOT NULL DEFAULT '0',
  `mediantweets` int(11) NOT NULL DEFAULT '0',
  `modetweets` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `rawdata`
--

CREATE TABLE IF NOT EXISTS `rawdata` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) NOT NULL,
  `datetime` varchar(100) NOT NULL,
  `text` varchar(200) CHARACTER SET utf8 NOT NULL,
  `user` varchar(200) NOT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;
