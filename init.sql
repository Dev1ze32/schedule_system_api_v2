-- MySQL dump 10.13  Distrib 9.5.0, for Win64 (x86_64)
--
-- Host: localhost    Database: campus_nav
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- GTID state at the beginning of the backup 
--
--
-- Temporary view structure for view `active_schedules`
--

DROP TABLE IF EXISTS `active_schedules`;
/*!50001 DROP VIEW IF EXISTS `active_schedules`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
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
 1 AS `semester_locked`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `admin_login`
--

DROP TABLE IF EXISTS `admin_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_login` (
  `login_id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `username` (`username`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `admin_login_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`admin_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_login`
--

LOCK TABLES `admin_login` WRITE;
/*!40000 ALTER TABLE `admin_login` DISABLE KEYS */;
INSERT INTO `admin_login` VALUES (1,1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',1,'2026-01-25 14:44:18');
/*!40000 ALTER TABLE `admin_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'System Admin','admin@school.edu','2026-01-21 10:27:00');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `faculty_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`faculty_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Aldrin soriano','soriano@university.edu','Computer Engineering','2026-01-17 14:59:36'),(2,'ENGR. CARLO B. CIMACIO','cimacio@university.edu','Computer Engineering','2026-01-17 15:00:21'),(3,'jhoana labitigan','jlabitigs@gmail.com','CPE','2026-01-21 23:09:02');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_login`
--

DROP TABLE IF EXISTS `faculty_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_login` (
  `login_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `password_salt` varchar(64) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `failed_attempts` int DEFAULT '0',
  `locked_until` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `username` (`username`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `faculty_login_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_login`
--

LOCK TABLES `faculty_login` WRITE;
/*!40000 ALTER TABLE `faculty_login` DISABLE KEYS */;
INSERT INTO `faculty_login` VALUES (1,1,'asoriano','d6ece2b40647aec079a1216cd8f7d15797502c97e2374f8abccd2c93595b98dd','96c31f10d78660f4f6a866cbfed4e461',1,0,NULL,'2026-01-25 19:14:38','2026-01-17 18:20:07','2026-01-25 19:14:37'),(2,2,'ccimacio','a9e0e0a57765990617d58edb683835d582d1d6de193f1ce5cef6996ec4df79dc','624b14b5cb930501cfde50eecc53115a',1,0,NULL,NULL,'2026-01-17 18:20:12','2026-01-21 23:08:06'),(3,3,'jlabitigan','5b78497f5c3a7a9ef7714126dee7be78f7b85ead61f2c25cdcdd629869821f7d','08326dcc4ba3ca10748210f104029103',1,0,NULL,NULL,'2026-01-21 23:09:02','2026-01-21 23:09:02');
/*!40000 ALTER TABLE `faculty_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `faculty_schedule_summary`
--

DROP TABLE IF EXISTS `faculty_schedule_summary`;
/*!50001 DROP VIEW IF EXISTS `faculty_schedule_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
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
 1 AS `last_upload`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int DEFAULT NULL,
  `action_type` varchar(50) DEFAULT NULL,
  `related_id` int DEFAULT NULL,
  `details` text,
  `search_timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `room_id` int NOT NULL AUTO_INCREMENT,
  `building_name` varchar(255) NOT NULL,
  `room_name` varchar(255) NOT NULL,
  `floor_number` int NOT NULL,
  PRIMARY KEY (`room_id`),
  UNIQUE KEY `room_number` (`room_name`)
) ENGINE=InnoDB AUTO_INCREMENT=197 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (1,'Main Building','Comlab 1',1),(2,'Main Building','Comlab 2',1),(3,'Main Building','Comlab 3',1),(4,'Main Building','Comlab 4',2),(5,'Main Building','Ergonomics Laboratory',2),(6,'Main Building','Digital Laboratory',2),(7,'Main Building','Network Laboratory',2),(8,'Main Building','Microbiology Parasitology Laboratory',2),(9,'Main Building','301',3),(10,'Main Building','302',3),(11,'Main Building','303',3),(12,'Main Building','304',3),(13,'Main Building','305',3),(14,'Main Building','306',3),(15,'Main Building','307',3),(16,'Main Building','308',3),(17,'Main Building','309',3),(18,'Main Building','310',3),(19,'Main Building','311',3),(20,'Main Building','312',3),(21,'Main Building','313',3),(22,'Main Building','314',3),(23,'Main Building','315',3),(24,'Main Building','316',3),(25,'Main Building','317',3),(26,'Main Building','318',3),(27,'Main Building','319',3),(28,'Main Building','Psychological Laboratory (320)',3),(29,'Main Building','321',3),(30,'Main Building','322',3),(148,'Bagong Cabuyao Hall','BCH101',1),(149,'Bagong Cabuyao Hall','BCH102',1),(150,'Bagong Cabuyao Hall','BCH103',1),(151,'Bagong Cabuyao Hall','BCH104',1),(152,'Bagong Cabuyao Hall','BCH105',1),(153,'Bagong Cabuyao Hall','BCH106',1),(154,'Bagong Cabuyao Hall','BCH107',1),(155,'Bagong Cabuyao Hall','BCH108',1),(156,'Bagong Cabuyao Hall','BCH201',2),(157,'Bagong Cabuyao Hall','BCH202',2),(158,'Bagong Cabuyao Hall','BCH203',2),(159,'Bagong Cabuyao Hall','BCH204',2),(160,'Bagong Cabuyao Hall','BCH205',2),(161,'Bagong Cabuyao Hall','BCH206',2),(162,'Bagong Cabuyao Hall','BCH207',2),(163,'Bagong Cabuyao Hall','BCH208',2),(164,'Bagong Cabuyao Hall','BCH209',2),(165,'Bagong Cabuyao Hall','BCH210',2),(166,'Bagong Cabuyao Hall','BCH301',3),(167,'Bagong Cabuyao Hall','BCH302',3),(168,'Bagong Cabuyao Hall','BCH303',3),(169,'Bagong Cabuyao Hall','BCH304',3),(170,'Bagong Cabuyao Hall','BCH305',3),(171,'Bagong Cabuyao Hall','BCH306',3),(172,'Bagong Cabuyao Hall','BCH307',3),(173,'Bagong Cabuyao Hall','BCH308',3),(174,'Bagong Cabuyao Hall','BCH309',3),(175,'Bagong Cabuyao Hall','BCH310',3),(176,'Bagong Cabuyao Hall','BCH401',4),(177,'Bagong Cabuyao Hall','BCH402',4),(178,'Bagong Cabuyao Hall','BCH403',4),(179,'Bagong Cabuyao Hall','BCH404',4),(180,'Bagong Cabuyao Hall','BCH405',4),(181,'Bagong Cabuyao Hall','BCH406',4),(182,'Bagong Cabuyao Hall','BCH407',4),(183,'Bagong Cabuyao Hall','BCH408',4),(184,'Bagong Cabuyao Hall','BCH409',4),(185,'Bagong Cabuyao Hall','BCH410',4),(186,'Bagong Cabuyao Hall','BCH501',5),(187,'Bagong Cabuyao Hall','BCH502',5),(188,'Bagong Cabuyao Hall','BCH503',5),(189,'Bagong Cabuyao Hall','BCH504',5),(190,'Bagong Cabuyao Hall','BCH505',5),(191,'Bagong Cabuyao Hall','BCH506',5),(192,'Bagong Cabuyao Hall','BCH507',5),(193,'Bagong Cabuyao Hall','BCH508',5),(194,'Bagong Cabuyao Hall','BCH509',5),(195,'Bagong Cabuyao Hall','BCH510',5);
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `semester_id` int NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(50) NOT NULL,
  `semester_code` varchar(20) NOT NULL,
  `academic_year` varchar(20) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_active` tinyint(1) DEFAULT '0',
  `is_locked` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `activated_at` datetime DEFAULT NULL,
  `deactivated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`semester_id`),
  UNIQUE KEY `semester_code` (`semester_code`),
  KEY `idx_active` (`is_active`),
  KEY `idx_dates` (`start_date`,`end_date`),
  KEY `idx_year` (`academic_year`),
  CONSTRAINT `chk_dates` CHECK ((`end_date` > `start_date`))
) ENGINE=InnoDB AUTO_INCREMENT=10016 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (9999,'Legacy Archive','LEGACY-000','2020-2025','2020-01-01','2025-12-31',0,1,'2026-01-18 17:16:09',NULL,NULL),(10015,'1st sem [admin]','2026-2','2025-2026','2026-01-10','2026-06-10',0,1,'2026-01-25 14:34:01','2026-01-25 14:42:52','2026-01-25 14:44:21');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester_audit_log`
--

DROP TABLE IF EXISTS `semester_audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester_audit_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `semester_id` int NOT NULL,
  `action` varchar(50) NOT NULL,
  `performed_by` int DEFAULT NULL,
  `performed_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `notes` text,
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_declaration` (
  `declaration_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `room_id` int NOT NULL,
  `semester_id` int NOT NULL,
  `subject_code` varchar(50) DEFAULT NULL,
  `class_section` varchar(50) DEFAULT NULL,
  `day_of_week` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time NOT NULL,
  `declaration_status` enum('Pending','Active','Rejected') DEFAULT 'Pending',
  `is_cancelled` tinyint(1) DEFAULT '0',
  `cancellation_reason` text,
  `uploaded_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_modified_at` datetime DEFAULT NULL,
  `last_modified_by` int DEFAULT NULL,
  PRIMARY KEY (`declaration_id`),
  KEY `fk_declaration_modifier` (`last_modified_by`),
  KEY `idx_declaration_status` (`declaration_status`,`semester_id`),
  KEY `idx_declaration_day` (`day_of_week`,`time_start`),
  KEY `idx_declaration_faculty_semester` (`faculty_id`,`semester_id`),
  KEY `idx_declaration_room_semester` (`room_id`,`semester_id`),
  KEY `idx_declaration_uploaded` (`uploaded_at`),
  KEY `idx_semester_work` (`semester_id`),
  CONSTRAINT `fk_declaration_modifier` FOREIGN KEY (`last_modified_by`) REFERENCES `faculty` (`faculty_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_declaration_semester` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE RESTRICT,
  CONSTRAINT `work_declaration_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE,
  CONSTRAINT `work_declaration_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_declaration`
--

LOCK TABLES `work_declaration` WRITE;
/*!40000 ALTER TABLE `work_declaration` DISABLE KEYS */;
INSERT INTO `work_declaration` VALUES (48,1,9,10015,'CPP106','2CPEA','Monday','07:30:00','10:00:00','Active',0,NULL,'2026-01-25 14:41:01',NULL,NULL),(49,1,10,10015,'Research','N/A','Monday','10:00:00','11:30:00','Active',0,NULL,'2026-01-25 14:41:01',NULL,NULL),(50,1,11,10015,'CPP106','2CPEB','Tuesday','10:00:00','11:30:00','Active',0,NULL,'2026-01-25 14:41:01',NULL,NULL),(51,1,12,10015,'CPP117','4CPEA','Wednesday','13:00:00','16:00:00','Active',0,NULL,'2026-01-25 14:41:02',NULL,NULL);
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
/*!50001 VIEW `active_schedules` AS select `w`.`declaration_id` AS `declaration_id`,`f`.`faculty_id` AS `faculty_id`,`f`.`faculty_name` AS `faculty_name`,`f`.`email` AS `email`,`f`.`department` AS `department`,`r`.`room_id` AS `room_id`,`r`.`building_name` AS `building_name`,`r`.`room_name` AS `room_name`,`r`.`floor_number` AS `floor_number`,`w`.`subject_code` AS `subject_code`,`w`.`day_of_week` AS `day_of_week`,`w`.`time_start` AS `time_start`,`w`.`time_end` AS `time_end`,`w`.`declaration_status` AS `declaration_status`,`s`.`semester_id` AS `semester_id`,`s`.`semester_name` AS `semester_name`,`s`.`semester_code` AS `semester_code`,`s`.`academic_year` AS `academic_year`,`s`.`is_active` AS `semester_active`,`s`.`is_locked` AS `semester_locked` from (((`work_declaration` `w` join `faculty` `f` on((`w`.`faculty_id` = `f`.`faculty_id`))) join `room` `r` on((`w`.`room_id` = `r`.`room_id`))) left join `semester` `s` on((`w`.`semester_id` = `s`.`semester_id`))) where ((`w`.`declaration_status` = 'Active') and (`w`.`is_cancelled` = 0) and ((`s`.`is_active` = 1) or (`s`.`is_active` is null))) */;
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
/*!50001 VIEW `faculty_schedule_summary` AS select `f`.`faculty_id` AS `faculty_id`,`f`.`faculty_name` AS `faculty_name`,`f`.`department` AS `department`,`s`.`semester_id` AS `semester_id`,`s`.`semester_name` AS `semester_name`,count(`w`.`declaration_id`) AS `total_declarations`,sum((case when (`w`.`declaration_status` = 'Active') then 1 else 0 end)) AS `active_count`,sum((case when (`w`.`declaration_status` = 'Pending') then 1 else 0 end)) AS `pending_count`,sum((case when (`w`.`is_cancelled` = true) then 1 else 0 end)) AS `cancelled_count`,min(`w`.`uploaded_at`) AS `first_upload`,max(`w`.`uploaded_at`) AS `last_upload` from ((`faculty` `f` left join `work_declaration` `w` on((`f`.`faculty_id` = `w`.`faculty_id`))) left join `semester` `s` on((`w`.`semester_id` = `s`.`semester_id`))) group by `f`.`faculty_id`,`s`.`semester_id` */;
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

-- Dump completed on 2026-01-25 19:46:55
