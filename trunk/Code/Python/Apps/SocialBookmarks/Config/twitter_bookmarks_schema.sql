-- phpMyAdmin SQL Dump
-- version 3.3.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 29, 2010 at 10:37 AM
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
  `timestamp` double NOT NULL,
  `wordfreqexpected` varchar(2000) NOT NULL,
  `wordfrequnexpected` varchar(2000) NOT NULL,
  `totaltweets` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`did`),
  KEY `pid_refs_pid_5901525b` (`pid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=338586 ;

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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=145387 ;

-- --------------------------------------------------------

--
-- Table structure for table `programmes`
--

CREATE TABLE IF NOT EXISTS `programmes` (
  `pid` varchar(10) NOT NULL,
  `channel` varchar(20) NOT NULL,
  `timestamp` double NOT NULL,
  `utcoffset` int(11) NOT NULL DEFAULT '0',
  `timediff` int(11) NOT NULL DEFAULT '0',
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `analysed` tinyint(1) NOT NULL DEFAULT '0',
  `totaltweets` int(11) NOT NULL DEFAULT '0',
  `meantweets` double NOT NULL DEFAULT '0',
  `mediantweets` int(11) NOT NULL DEFAULT '0',
  `modetweets` int(11) NOT NULL DEFAULT '0',
  `stdevtweets` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`pid`,`timestamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `programmes_unique`
--

CREATE TABLE IF NOT EXISTS `programmes_unique` (
  `pid` varchar(10) NOT NULL,
  `title` varchar(200) CHARACTER SET utf8 NOT NULL,
  `duration` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `rawdata`
--

CREATE TABLE IF NOT EXISTS `rawdata` (
  `tweet_id` decimal(22,0) NOT NULL,
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) NOT NULL,
  `timestamp` double NOT NULL,
  `text` varchar(200) CHARACTER SET utf8 NOT NULL,
  `user` varchar(200) NOT NULL,
  `analysed` tinyint(1) NOT NULL DEFAULT '0',
  `programme_position` int(11) NOT NULL,
  PRIMARY KEY (`tid`),
  KEY `ANALYSED` (`analysed`),
  KEY `TweetID` (`tweet_id`),
  KEY `Composite` (`pid`,`timestamp`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1864134 ;

-- --------------------------------------------------------

--
-- Table structure for table `rawtweets`
--

CREATE TABLE IF NOT EXISTS `rawtweets` (
  `tweet_id` decimal(22,0) NOT NULL,
  `tweet_json` varchar(16000) NOT NULL,
  `tweet_stored_seconds` int(11) NOT NULL,
  `tweet_stored_fraction` double NOT NULL,
  PRIMARY KEY (`tweet_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `wordanalysis`
--

CREATE TABLE IF NOT EXISTS `wordanalysis` (
  `wid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) NOT NULL,
  `timestamp` double NOT NULL,
  `word` varchar(200) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `phrase` varchar(200) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT '0',
  `is_keyword` tinyint(1) NOT NULL DEFAULT '0',
  `is_entity` tinyint(1) NOT NULL DEFAULT '0',
  `is_common` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`wid`),
  KEY `Q1` (`pid`,`timestamp`,`word`),
  KEY `Q2` (`pid`,`timestamp`,`phrase`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2472471 ;
