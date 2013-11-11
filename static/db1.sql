-- MySQL dump 10.13  Distrib 5.5.34, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: problemCategory
-- ------------------------------------------------------
-- Server version	5.5.34-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ProCate`
--

DROP TABLE IF EXISTS `ProCate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ProCate` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PID` int(11) DEFAULT NULL,
  `SubCID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `PID` (`PID`),
  KEY `SubCID` (`SubCID`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ProCate`
--

LOCK TABLES `ProCate` WRITE;
/*!40000 ALTER TABLE `ProCate` DISABLE KEYS */;
INSERT INTO `ProCate` VALUES (1,1,1),(2,1,5),(3,1,3),(4,2,1),(5,2,2),(6,3,1),(7,4,1),(8,4,3),(9,4,2),(10,5,10),(11,6,10),(12,6,13),(13,5,11),(14,11,16),(15,15,9);
/*!40000 ALTER TABLE `ProCate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SubCategory`
--

DROP TABLE IF EXISTS `SubCategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SubCategory` (
  `SubCID` int(11) NOT NULL AUTO_INCREMENT,
  `SubCName` varchar(100) DEFAULT NULL,
  `CID` int(11) DEFAULT NULL,
  PRIMARY KEY (`SubCID`),
  KEY `CID` (`CID`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SubCategory`
--

LOCK TABLES `SubCategory` WRITE;
/*!40000 ALTER TABLE `SubCategory` DISABLE KEYS */;
INSERT INTO `SubCategory` VALUES (1,'二分图匹配',1),(2,'最短路',1),(3,'网络流',1),(4,'最小生成树',1),(5,'差分约束',1),(6,'划分型',2),(7,'区间型',2),(8,'最长公共子序列',2),(9,'启发式搜索',3),(10,'广度优先搜索',3),(11,'深度优先搜索',3),(12,'欧几里德定理',4),(13,'组合数学',4),(14,'容斥原理',4),(15,'坐标变换',5),(16,'几何图形的交与并',5),(17,'平面图',1),(18,'置换群',6),(19,'未分类',8);
/*!40000 ALTER TABLE `SubCategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `CID` int(11) NOT NULL AUTO_INCREMENT,
  `CName` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'图论'),(2,'动态规划'),(3,'搜索'),(4,'数论'),(5,'计算几何'),(6,'群论'),(7,'张汝全'),(8,'未分类');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problem`
--

DROP TABLE IF EXISTS `problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problem` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `OJName` varchar(100) DEFAULT NULL,
  `PID` varchar(10) DEFAULT NULL,
  `AddUserID` int(11) DEFAULT NULL,
  `PUrl` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `AddUserID` (`AddUserID`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problem`
--

LOCK TABLES `problem` WRITE;
/*!40000 ALTER TABLE `problem` DISABLE KEYS */;
INSERT INTO `problem` VALUES (1,'hdu','1000',1,'http://acm.hdu.edu.cn/showproblem.php?pid=1000'),(2,'poj','1000',2,'http://poj.org/problem?id=1000'),(3,'hdu','1001',1,'http://acm.hdu.edu.cn/showproblem.php?pid=1001'),(4,'hdu','1010',1,'http://acm.hdu.edu.cn/showproblem.php?pid=1010'),(5,'poj','1010',1,'http://poj.org/problem?id=1010'),(6,'poj','1011',1,'http://poj.org/problem?id=1011'),(7,'hdu','2010',2,'http://acm.hdu.edu.cn/showproblem.php?pid=2010'),(8,'hdu','1014',2,'http://acm.hdu.edu.cn/showproblem.php?pid=1014'),(9,'poj','1111',1,'http://poj.org/problem?id=1111'),(10,'hdu','1322',1,'http://acm.hdu.edu.cn/showproblem.php?pid=1322'),(11,'poj','1304',6,'http://poj.org/problem?id=1304'),(12,'poj','1304',6,'http://poj.org/problem?id=1304'),(13,'poj','1304',6,'http://poj.org/problem?id=1304'),(14,'poj','1304',6,'http://poj.org/problem?id=1304'),(15,'hdu','1305',1,'http://poj.org/problem?id=1305');
/*!40000 ALTER TABLE `problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solution` (
  `SID` int(11) NOT NULL AUTO_INCREMENT,
  `SUrl` varchar(200) DEFAULT NULL,
  `PID` int(11) DEFAULT NULL,
  `AddUserID` int(11) DEFAULT NULL,
  PRIMARY KEY (`SID`),
  KEY `PID` (`PID`),
  KEY `AddUserID` (`AddUserID`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (1,'www.qq.com',4,4),(2,'http://www.baidu.com',1,1),(3,'http://www.1222.com',1,2),(4,'http://www.linux.com',3,3),(5,'www.zrq495.com',2,1),(6,'http://www.zrq495.com',1,2),(7,'www.z.com',2,2),(8,'http://www.zrq495.me',1,6),(9,'http://poj.org/problem?id=1304',11,6),(10,'http://poj.org/problem?id=1304',11,6),(11,'http://poj.org/problem?id=1304',11,6),(12,'http://poj.org/problem?id=1304',11,6),(13,'http://poj.org/problem?id=1305',15,1);
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(100) DEFAULT NULL,
  `Password` varchar(200) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Permission` int(11) DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'zrq495','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','zrq495@gmail.com',2),(2,'zrq','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','zrq1@gmail.com',1),(3,'zp','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','zp@gmail.com',1),(4,'qc','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','qcsb@gmail.com',1),(5,'scf','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','scf@gmail.com',2),(6,'acm','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','acm@gmail.com',1),(7,'wp','4d4aac071a38a60ba39d1c8eadfbd2701bbe3add','wp@gmail.com',2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-31 21:02:57
