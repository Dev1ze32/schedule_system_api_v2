/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.6.25-MariaDB, for debian-linux-gnu (aarch64)
--
-- Host: localhost    Database: campus_nav
-- ------------------------------------------------------
-- Server version	10.6.25-MariaDB-ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary table structure for view `active_schedules`
--

DROP TABLE IF EXISTS `active_schedules`;
/*!50001 DROP VIEW IF EXISTS `active_schedules`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `active_schedules` AS SELECT
 1 AS `declaration_id`,
  1 AS `faculty_id`,
  1 AS `faculty_name`,
  1 AS `email`,
  1 AS `department`,
  1 AS `room_id`,
  1 AS `building_name`,
  1 AS `room_name`,
  1 AS `floor_number`,
  1 AS `subject_code`,
  1 AS `day_of_week`,
  1 AS `time_start`,
  1 AS `time_end`,
  1 AS `declaration_status`,
  1 AS `semester_id`,
  1 AS `semester_name`,
  1 AS `semester_code`,
  1 AS `academic_year`,
  1 AS `semester_active`,
  1 AS `semester_locked` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `admin_login`
--

DROP TABLE IF EXISTS `admin_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `username` (`username`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `admin_login_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`admin_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_login`
--

LOCK TABLES `admin_login` WRITE;
/*!40000 ALTER TABLE `admin_login` DISABLE KEYS */;
INSERT INTO `admin_login` VALUES (1,1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',1,'2026-04-06 07:37:40'),(3,9,'ms.jhoana','e83bbbcc22fb6eb9fd77212a8edaa66d3a9430694a29fb2975ef151e53ee6476',1,'2026-03-29 15:09:32'),(4,10,'dell69','7bbf789eb68815ea37e3d99fbe42f6fdcb7ec7527e0a150921bf7b0f0b19a056',1,NULL);
/*!40000 ALTER TABLE `admin_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'System Admin','admin@school.edu','2026-01-21 10:27:00'),(9,'Jhoanaliz Gaile A. Labitigan','labitiganjhoanalizgaile01@gmail.com','2026-03-29 13:09:26'),(10,'wendell pogi','dell@edu.ph','2026-04-02 02:29:30');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int(11) NOT NULL AUTO_INCREMENT,
  `faculty_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`faculty_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (28,'Aldrin Soriano','asoriano@gmail.com','COE','2026-02-28 11:39:56'),(29,'Carlo Cimacio','ccmicacio@gmail.com','COE','2026-02-28 11:40:25'),(32,'Juanito M. Bunag III','bunagjuanito82@gmail.com','COE','2026-03-22 10:39:16'),(33,'Ej Khyle Culabat','culabatej@gmail.com','COE','2026-03-22 10:45:46'),(34,'Jhoanaliz Gaile A. Labitigan','labitiganjhoanalizgaile01@gmail.com','COE','2026-03-27 11:44:35'),(35,'Iesha Loisse T. Servo','servoieshaloisse54@gmail.com','COE','2026-03-28 07:48:54'),(36,'Rayelle Anjelie A. Bariring','bariringrayelle53@gmail.com','COE','2026-03-28 08:03:01'),(37,'Divina P. Abelardo','abelardodivina@gmail.com','CAS','2026-03-28 08:05:55'),(38,'Patrice G. Aguillo','aguillopatrice@gmail.com','CAS','2026-03-28 08:07:06'),(39,'Araceli B. Paster','pasteraraceli@gmail.com','CAS','2026-03-28 08:08:02'),(40,'Jerome F. Villadares','villadaresjerome@gmail.com','CAS','2026-03-28 08:09:05'),(41,'Pamela Joy O. Celimen','celimenpamela@gmail.com','CAS','2026-03-28 08:10:01'),(42,'Liann Paula H. Ortiz','ortizliann@gmail','CAS','2026-03-28 08:12:06'),(43,'Edgardo C. Salazar','salazaredgardo@gmail.com','CAS','2026-03-28 08:14:54'),(44,'Arjane Mae L. Monterde','monterdearjane@gmail.com','CAS','2026-03-28 08:16:35'),(45,'Ma. Gloria G. Greganda','greganadagloria@gmail.com','CAS','2026-03-28 08:17:49'),(46,'Hanzen M. Reyes','reyeshanzen@gmail.com','CAS','2026-03-28 08:18:41'),(47,'Marilou R. Tayao','tayaomarilou@gmail.com','CAS','2026-03-28 08:20:35'),(48,'Alicia Clarita G. De Vergara','devergaraalicia@gmail.com','CAS','2026-03-28 08:23:05'),(49,'Joniel S. Ceribito','ceribitojoniel@gmail.com','CAS','2026-03-28 08:28:35'),(51,'Bon Jovi D. Villarama','villaramabon@gmail.com','COE','2026-03-28 08:31:43'),(52,' Daryl Louge F. Tolentino','tolentinodaryl@gmail.com','COE','2026-03-28 08:33:58'),(53,'Bernie Domingo','domingobernie@gmail.com','COE','2026-03-28 08:54:36'),(55,'Wendell Dave Anciso','wendelldaveanciso@gmail.com','COE','2026-03-29 13:08:10'),(56,'wendell anciso','dell@pnc.edu','COE','2026-04-02 02:28:34'),(57,'Mary Grace P. Beaño','mgbeano@gmail.com','COE','2026-04-06 05:02:51'),(58,'Janus H. Perez','janusperez@gmail.com','COE','2026-04-06 05:06:31'),(60,'Juancho G. Aragon','juanchoaragon@gmail.com','COE','2026-04-06 06:32:09'),(61,'Ericson Mandayo','mandayo@gmail.com','COE','2026-04-06 07:07:35');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_login`
--

DROP TABLE IF EXISTS `faculty_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `faculty_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `password_salt` varchar(64) NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `failed_attempts` int(11) DEFAULT 0,
  `locked_until` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `username` (`username`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `faculty_login_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_login`
--

LOCK TABLES `faculty_login` WRITE;
/*!40000 ALTER TABLE `faculty_login` DISABLE KEYS */;
INSERT INTO `faculty_login` VALUES (15,28,'asoriano','1a35b990648e537b2871ef9decc4f25fae1390aad06970e231725efa4ca0cf6e','442015d21c6f7d59c4955e1a0a9ac516',1,0,NULL,'2026-04-02 10:30:27','2026-02-28 11:39:57','2026-04-02 10:30:27'),(16,29,'ccimacio','1092d2fcb1508278f6601d734143d60d20801176247780a8d25c5a129781501d','cc1022f93bf231497963f6128de0ce03',1,0,NULL,'2026-04-10 10:01:41','2026-02-28 11:40:25','2026-04-10 10:01:41'),(19,32,'third','0e6e8f9b2ac93af20b2c09bdbc35ac260e61a28fee5b186e42c82997f0102c2e','bd2647e5a5293b51d9950a032da655ad',1,0,NULL,'2026-03-28 08:14:08','2026-03-22 10:39:16','2026-03-28 08:14:08'),(20,33,'skadi','15e95807bae65db900e7901388cee2cfd35389ec2c5690b9dceba6826958e518','9fd357ade75bb5c4d06d86722cc83ebd',1,0,NULL,'2026-03-22 11:28:21','2026-03-22 10:45:46','2026-03-22 11:28:21'),(21,34,'ms.jhoana','c50f3ccc650e321b410b37bd90390455567a3db2ee315b74b9814b38ab3475fd','794dea303284bf7ea181f017e8f625b6',1,0,NULL,'2026-04-10 09:58:58','2026-03-27 11:44:35','2026-04-10 09:58:58'),(22,35,'ms.ishang','9b807d3ffb413a8175bb7418300022fd02f1daaaf8866e2c2d690217f4019f4c','3e2618b6919c0452dc906d827eb7b8f9',1,0,NULL,'2026-04-06 02:25:18','2026-03-28 07:48:54','2026-04-06 02:25:18'),(23,36,'ms.rayelle','a8b03ecf9ea15c2b9234925475df845089853a78c1e4f6d02be1d8cf345d7503','69cbed1580122c2a58051b79bcb73644',1,0,NULL,NULL,'2026-03-28 08:03:01','2026-03-28 08:03:01'),(24,37,'ms.divina','01c08fcbb822e49d95032cb9128275e7526097263c00ccd3e8ebce0534741f5e','9f3124cd0cca2e4215618c018dfef8e6',1,0,NULL,'2026-04-06 03:18:14','2026-03-28 08:05:55','2026-04-06 03:18:14'),(25,38,'ms.patrice','2bd5e7aa460fcff3b9141a320106dbd6346e84b2b31695eea0f6717e20754a92','b91b0a0e523e3fb2e5da5309abe5b494',1,0,NULL,'2026-04-06 03:12:06','2026-03-28 08:07:06','2026-04-06 03:12:06'),(26,39,'ms.araceli','4e1883d5822ee1aa5af10d191a8b9bd8acbbd14c29290bb8482b378f1f2be581','3a05fbb124df50ec67803aed56feffe6',1,0,NULL,'2026-04-06 03:36:02','2026-03-28 08:08:02','2026-04-06 03:36:02'),(27,40,'mr.jerome','306fedf510e6b8d777a5c292bf558b112e84258ad122ba021a1858a67fede0ef','39ec8ec03627e89ad7b19a0ba56efe8d',1,0,NULL,'2026-04-06 04:40:48','2026-03-28 08:09:05','2026-04-06 04:40:48'),(28,41,'ms.pamela','f03387b7e73db92da54a31ef8838d4bcd0d6c7ad00d8384f111e8e128b48e6c1','b80235ff7ccc50ad11d9aaee251f1972',1,0,NULL,'2026-04-06 04:37:36','2026-03-28 08:10:01','2026-04-06 04:37:36'),(29,42,'ms.liann','42ab315d34481407de281d4b12b4a4c7fb6eb593c23d2ccca223b5689fc7f57f','b0bcbeaf7e51e2037fc50369d60de7ab',1,0,NULL,'2026-04-06 03:36:28','2026-03-28 08:12:06','2026-04-06 03:36:28'),(30,43,'mr.edgardo','7b0197d7cb83434f8d3ca503801c4a03cb62d8f812f49fc98f3052d87548dd39','ef568741dff98c87cfd4ce40371c902e',1,0,NULL,'2026-04-06 02:30:22','2026-03-28 08:14:54','2026-04-06 02:30:22'),(31,44,'ms.arjane','2909cb34bac8fdf55a1a9b27c27bc05b9e8525c74b3b8474c485b8a43099a5f4','3f7b7d0d4207a78b18f7c18020a7cb1a',1,0,NULL,'2026-04-06 03:43:13','2026-03-28 08:16:36','2026-04-06 03:43:13'),(32,45,'ms.gloria','b8a27ac5c160f7fa056414185b72cb1907b79959f75e186bc1b659ca4f01e117','28a2c0807f7b50d19dd12176b74b857d',1,0,NULL,'2026-04-06 02:39:44','2026-03-28 08:17:49','2026-04-06 02:39:44'),(33,46,'ms.hanzen','14846c0850f4f64499b06d9151574bb3d36d3a9e46ed53b007fe9d76fc884006','e4852af8573a687cc2e5a31d6c6d4cd5',1,0,NULL,'2026-04-06 02:32:18','2026-03-28 08:18:41','2026-04-06 02:32:18'),(34,47,'ms.marilou','a958210f53f710ec5aa2a40cf6001a0f89bfed4cef5d9f6417183fdefb770d7b','6cd2ce2f5147f3edf8cdfc34bf314db2',1,0,NULL,'2026-04-06 02:42:33','2026-03-28 08:20:36','2026-04-06 02:42:33'),(35,48,'ms.alicia','b2c65dd08cfad03bf2fe0ad75eb8474bbb62fee24012c1a9a643b1fa1ea9b75e','29be38a604eb5a8de1c4c080ca80bcbf',1,0,NULL,'2026-04-06 03:45:47','2026-03-28 08:23:05','2026-04-06 03:45:47'),(36,49,'mr.joniel','6e3ce09e1c43e5d2bbcebcb7dfb652d66c514f67d55512137a90b3c9e8db7bf0','cf22a730604ed360e748b70c469db10c',1,0,NULL,'2026-04-06 02:33:13','2026-03-28 08:28:36','2026-04-06 02:33:13'),(38,51,'mr.bonjovi','32b28f323ed49fa83cbe8cef25556cdf1fc29a5694221456e13a5751bfee44a6','656d347822b0b5d7a05417fe06bc6fe1',1,1,NULL,'2026-04-06 07:13:56','2026-03-28 08:31:43','2026-04-06 23:30:35'),(39,52,'mr.daryl','e35225d8f83d72372e409d72055b7ed01b8477c90bdfa3e2ccc4c81c61dfc905','8ce45a25db0fc9559a242c052fb32d9d',1,0,NULL,'2026-04-06 02:32:13','2026-03-28 08:33:58','2026-04-06 02:32:13'),(40,53,'mr.bernie','32579cc8e93171195a44550ba153d65c258963d5fb2ee13d8ef55cbcbe5908bb','ffbdf812224e8f1c2461da3b8dcd4735',1,0,NULL,'2026-04-06 23:30:47','2026-03-28 08:54:36','2026-04-06 23:30:47'),(42,55,'mr.wendell','eba1fa72207bd4337362748e2c618ed5234d669ce2064acebbec23671d93666b','c0f3decd9eb665be71ca6f915399d4b1',1,0,NULL,NULL,'2026-03-29 13:08:10','2026-03-29 13:08:10'),(43,56,'dell32','0f507202ebedb03faa47491c3f5f26db26a0aff1710b1542dcd312c52a17403d','d14214041c26e24f82603cf2fbe3b8b5',1,0,NULL,'2026-04-02 10:31:20','2026-04-02 02:28:34','2026-04-02 10:31:20'),(44,57,'ms.grace','8e092a73d486a62c7116355a025a49b25f81c418e8deb883169f74dc013b7771','0de6a1f14dd2673aad93b917f839265a',1,0,NULL,'2026-04-06 05:12:16','2026-04-06 05:02:51','2026-04-06 05:12:16'),(45,58,'ms.janus','fbd87117340c05d8629952a7da81cd5c23000502c13f21edf1fca3a512756380','1b44f3356d9446ebb0b64d219cf81de9',1,0,NULL,'2026-04-06 23:59:08','2026-04-06 05:06:31','2026-04-06 23:59:08'),(47,60,'mr.juancho','17bc170252997c7269a9d64cb3b2f8c7d07b315a088cf8f4884467fb2ee6daba','028a3fbdac9b817c4dfe4441732af86b',1,0,NULL,'2026-04-06 06:33:06','2026-04-06 06:32:09','2026-04-06 06:33:06'),(48,61,'mr.ericson','c865d1cf1508396853f06ecda5797ee0bf9c85ea771fdba9e18ea9c3ee632671','8297ccf6469aaf95da949373ff24d4e9',1,0,NULL,'2026-04-06 07:38:42','2026-04-06 07:07:35','2026-04-06 07:38:42');
/*!40000 ALTER TABLE `faculty_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `faculty_schedule_summary`
--

DROP TABLE IF EXISTS `faculty_schedule_summary`;
/*!50001 DROP VIEW IF EXISTS `faculty_schedule_summary`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `faculty_schedule_summary` AS SELECT
 1 AS `faculty_id`,
  1 AS `faculty_name`,
  1 AS `department`,
  1 AS `semester_id`,
  1 AS `semester_name`,
  1 AS `total_declarations`,
  1 AS `active_count`,
  1 AS `pending_count`,
  1 AS `cancelled_count`,
  1 AS `first_upload`,
  1 AS `last_upload` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `faculty_id` int(11) DEFAULT NULL,
  `action_type` varchar(50) DEFAULT NULL,
  `related_id` int(11) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `search_timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`log_id`),
  KEY `faculty_id` (`faculty_id`),
  KEY `idx_logs_action` (`action_type`,`search_timestamp`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,NULL,'semester_activation',10000,'Activated semester: Spring 2025. 1 declarations changed to Posted.','2026-01-18 19:44:55'),(2,NULL,'semester_activation',10001,'Activated semester: 1st semester 2025-2026. 0 declarations changed to Posted.','2026-01-18 19:52:21'),(3,NULL,'semester_activation',10004,'Activated semester: 1st sem. 1 declarations changed to Posted.','2026-01-18 21:02:52'),(4,NULL,'semester_activation',10005,'Activated semester: 1st semester. 2 declarations changed to Posted.','2026-01-18 21:09:37'),(5,NULL,'semester_activation',10006,'Activated semester: 1st semester. 3 declarations changed to Active.','2026-01-20 11:44:31'),(6,NULL,'semester_activation',10008,'Activated semester: 1st semester. 1 declarations changed to Active.','2026-01-22 20:14:10');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `building_name` varchar(255) NOT NULL,
  `room_name` varchar(255) NOT NULL,
  `floor_number` int(11) NOT NULL,
  PRIMARY KEY (`room_id`),
  UNIQUE KEY `room_number` (`room_name`)
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (1,'Main Building','Comlab 1',1),(2,'Main Building','Comlab 2',1),(3,'Main Building','Comlab 3',1),(4,'Main Building','Comlab 4',2),(5,'Main Building','Ergonomics Laboratory',2),(6,'Main Building','Digital Laboratory',2),(7,'Main Building','Network Laboratory',2),(8,'Main Building','Microbiology Parasitology Laboratory',2),(9,'Main Building','301',3),(10,'Main Building','302',3),(11,'Main Building','303',3),(12,'Main Building','304',3),(13,'Main Building','305',3),(14,'Main Building','306',3),(15,'Main Building','307',3),(16,'Main Building','308',3),(17,'Main Building','309',3),(18,'Main Building','310',3),(19,'Main Building','311',3),(20,'Main Building','312',3),(21,'Main Building','313',3),(22,'Main Building','314',3),(23,'Main Building','315',3),(24,'Main Building','316',3),(25,'Main Building','317',3),(26,'Main Building','318',3),(27,'Main Building','319',3),(28,'Main Building','Psychological Laboratory (320)',3),(29,'Main Building','321',3),(30,'Main Building','322',3),(148,'Bagong Cabuyao Hall','BCH101',1),(149,'Bagong Cabuyao Hall','BCH102',1),(150,'Bagong Cabuyao Hall','BCH103',1),(151,'Bagong Cabuyao Hall','BCH104',1),(152,'Bagong Cabuyao Hall','BCH105',1),(153,'Bagong Cabuyao Hall','BCH106',1),(154,'Bagong Cabuyao Hall','BCH107',1),(155,'Bagong Cabuyao Hall','BCH108',1),(156,'Bagong Cabuyao Hall','BCH201',2),(157,'Bagong Cabuyao Hall','BCH202',2),(158,'Bagong Cabuyao Hall','BCH203',2),(159,'Bagong Cabuyao Hall','BCH204',2),(160,'Bagong Cabuyao Hall','BCH205',2),(161,'Bagong Cabuyao Hall','BCH206',2),(162,'Bagong Cabuyao Hall','BCH207',2),(163,'Bagong Cabuyao Hall','BCH208',2),(164,'Bagong Cabuyao Hall','BCH209',2),(165,'Bagong Cabuyao Hall','BCH210',2),(166,'Bagong Cabuyao Hall','BCH301',3),(167,'Bagong Cabuyao Hall','BCH302',3),(168,'Bagong Cabuyao Hall','BCH303',3),(169,'Bagong Cabuyao Hall','BCH304',3),(170,'Bagong Cabuyao Hall','BCH305',3),(171,'Bagong Cabuyao Hall','BCH306',3),(172,'Bagong Cabuyao Hall','BCH307',3),(173,'Bagong Cabuyao Hall','BCH308',3),(174,'Bagong Cabuyao Hall','BCH309',3),(175,'Bagong Cabuyao Hall','BCH310',3),(176,'Bagong Cabuyao Hall','BCH401',4),(177,'Bagong Cabuyao Hall','BCH402',4),(178,'Bagong Cabuyao Hall','BCH403',4),(179,'Bagong Cabuyao Hall','BCH404',4),(180,'Bagong Cabuyao Hall','BCH405',4),(181,'Bagong Cabuyao Hall','BCH406',4),(182,'Bagong Cabuyao Hall','BCH407',4),(183,'Bagong Cabuyao Hall','BCH408',4),(184,'Bagong Cabuyao Hall','BCH409',4),(185,'Bagong Cabuyao Hall','BCH410',4),(186,'Bagong Cabuyao Hall','BCH501',5),(187,'Bagong Cabuyao Hall','BCH502',5),(188,'Bagong Cabuyao Hall','BCH503',5),(189,'Bagong Cabuyao Hall','BCH504',5),(190,'Bagong Cabuyao Hall','BCH505',5),(191,'Bagong Cabuyao Hall','BCH506',5),(192,'Bagong Cabuyao Hall','BCH507',5),(193,'Bagong Cabuyao Hall','BCH508',5),(194,'Bagong Cabuyao Hall','BCH509',5),(195,'Bagong Cabuyao Hall','BCH510',5),(197,'Main Building','N/A',1),(198,'Nursing Building','University Health Dept',1),(199,'Nursing Building','Anatomy Lab',1),(200,'Nursing Building','Records Management Office/University Library',2),(201,'Nursing Building','Nursing Skills Lab',3),(202,'Nursing Building','Chemistry Lab',4),(203,'Nursing Building','Biochemistry Lab',4);
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `semester_id` int(11) NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(50) NOT NULL,
  `semester_code` varchar(20) NOT NULL,
  `academic_year` varchar(20) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_active` tinyint(1) DEFAULT 0,
  `is_locked` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `activated_at` datetime DEFAULT NULL,
  `deactivated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`semester_id`),
  UNIQUE KEY `semester_code` (`semester_code`),
  KEY `idx_active` (`is_active`),
  KEY `idx_dates` (`start_date`,`end_date`),
  KEY `idx_year` (`academic_year`),
  CONSTRAINT `chk_dates` CHECK (`end_date` > `start_date`)
) ENGINE=InnoDB AUTO_INCREMENT=10093 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (9999,'Legacy Archive','LEGACY-000','2020-2025','2020-01-01','2025-12-31',0,1,'2026-01-18 17:16:09',NULL,NULL),(10091,'asd','asd','asd','2026-04-02','2026-09-02',0,0,'2026-04-02 10:30:20',NULL,NULL),(10092,'First Semester 2026','1-2026','2026-2027','2026-08-03','2027-01-02',0,0,'2026-04-06 02:23:26',NULL,NULL);
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester_audit_log`
--

DROP TABLE IF EXISTS `semester_audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester_audit_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `semester_id` int(11) NOT NULL,
  `action` varchar(50) NOT NULL,
  `performed_by` int(11) DEFAULT NULL,
  `performed_at` datetime DEFAULT current_timestamp(),
  `notes` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `idx_semester` (`semester_id`),
  KEY `idx_action` (`action`),
  KEY `idx_performed_at` (`performed_at`),
  KEY `fk_audit_faculty` (`performed_by`),
  CONSTRAINT `fk_audit_faculty` FOREIGN KEY (`performed_by`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_audit_semester` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester_audit_log`
--

LOCK TABLES `semester_audit_log` WRITE;
/*!40000 ALTER TABLE `semester_audit_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `semester_audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_declaration`
--

DROP TABLE IF EXISTS `work_declaration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_declaration` (
  `declaration_id` int(11) NOT NULL AUTO_INCREMENT,
  `faculty_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `semester_id` int(11) NOT NULL,
  `subject_code` varchar(50) DEFAULT NULL,
  `class_section` varchar(50) DEFAULT NULL,
  `day_of_week` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time NOT NULL,
  `declaration_status` enum('Pending','Active','Rejected') DEFAULT 'Pending',
  `is_cancelled` tinyint(1) DEFAULT 0,
  `cancellation_reason` text DEFAULT NULL,
  `uploaded_at` datetime DEFAULT current_timestamp(),
  `last_modified_at` datetime DEFAULT NULL,
  `last_modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`declaration_id`),
  KEY `fk_declaration_modifier` (`last_modified_by`),
  KEY `idx_declaration_status` (`declaration_status`,`semester_id`),
  KEY `idx_declaration_day` (`day_of_week`,`time_start`),
  KEY `idx_declaration_faculty_semester` (`faculty_id`,`semester_id`),
  KEY `idx_declaration_room_semester` (`room_id`,`semester_id`),
  KEY `idx_declaration_uploaded` (`uploaded_at`),
  KEY `idx_semester_work` (`semester_id`),
  CONSTRAINT `fk_declaration_modifier` FOREIGN KEY (`last_modified_by`) REFERENCES `faculty` (`faculty_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_declaration_semester` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`),
  CONSTRAINT `work_declaration_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE,
  CONSTRAINT `work_declaration_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2509 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_declaration`
--

LOCK TABLES `work_declaration` WRITE;
/*!40000 ALTER TABLE `work_declaration` DISABLE KEYS */;
INSERT INTO `work_declaration` VALUES (2204,28,27,10091,'PSM112','3PSY-D','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2205,28,197,10091,'Consultation Hours','N/A','Monday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2206,28,197,10091,'Research','N/A','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2207,28,27,10091,'PSM112','3PSY-C','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2208,28,27,10091,'PSM113','3PSY-A','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2209,28,197,10091,'Com.  Extension Hours','N/A','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2210,28,187,10091,'SMF119','3SEDF-A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2211,28,153,10091,'SMF119','3SEDF-B','Wednesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2212,28,197,10091,'Consultation Hours','N/A','Wednesday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2213,28,197,10091,'Quasi Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2214,28,27,10091,'PSM112','3PSY-B','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2215,28,27,10091,'PSM113','3PSY-B','Thursday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2216,28,197,10091,'Break','N/A','Thursday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2217,28,197,10091,'Quasi Hours','N/A','Thursday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2218,28,27,10091,'PSM112','3PSY-A','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2219,28,15,10091,'PSM112','3PSY-E','Friday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2220,28,197,10091,'Break','N/A','Friday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2221,28,197,10091,'Quasi Hours','N/A','Friday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:30:50',NULL,NULL),(2222,34,171,10091,'PSM108','2PSY-B','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2223,34,171,10091,'PSM108','2PSY-B','Monday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2224,34,171,10091,'PSM108','2PSY-A','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2225,34,171,10091,'PSM108','2PSY-A','Tuesday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2226,34,197,10091,'Research','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2227,34,197,10091,'Consultation Hours','N/A','Wednesday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2228,34,197,10091,'Com.  Extension Hours','N/A','Wednesday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2229,34,197,10091,'Consultation Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2230,34,171,10091,'PSM108','2PSY-C','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2231,34,171,10091,'PSM108','2PSY-C','Thursday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2232,34,197,10091,'Quasi Hours','N/A','Thursday','16:00:00','17:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2233,34,14,10091,'PSE104','3PSY-F','Thursday','17:00:00','20:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2234,34,197,10091,'Quasi Hours','N/A','Friday','07:00:00','15:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2235,34,197,10091,'Consultation Hours','N/A','Friday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:03',NULL,NULL),(2236,35,173,10091,'PSM107','2PSY-C','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2237,35,173,10091,'PSM107','2PSY-C','Monday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2238,35,197,10091,'Consultation Hours','N/A','Tuesday','07:00:00','11:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2239,35,197,10091,'Break','N/A','Tuesday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2240,35,197,10091,'Quasi Hours','N/A','Tuesday','12:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2241,35,197,10091,'Research Hours','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2242,35,197,10091,'Break','N/A','Wednesday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2243,35,197,10091,'Com. Extension Hours','N/A','Wednesday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2244,35,197,10091,'Quasi Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2245,35,173,10091,'PSM107','2PSY-B','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2246,35,173,10091,'PSM107','2PSY-B','Thursday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2247,35,173,10091,'PSM107','2PSY-A','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2248,35,173,10091,'PSM107','2PSY-A','Friday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:16',NULL,NULL),(2249,56,197,10091,'Consultation Hours','N/A','Monday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:31:26',NULL,NULL),(2250,56,172,10091,'PSM108','1PSY-A','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:26',NULL,NULL),(2251,56,171,10091,'PSM106','2PSY-A','Monday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-02 10:31:26',NULL,NULL),(2252,56,197,10091,'Consultation Hours','N/A','Tuesday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:31:26',NULL,NULL),(2253,56,172,10091,'PSM109','1PSY-B','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:26',NULL,NULL),(2254,56,171,10091,'PSM106','2PSY-A','Tuesday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-02 10:31:26',NULL,NULL),(2255,56,15,10091,'PSM113','3PSY-E','Friday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:27',NULL,NULL),(2256,56,171,10091,'PSM106','2PSY-A','Friday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-02 10:31:27',NULL,NULL),(2257,56,14,10091,'PSE106','4PSY-A','Saturday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-02 10:31:27',NULL,NULL),(2258,56,14,10091,'PSE106','4PSY-B','Saturday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-02 10:31:27',NULL,NULL),(2259,56,14,10091,'PSE106','4PSY-A','Saturday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-02 10:31:27',NULL,NULL),(2273,43,27,10092,'PSM112','3PSY-D','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2274,43,197,10092,'Consultation Hours','N/A','Monday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2275,43,197,10092,'Research','N/A','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2276,43,27,10092,'PSM112','3PSY-C','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2277,43,27,10092,'PSM113','3PSY-A','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2278,43,197,10092,'Com.  Extension Hours','N/A','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2279,43,187,10092,'SMF119','3SEDF-A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2280,43,153,10092,'SMF119','3SEDF-B','Wednesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2281,43,197,10092,'Consultation Hours','N/A','Wednesday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2282,43,197,10092,'Quasi Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2283,43,27,10092,'PSM112','3PSY-B','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2284,43,27,10092,'PSM113','3PSY-B','Thursday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2285,43,197,10092,'Break','N/A','Thursday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2286,43,197,10092,'Quasi Hours','N/A','Thursday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2287,43,27,10092,'PSM112','3PSY-A','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2288,43,15,10092,'PSM112','3PSY-E','Friday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2289,43,197,10092,'Break','N/A','Friday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2290,43,197,10092,'Quasi Hours','N/A','Friday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:30:42',NULL,NULL),(2291,46,16,10092,'PSE102','3PSY-C','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2292,46,16,10092,'PSM104','1PSY-B','Monday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2293,46,197,10092,'Break','N/A','Monday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2294,46,197,10092,'Quasi Hours','N/A','Monday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2295,46,16,10092,'PSE102','3PSY-D','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2296,46,16,10092,'PSM104','1PSY-A','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2297,46,197,10092,'Break','N/A','Tuesday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2298,46,197,10092,'Quasi Hours','N/A','Tuesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2299,46,197,10092,'Consultation Hours','N/A','Wednesday','07:00:00','11:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2300,46,197,10092,'Break','N/A','Wednesday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2301,46,197,10092,'Research','N/A','Wednesday','12:00:00','15:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2302,46,197,10092,'Quasi Hours','N/A','Wednesday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2303,46,16,10092,'PSE102','3PSY-A','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2304,46,16,10092,'PSE102','3PSY-E','Thursday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2305,46,197,10092,'Break','N/A','Thursday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2306,46,197,10092,'Quasi Hours','N/A','Thursday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2307,46,16,10092,'PSE102','3PSY-B','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2308,46,197,10092,'Com.  Extension Hours','N/A','Friday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2309,46,197,10092,'Break','N/A','Friday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2310,46,197,10092,'Quasi Hours','N/A','Friday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:32:36',NULL,NULL),(2311,52,9,10092,'CPP106','2CPEA','Monday','07:30:00','10:00:00','Pending',0,NULL,'2026-04-06 02:36:07',NULL,NULL),(2312,52,10,10092,'Research','N/A','Monday','10:00:00','11:30:00','Pending',0,NULL,'2026-04-06 02:36:07',NULL,NULL),(2313,52,11,10092,'CPP106','2CPEB','Tuesday','10:00:00','11:30:00','Pending',0,NULL,'2026-04-06 02:36:07',NULL,NULL),(2314,52,12,10092,'CPP117','4CPEA','Wednesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:36:07',NULL,NULL),(2315,52,174,10092,'CPE103','3CPEA','Thursday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 02:36:07',NULL,NULL),(2316,52,159,10092,'CPP101','2CPEA','Friday','08:00:00','11:00:00','Pending',0,NULL,'2026-04-06 02:36:07',NULL,NULL),(2317,49,197,10092,'Consultation Hours','N/A','Monday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:39:03',NULL,NULL),(2318,49,172,10092,'PSM102','1PSY-A','Monday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 02:39:03',NULL,NULL),(2319,49,197,10092,'Consultation Hours','N/A','Tuesday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:39:03',NULL,NULL),(2320,49,172,10092,'PSM102','1PSY-A','Tuesday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 02:39:03',NULL,NULL),(2321,49,16,10092,'PSM102','1PSY-A','Saturday','07:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:39:03',NULL,NULL),(2322,49,16,10092,'PSM102','1PSY-A','Saturday','13:00:00','19:00:00','Pending',0,NULL,'2026-04-06 02:39:03',NULL,NULL),(2323,45,15,10092,'ANA101','1PSY-B','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2324,45,15,10092,'ENV101','3PSY-A','Monday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2325,45,197,10092,'Break','N/A','Monday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2326,45,197,10092,'Quasi Hours','N/A','Monday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2327,45,15,10092,'ANA101','1PSY-A','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2328,45,15,10092,'ENV101','3PSY-B','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2329,45,197,10092,'Break','N/A','Tuesday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2330,45,197,10092,'Quasi Hours','N/A','Tuesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2331,45,197,10092,'Consultation Hours','N/A','Wednesday','07:00:00','11:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2332,45,197,10092,'Com.  Extension Hours','N/A','Wednesday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2333,45,197,10092,'Quasi Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2334,45,150,10092,'ANA101','1PSY-A','Thursday','07:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2335,45,197,10092,'Research','N/A','Thursday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2336,45,150,10092,'ANA101','1PSY-B','Friday','07:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2337,45,197,10092,'Quasi Hours','N/A','Friday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:40:10',NULL,NULL),(2338,47,197,10092,'Quasi Hours','N/A','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2339,47,197,10092,'Consultation Hours','N/A','Monday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2340,47,197,10092,'Break','N/A','Monday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2341,47,197,10092,'Com.  Extension Hours','N/A','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2342,47,172,10092,'CHM102','2PSY-C','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2343,47,202,10092,'CHM102','2PSY-C','Tuesday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2344,47,197,10092,'Research','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2345,47,197,10092,'Consultation Hours','N/A','Wednesday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2346,47,197,10092,'Break','N/A','Wednesday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2347,47,197,10092,'Quasi Hours','N/A','Wednesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2348,47,172,10092,'CHM102','2PSY-A','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2349,47,197,10092,'Break','N/A','Thursday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2350,47,197,10092,'Quasi Hours','N/A','Thursday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2351,47,172,10092,'CHM102','2PSY-B','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2352,47,202,10092,'CHM102','2PSY-B','Friday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 02:45:24',NULL,NULL),(2360,37,151,10092,'CHM104A','1BSN-A','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:23:01',NULL,NULL),(2361,37,151,10092,'CHM104A','1BSN-B','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:23:01',NULL,NULL),(2362,37,197,10092,'Consultation Hours','N/A','Thursday','09:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:23:01',NULL,NULL),(2363,37,197,10092,'Consultation Hours','N/A','Friday','09:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:23:01',NULL,NULL),(2364,37,151,10092,'CHM104A','1BSN-C','Friday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:23:01',NULL,NULL),(2365,38,15,10092,'NSTP2','1PSYB','Monday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2366,38,15,10092,'NSTP2','1PSYA','Tuesday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2367,38,197,10092,'Consultation Hours','N/A','Wednesday','16:00:00','17:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2368,38,197,10092,'Consultation Hours','N/A','Thursday','16:00:00','17:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2369,38,173,10092,'PSE106','4PSYF','Saturday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2370,38,173,10092,'PSE106','4PSYD','Saturday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2371,38,173,10092,'PSE106','4PSYE','Saturday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2372,38,197,10092,'Consultation Hours','N/A','Saturday','16:00:00','17:00:00','Pending',0,NULL,'2026-04-06 03:31:28',NULL,NULL),(2373,39,173,10092,'PSM107','2PSY-C','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2374,39,173,10092,'PSM107','2PSY-C','Monday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2375,39,197,10092,'Consultation Hours','N/A','Tuesday','07:00:00','11:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2376,39,197,10092,'Break','N/A','Tuesday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2377,39,197,10092,'Quasi Hours','N/A','Tuesday','12:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2378,39,197,10092,'Research Hours','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2379,39,197,10092,'Break','N/A','Wednesday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2380,39,197,10092,'Community Extension Hours','N/A','Wednesday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2381,39,197,10092,'Quasi Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2382,39,173,10092,'PSM107','2PSY-B','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2383,39,173,10092,'PSM107','2PSY-B','Thursday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2384,39,173,10092,'PSM107','2PSY-A','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:36:21',NULL,NULL),(2385,44,197,10092,'Consultation Hours','N/A','Monday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2386,44,172,10092,'PSM108','1PSY-A','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2387,44,171,10092,'PSM106','2PSY-A','Monday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2388,44,197,10092,'Consultation Hours','N/A','Tuesday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2389,44,172,10092,'PSM109','1PSY-B','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2390,44,171,10092,'PSM106','2PSY-A','Tuesday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2391,44,15,10092,'PSM113','3PSY-E','Saturday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2392,44,171,10092,'PSM106','2PSY-A','Friday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2393,44,14,10092,'PSE106','4PSY-A','Saturday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2394,44,14,10092,'PSE106','4PSY-B','Saturday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:45:08',NULL,NULL),(2395,48,171,10092,'PSM108','2PSY-B','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2396,48,171,10092,'PSM108','2PSY-B','Monday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2397,48,171,10092,'PSM108','2PSY-A','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2398,48,171,10092,'PSM108','2PSY-A','Tuesday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2399,48,197,10092,'Research','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2400,48,197,10092,'Consultation Hours','N/A','Wednesday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2401,48,197,10092,'Com.  Extension Hours','N/A','Wednesday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2402,48,197,10092,'Consultation Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2403,48,171,10092,'PSM108','2PSY-C','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2404,48,171,10092,'PSM108','2PSY-C','Thursday','10:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2405,48,197,10092,'Quasi Hours','N/A','Thursday','16:00:00','17:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2406,48,14,10092,'PSE104','3PSY-F','Thursday','17:00:00','20:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2407,48,197,10092,'Quasi Hours','N/A','Friday','07:00:00','15:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2408,48,197,10092,'Consultation Hours','N/A','Friday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:46:19',NULL,NULL),(2409,42,197,10092,'Consultation Hours','N/A','Monday','07:00:00','11:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2410,42,197,10092,'Break','N/A','Monday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2411,42,197,10092,'Quasi Hours','N/A','Monday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2412,42,16,10092,'PSE104','3PSYC','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2413,42,27,10092,'PSM114','3PSYD','Monday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2414,42,197,10092,'Quasi Hours','N/A','Tuesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2415,42,197,10092,'Research Hours','N/A','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2416,42,16,10092,'PSE104','3PSYD','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2417,42,27,10092,'PSM114','3PSYC','Tuesday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2418,42,197,10092,'Quasi Hours','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2419,42,15,10092,'PSE104','3PSYE','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2420,42,197,10092,'Community Extension Hours','N/A','Thursday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2421,42,17,10092,'PSE104','3PSYA','Thursday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2422,42,27,10092,'PSM114','3PSYB','Thursday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2423,42,15,10092,'PSM114','3PSYE','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2424,42,197,10092,'Quasi Hours','N/A','Friday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2425,42,197,10092,'Break','N/A','Friday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2426,42,197,10092,'Quasi Hours','N/A','Friday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2427,42,16,10092,'PSE104','3PSYB','Friday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2428,42,27,10092,'PSM114','3PSYA','Friday','16:00:00','19:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2429,42,15,10092,'PSE105','4PSYD','Saturday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2430,42,15,10092,'PSE105','4PSYE','Saturday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 03:50:26',NULL,NULL),(2431,41,197,10092,'Administrative Hours','N/A','Monday','07:00:00','08:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2432,41,197,10092,'Break','N/A','Monday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2433,41,197,10092,'Administrative Hours','N/A','Monday','12:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2434,41,197,10092,'Administrative Hours','N/A','Tuesday','07:00:00','08:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2435,41,197,10092,'Break','N/A','Tuesday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2436,41,197,10092,'Administrative Hours','N/A','Tuesday','12:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2437,41,197,10092,'Research Hours','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2438,41,197,10092,'Break','N/A','Wednesday','10:00:00','11:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2439,41,197,10092,'Community Extension Hours','N/A','Wednesday','11:00:00','14:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2440,41,197,10092,'Administrative Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2441,41,197,10092,'Administrative Hours','N/A','Thursday','07:00:00','12:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2442,41,197,10092,'Break','N/A','Thursday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2443,41,197,10092,'Administrative Hours','N/A','Thursday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2444,41,197,10092,'Administrative Hours','N/A','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2445,41,197,10092,'Consultation Hours','N/A','Friday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2446,41,197,10092,'Break','N/A','Friday','12:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2447,41,197,10092,'Consultation Hours','N/A','Friday','13:00:00','15:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2448,41,197,10092,'Administrative Hours','N/A','Friday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2449,41,14,10092,'PSE105','4PSYC','Saturday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:37:43',NULL,NULL),(2450,40,197,10092,'Quasi Hours','N/A','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2451,40,172,10092,'PSE103','3PSY-C','Monday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2452,40,197,10092,'Break','N/A','Monday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2453,40,197,10092,'Consultation Hours','N/A','Monday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2454,40,197,10092,'Break','N/A','Tuesday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2455,40,197,10092,'Quasi Hours','N/A','Tuesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2456,40,197,10092,'Quasi Hours','N/A','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2457,40,172,10092,'PSE103','3PSY-D','Wednesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2458,40,197,10092,'Break','N/A','Wednesday','13:00:00','14:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2459,40,197,10092,'Consultation Hours','N/A','Wednesday','14:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2460,40,29,10092,'LOG101','3BSN-C','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2461,40,15,10092,'PSE103','3PSY-A','Thursday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2462,40,15,10092,'PSE103','3PSY-E','Thursday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2463,40,197,10092,'Quasi Hours','N/A','Friday','07:00:00','09:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2464,40,197,10092,'Break','N/A','Friday','09:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2465,40,172,10092,'PSE103','3PSY-B','Friday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2466,40,26,10092,'LOG101','3BSN-C','Friday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:41:06',NULL,NULL),(2467,53,163,10092,'COE101','2CPEB','Monday','07:00:00','08:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2468,53,165,10092,'COE116','2CPEA','Monday','08:00:00','11:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2469,53,197,10092,'Break','N/A','Monday','11:00:00','12:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2470,53,197,10092,'Consultation Hours','N/A','Tuesday','08:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2471,53,10,10092,'CPA102','2CPEA','Wednesday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2472,53,11,10092,'CPA102','2CPEB','Thursday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2473,53,159,10092,'COE112','2CPEB','Thursday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2474,53,160,10092,'COE112','2CPEA','Friday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2475,53,160,10092,'COE112','2CPEC','Friday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 04:50:18',NULL,NULL),(2476,57,11,10092,'CPP122','4CPEA','Monday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 05:18:18',NULL,NULL),(2477,57,197,10092,'Consultation Hours','N/A','Tuesday','08:00:00','11:00:00','Pending',0,NULL,'2026-04-06 05:18:18',NULL,NULL),(2478,57,10,10092,'CPP120','3CPEB','Tuesday','14:00:00','17:00:00','Pending',0,NULL,'2026-04-06 05:18:18',NULL,NULL),(2479,57,197,10092,'Consultation Hours','N/A','Wednesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 05:18:18',NULL,NULL),(2480,57,11,10092,'CPP120','3CPEB','Thursday','13:00:00','15:00:00','Pending',0,NULL,'2026-04-06 05:18:18',NULL,NULL),(2481,57,10,10092,'CPP120','3CPEA','Thursday','15:00:00','16:00:00','Pending',0,NULL,'2026-04-06 05:18:18',NULL,NULL),(2482,60,148,10092,'CPP101','1CPE-A','Monday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 06:34:28',NULL,NULL),(2483,60,148,10092,'CPP101','2CPE-A','Tuesday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 06:35:26',NULL,NULL),(2484,60,150,10092,'CPP102','3CPE-A','Wednesday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 06:36:05',NULL,NULL),(2485,60,150,10092,'CPP100','4CPE-B','Saturday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 06:40:16',NULL,NULL),(2486,58,148,10092,'CPP101','1CPE-A','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 06:52:30',NULL,NULL),(2487,58,149,10092,'CPP102','2CPE-B','Tuesday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 06:53:38',NULL,NULL),(2488,58,150,10092,'CPP103','1CPE-A','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 06:54:56',NULL,NULL),(2489,58,154,10092,'CPP105','4CPE-A','Friday','08:00:00','12:00:00','Pending',0,NULL,'2026-04-06 07:01:23',NULL,NULL),(2490,61,172,10092,'COE101','1CPE-A','Monday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 07:09:14',NULL,NULL),(2491,61,168,10092,'COE101','2CPE-B','Monday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 07:10:29',NULL,NULL),(2492,61,166,10092,'COE102','1CPE-A','Thursday','07:00:00','10:00:00','Pending',0,NULL,'2026-04-06 07:11:24',NULL,NULL),(2493,61,166,10092,'COE102','2CPE-A','Thursday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 07:12:08',NULL,NULL),(2495,51,155,10092,'CPE102','4CPE-B','Wednesday','08:00:00','10:00:00','Pending',0,NULL,'2026-04-06 07:15:37',NULL,NULL),(2496,51,155,10092,'CPE103','3CPE-B','Wednesday','10:00:00','12:00:00','Pending',0,NULL,'2026-04-06 07:17:01',NULL,NULL),(2497,51,154,10092,'CPE101','2CPE-B','Thursday','08:00:00','10:00:00','Pending',0,NULL,'2026-04-06 07:18:43',NULL,NULL),(2498,51,153,10092,'CPE104','4CPE-B','Thursday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 07:19:40',NULL,NULL),(2499,61,166,10092,'COE101','1CPE-A','Tuesday','13:00:00','16:00:00','Pending',0,NULL,'2026-04-06 07:42:07',NULL,NULL),(2500,61,152,10092,'COE102','2CPE-B','Tuesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 07:43:59',NULL,NULL),(2501,53,197,10092,'Consultation Hours','N/A','Wednesday','10:00:00','13:00:00','Pending',0,NULL,'2026-04-06 23:31:07',NULL,NULL);
/*!40000 ALTER TABLE `work_declaration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `active_schedules`
--

/*!50001 DROP VIEW IF EXISTS `active_schedules`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `active_schedules` AS select `w`.`declaration_id` AS `declaration_id`,`f`.`faculty_id` AS `faculty_id`,`f`.`faculty_name` AS `faculty_name`,`f`.`email` AS `email`,`f`.`department` AS `department`,`r`.`room_id` AS `room_id`,`r`.`building_name` AS `building_name`,`r`.`room_name` AS `room_name`,`r`.`floor_number` AS `floor_number`,`w`.`subject_code` AS `subject_code`,`w`.`day_of_week` AS `day_of_week`,`w`.`time_start` AS `time_start`,`w`.`time_end` AS `time_end`,`w`.`declaration_status` AS `declaration_status`,`s`.`semester_id` AS `semester_id`,`s`.`semester_name` AS `semester_name`,`s`.`semester_code` AS `semester_code`,`s`.`academic_year` AS `academic_year`,`s`.`is_active` AS `semester_active`,`s`.`is_locked` AS `semester_locked` from (((`work_declaration` `w` join `faculty` `f` on(`w`.`faculty_id` = `f`.`faculty_id`)) join `room` `r` on(`w`.`room_id` = `r`.`room_id`)) left join `semester` `s` on(`w`.`semester_id` = `s`.`semester_id`)) where `w`.`declaration_status` = 'Active' and `w`.`is_cancelled` = 0 and (`s`.`is_active` = 1 or `s`.`is_active` is null) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `faculty_schedule_summary`
--

/*!50001 DROP VIEW IF EXISTS `faculty_schedule_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `faculty_schedule_summary` AS select `f`.`faculty_id` AS `faculty_id`,`f`.`faculty_name` AS `faculty_name`,`f`.`department` AS `department`,`s`.`semester_id` AS `semester_id`,`s`.`semester_name` AS `semester_name`,count(`w`.`declaration_id`) AS `total_declarations`,sum(case when `w`.`declaration_status` = 'Active' then 1 else 0 end) AS `active_count`,sum(case when `w`.`declaration_status` = 'Pending' then 1 else 0 end) AS `pending_count`,sum(case when `w`.`is_cancelled` = 1 then 1 else 0 end) AS `cancelled_count`,min(`w`.`uploaded_at`) AS `first_upload`,max(`w`.`uploaded_at`) AS `last_upload` from ((`faculty` `f` left join `work_declaration` `w` on(`f`.`faculty_id` = `w`.`faculty_id`)) left join `semester` `s` on(`w`.`semester_id` = `s`.`semester_id`)) group by `f`.`faculty_id`,`s`.`semester_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-10 10:14:44
