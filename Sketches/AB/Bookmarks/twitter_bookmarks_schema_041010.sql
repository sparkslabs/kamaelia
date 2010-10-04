-- phpMyAdmin SQL Dump
-- version 3.3.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 04, 2010 at 09:59 AM
-- Server version: 5.1.41
-- PHP Version: 5.3.2-1ubuntu4.5

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
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) NOT NULL,
  `datetime` varchar(100) NOT NULL,
  `wordfreqexpected` varchar(500) NOT NULL,
  `wordfrequnexpected` varchar(500) NOT NULL,
  `totaltweets` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`did`),
  KEY `pid_refs_pid_5901525b` (`pid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=50218 ;

-- --------------------------------------------------------

--
-- Table structure for table `keywords`
--

CREATE TABLE IF NOT EXISTS `keywords` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) NOT NULL,
  `keyword` varchar(200) NOT NULL,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `pid_refs_pid_38b0e356` (`pid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=27863 ;

-- --------------------------------------------------------

--
-- Table structure for table `programmes`
--

CREATE TABLE IF NOT EXISTS `programmes` (
  `pid` varchar(10) NOT NULL,
  `channel` varchar(20) NOT NULL,
  `title` varchar(200) CHARACTER SET utf8 NOT NULL,
  `expectedstart` varchar(100) NOT NULL,
  `timediff` int(11) NOT NULL DEFAULT '0',
  `duration` int(11) NOT NULL DEFAULT '0',
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `analysed` tinyint(1) NOT NULL DEFAULT '0',
  `totaltweets` int(11) NOT NULL DEFAULT '0',
  `meantweets` double NOT NULL DEFAULT '0',
  `mediantweets` int(11) NOT NULL DEFAULT '0',
  `modetweets` int(11) NOT NULL DEFAULT '0',
  `stdevtweets` double NOT NULL DEFAULT '0',
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
  `analysed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`),
  KEY `pid_refs_pid_458415f9` (`pid`),
  KEY `ANALYSED` (`analysed`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=357821 ;
