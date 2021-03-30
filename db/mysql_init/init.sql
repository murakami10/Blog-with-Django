-- MySQL dump 10.13  Distrib 5.7.33, for Linux (x86_64)
--
-- Host: localhost    Database: article
-- ------------------------------------------------------
-- Server version	5.7.33

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
-- Table structure for table `article_user`
--

DROP TABLE IF EXISTS `article_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_user`
--

LOCK TABLES `article_user` WRITE;
/*!40000 ALTER TABLE `article_user` DISABLE KEYS */;
INSERT INTO `article_user` VALUES (1,'pbkdf2_sha256$216000$1rMLNIZDHZZM$yFHpudry3ahuBNG580KIFHFaFSJ7Fh4GN+aDLrdx2J0=','2021-03-30 11:26:00.676158',1,'','',1,1,'2021-02-28 21:56:47.820287','tom','root@root.com');
/*!40000 ALTER TABLE `article_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article_user_groups`
--

DROP TABLE IF EXISTS `article_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article_user_groups_user_id_group_id_802f39c9_uniq` (`user_id`,`group_id`),
  KEY `article_user_groups_group_id_3407d6e6_fk_auth_group_id` (`group_id`),
  CONSTRAINT `article_user_groups_group_id_3407d6e6_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `article_user_groups_user_id_9cc83b79_fk_article_user_id` FOREIGN KEY (`user_id`) REFERENCES `article_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_user_groups`
--

LOCK TABLES `article_user_groups` WRITE;
/*!40000 ALTER TABLE `article_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `article_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article_user_user_permissions`
--

DROP TABLE IF EXISTS `article_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article_user_user_permis_user_id_permission_id_5112008a_uniq` (`user_id`,`permission_id`),
  KEY `article_user_user_pe_permission_id_ffae5172_fk_auth_perm` (`permission_id`),
  CONSTRAINT `article_user_user_pe_permission_id_ffae5172_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `article_user_user_pe_user_id_e4e707ab_fk_article_u` FOREIGN KEY (`user_id`) REFERENCES `article_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_user_user_permissions`
--

LOCK TABLES `article_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `article_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `article_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `summary` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `publish_date` datetime(6) NOT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `public` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articles_author_id_e11be98a_fk_article_user_id` (`author_id`),
  KEY `articles_category_id_8d549191_fk_articles_categories_id` (`category_id`),
  CONSTRAINT `articles_author_id_e11be98a_fk_article_user_id` FOREIGN KEY (`author_id`) REFERENCES `article_user` (`id`),
  CONSTRAINT `articles_category_id_8d549191_fk_articles_categories_id` FOREIGN KEY (`category_id`) REFERENCES `articles_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (13,'こんにちわん','これはテストです','# これはテストです\r\nよろしくおねがいします!!!\r\n~~よろしくおねがいします~~\r\n\r\n## これは二回目のテストです。\r\nこんんにちわ\r\n\r\n### 3回目\r\n3回目です','2021-03-11 06:43:35.000000',1,5,1),(32,'例1','この記事は例2です','# これは犬の例です\r\n![my_dog](/media/editor/10107_20210330200047573220.jpg \"my_dog\")\r\nかわいい','2027-12-15 11:01:47.000000',1,5,1),(33,'例2','これは非公開の記事の例です','# この記事は非公開です\r\nそのため一般ユーザーには見れません','2021-03-30 11:03:34.000000',1,5,0),(34,'例','公開済み','公開済み\r\n```\r\nthis code is public\r\nthis code is public\r\nthis code is public\r\nthis code is public\r\n	this code is public\r\n	this code is public\r\n```','2021-03-30 11:06:35.000000',1,5,1),(35,'記事','記事です','これはきじですか？\r\n\r\n| a  |   a|\r\n| ------------ | ------------ |\r\n| a  |  a |\r\n|  a | a  |','2021-03-30 11:08:40.000000',1,6,1),(36,'xxx','これは例','[TOC]\r\n\r\n# 一番\r\n11\r\n/\r\n/\r\n/\r\n1\r\n1\r\n1\r\n1\r\n1\r\n1\r\n\r\na\r\n# 二番\r\n222\r\n2\r\n2\r\n2\r\n1\r\n1\r\n1\r\n1\r\n1\r\n2\r\n2\r\n\r\n# 三番\r\n333\r\n3\r\n3\r\n3\r\n3\r\n3\r\n3\r\n\r\n3\r\n3\r\n# ラスト\r\nlast\r\nlast','2021-03-30 11:21:25.000000',1,5,1),(37,'あ','あかさたな','ｘ','2021-03-30 11:24:58.000000',1,5,1),(38,'aiueo','あいうえお','n','2021-03-30 11:25:09.000000',1,5,1);
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_categories`
--

DROP TABLE IF EXISTS `articles_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_categories`
--

LOCK TABLES `articles_categories` WRITE;
/*!40000 ALTER TABLE `articles_categories` DISABLE KEYS */;
INSERT INTO `articles_categories` VALUES (5,'category1'),(6,'category2'),(7,'カテゴリ');
/*!40000 ALTER TABLE `articles_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_tag`
--

DROP TABLE IF EXISTS `articles_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articles_tag_article_id_tag_id_85bc45b1_uniq` (`article_id`,`tag_id`),
  KEY `articles_tag_tag_id_98834895_fk_articles_tags_id` (`tag_id`),
  CONSTRAINT `articles_tag_article_id_359d2a80_fk_articles_id` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`),
  CONSTRAINT `articles_tag_tag_id_98834895_fk_articles_tags_id` FOREIGN KEY (`tag_id`) REFERENCES `articles_tags` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_tag`
--

LOCK TABLES `articles_tag` WRITE;
/*!40000 ALTER TABLE `articles_tag` DISABLE KEYS */;
INSERT INTO `articles_tag` VALUES (10,32,6),(11,33,7),(12,34,6),(13,35,6),(15,36,7),(14,36,9),(16,37,7),(17,38,8);
/*!40000 ALTER TABLE `articles_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_tags`
--

DROP TABLE IF EXISTS `articles_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articles_tags_name_c54b5b02_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_tags`
--

LOCK TABLES `articles_tags` WRITE;
/*!40000 ALTER TABLE `articles_tags` DISABLE KEYS */;
INSERT INTO `articles_tags` VALUES (6,'tag1'),(7,'tag2'),(8,'tag3'),(9,'tag4'),(10,'タグ');
/*!40000 ALTER TABLE `articles_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_user'),(2,'Can change user',1,'change_user'),(3,'Can delete user',1,'delete_user'),(4,'Can view user',1,'view_user'),(5,'Can add article category',2,'add_articlecategory'),(6,'Can change article category',2,'change_articlecategory'),(7,'Can delete article category',2,'delete_articlecategory'),(8,'Can view article category',2,'view_articlecategory'),(9,'Can add article',3,'add_article'),(10,'Can change article',3,'change_article'),(11,'Can delete article',3,'delete_article'),(12,'Can view article',3,'view_article'),(13,'Can add log entry',4,'add_logentry'),(14,'Can change log entry',4,'change_logentry'),(15,'Can delete log entry',4,'delete_logentry'),(16,'Can view log entry',4,'view_logentry'),(17,'Can add permission',5,'add_permission'),(18,'Can change permission',5,'change_permission'),(19,'Can delete permission',5,'delete_permission'),(20,'Can view permission',5,'view_permission'),(21,'Can add group',6,'add_group'),(22,'Can change group',6,'change_group'),(23,'Can delete group',6,'delete_group'),(24,'Can view group',6,'view_group'),(25,'Can add content type',7,'add_contenttype'),(26,'Can change content type',7,'change_contenttype'),(27,'Can delete content type',7,'delete_contenttype'),(28,'Can view content type',7,'view_contenttype'),(29,'Can add session',8,'add_session'),(30,'Can change session',8,'change_session'),(31,'Can delete session',8,'delete_session'),(32,'Can view session',8,'view_session'),(33,'Can add tag',9,'add_tag'),(34,'Can change tag',9,'change_tag'),(35,'Can delete tag',9,'delete_tag'),(36,'Can view tag',9,'view_tag');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_article_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_article_user_id` FOREIGN KEY (`user_id`) REFERENCES `article_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-03-02 04:09:26.268579','1','python',1,'[{\"added\": {}}]',2,1),(2,'2021-03-02 11:57:06.581244','7','777777',3,'',3,1),(3,'2021-03-02 11:57:06.591719','6','aaaa',3,'',3,1),(4,'2021-03-02 11:57:06.596519','5','aiueo',3,'',3,1),(5,'2021-03-02 11:57:06.600808','4','aaa',3,'',3,1),(6,'2021-03-02 11:57:06.603645','3','aaa',3,'',3,1),(7,'2021-03-02 11:57:06.606561','2','first',3,'',3,1),(8,'2021-03-02 11:57:06.609548','1','aiueo',3,'',3,1),(9,'2021-03-12 22:08:47.317196','23','aiueo',1,'[{\"added\": {}}]',3,1),(10,'2021-03-12 22:09:03.095505','24','x',1,'[{\"added\": {}}]',3,1),(11,'2021-03-12 22:09:16.891325','25','aiueo',1,'[{\"added\": {}}]',3,1),(12,'2021-03-12 22:09:35.827608','26','x',1,'[{\"added\": {}}]',3,1),(13,'2021-03-12 22:09:56.542007','27','d',1,'[{\"added\": {}}]',3,1),(14,'2021-03-15 01:07:09.354641','1','py',1,'[{\"added\": {}}]',9,1),(15,'2021-03-15 01:11:12.686079','2','ruby',1,'[{\"added\": {}}]',9,1),(16,'2021-03-15 01:11:17.661664','3','php',1,'[{\"added\": {}}]',9,1),(17,'2021-03-15 04:04:29.059802','29','xx',2,'[{\"changed\": {\"fields\": [\"Content\", \"\\u30bf\\u30b0\"]}}]',3,1),(18,'2021-03-30 05:50:26.784919','31','first express',2,'[{\"changed\": {\"fields\": [\"Content\"]}}]',3,1),(19,'2021-03-30 10:32:58.264436','4','hhhh',3,'',9,1),(20,'2021-03-30 10:32:58.304167','3','php',3,'',9,1),(21,'2021-03-30 10:32:58.323070','2','ruby',3,'',9,1),(22,'2021-03-30 10:32:58.350585','1','py',3,'',9,1),(23,'2021-03-30 10:33:10.740198','5','tag1',1,'[{\"added\": {}}]',9,1),(24,'2021-03-30 10:33:25.728210','13','こんにちわん',2,'[{\"changed\": {\"fields\": [\"\\u30bf\\u30b0\"]}}]',3,1),(25,'2021-03-30 10:33:35.243293','5','tag1',3,'',9,1),(26,'2021-03-30 10:33:55.002651','6','tag1',1,'[{\"added\": {}}]',9,1),(27,'2021-03-30 10:33:58.589794','7','tag2',1,'[{\"added\": {}}]',9,1),(28,'2021-03-30 10:34:02.261368','8','tag3',1,'[{\"added\": {}}]',9,1),(29,'2021-03-30 10:34:09.189981','9','tag4',1,'[{\"added\": {}}]',9,1),(30,'2021-03-30 10:34:33.933109','31','first express',3,'',3,1),(31,'2021-03-30 10:34:33.966852','29','xx',3,'',3,1),(32,'2021-03-30 10:34:33.988986','28','xxx',3,'',3,1),(33,'2021-03-30 10:34:34.006665','27','d',3,'',3,1),(34,'2021-03-30 10:34:34.026951','26','x',3,'',3,1),(35,'2021-03-30 10:34:34.050486','25','aiueo',3,'',3,1),(36,'2021-03-30 10:34:34.070303','24','x',3,'',3,1),(37,'2021-03-30 10:34:34.087423','23','aiueo',3,'',3,1),(38,'2021-03-30 10:34:34.101445','18','dasf',3,'',3,1),(39,'2021-03-30 10:34:34.119218','15','xx',3,'',3,1),(40,'2021-03-30 10:54:59.744261','13','こんにちわん',2,'[{\"changed\": {\"fields\": [\"Content\"]}}]',3,1),(41,'2021-03-30 10:55:38.986128','5','category1',1,'[{\"added\": {}}]',2,1),(42,'2021-03-30 10:55:46.677239','6','category2',1,'[{\"added\": {}}]',2,1),(43,'2021-03-30 10:56:00.290991','13','こんにちわん',2,'[{\"changed\": {\"fields\": [\"\\u30ab\\u30c6\\u30b4\\u30ea\"]}}]',3,1),(44,'2021-03-30 10:56:12.388365','4','aiu',3,'',2,1),(45,'2021-03-30 10:56:12.419106','3','python2',3,'',2,1),(46,'2021-03-30 10:56:12.441032','2','django',3,'',2,1),(47,'2021-03-30 10:56:12.459468','1','python',3,'',2,1),(48,'2021-03-30 11:01:55.514146','32','例1',1,'[{\"added\": {}}]',3,1),(49,'2021-03-30 11:02:02.982770','32','例1',2,'[{\"changed\": {\"fields\": [\"\\u30bf\\u30b0\"]}}]',3,1),(50,'2021-03-30 11:03:44.321535','33','例2',1,'[{\"added\": {}}]',3,1),(51,'2021-03-30 11:05:09.228847','1','root@root.com',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',1,1),(52,'2021-03-30 11:06:48.197719','34','例',1,'[{\"added\": {}}]',3,1),(53,'2021-03-30 11:08:48.810170','35','記事',1,'[{\"added\": {}}]',3,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (4,'admin','logentry'),(3,'article','article'),(2,'article','articlecategory'),(9,'article','tag'),(1,'article','user'),(6,'auth','group'),(5,'auth','permission'),(7,'contenttypes','contenttype'),(8,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-02-28 21:55:35.281344'),(2,'contenttypes','0002_remove_content_type_name','2021-02-28 21:55:35.503615'),(3,'auth','0001_initial','2021-02-28 21:55:35.737010'),(4,'auth','0002_alter_permission_name_max_length','2021-02-28 21:55:36.311756'),(5,'auth','0003_alter_user_email_max_length','2021-02-28 21:55:36.333960'),(6,'auth','0004_alter_user_username_opts','2021-02-28 21:55:36.374494'),(7,'auth','0005_alter_user_last_login_null','2021-02-28 21:55:36.400300'),(8,'auth','0006_require_contenttypes_0002','2021-02-28 21:55:36.415190'),(9,'auth','0007_alter_validators_add_error_messages','2021-02-28 21:55:36.444901'),(10,'auth','0008_alter_user_username_max_length','2021-02-28 21:55:36.472697'),(11,'auth','0009_alter_user_last_name_max_length','2021-02-28 21:55:36.499338'),(12,'auth','0010_alter_group_name_max_length','2021-02-28 21:55:36.590532'),(13,'auth','0011_update_proxy_permissions','2021-02-28 21:55:36.619418'),(14,'auth','0012_alter_user_first_name_max_length','2021-02-28 21:55:36.643972'),(15,'article','0001_initial','2021-02-28 21:55:37.108350'),(16,'admin','0001_initial','2021-02-28 21:55:37.997871'),(17,'admin','0002_logentry_remove_auto_add','2021-02-28 21:55:38.258083'),(18,'admin','0003_logentry_add_action_flag_choices','2021-02-28 21:55:38.295738'),(19,'article','0002_auto_20210301_0654','2021-02-28 21:55:38.354977'),(20,'sessions','0001_initial','2021-02-28 21:55:38.457880'),(21,'article','0003_article_public','2021-03-13 00:43:13.309809'),(22,'article','0004_auto_20210313_0952','2021-03-13 00:52:46.289337'),(23,'article','0005_tag','2021-03-15 00:54:01.529627'),(24,'article','0006_auto_20210315_1006','2021-03-15 01:10:31.817893'),(25,'article','0007_auto_20210315_1336','2021-03-15 04:36:55.137426'),(26,'article','0008_auto_20210330_1954','2021-03-30 10:54:29.311309');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('g4rdpglikhiquoinawvq41k25awolzel','.eJxVjMsOwiAQRf-FtSFDy2Nw6d5vIAMDUjU0Ke3K-O_apAvd3nPOfYlA21rD1vMSJhZnocTpd4uUHrntgO_UbrNMc1uXKcpdkQft8jpzfl4O9--gUq_fGkebivfsXQJXDGo3EDAz2KJTNIQqEaNxTAjZw4iKPZasBw1kS2bx_gDqPDhL:1lRCVU:Ce5r9JeEWHvrI2RY4wkHlfNBb5lSDpmWo2D47gWtNCQ','2021-04-13 11:26:00.754586');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-30 20:31:53
