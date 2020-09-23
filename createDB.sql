SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `telegram` DEFAULT CHARACTER SET utf8 ;
USE `telegram` ;

CREATE TABLE IF NOT EXISTS `telegram`.`users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `hash` CHAR(32) NOT NULL,
  `chat_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `telegram`.`updates` (
  `update_id` INT UNSIGNED NOT NULL,
  `status` BOOL NOT NULL,
  PRIMARY KEY (`update_id`),
  UNIQUE INDEX `update_id_UNIQUE` (`update_id` ASC))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `telegram`.`chat_ids` (
  `chat_id` INT UNSIGNED NOT NULL,
  `chat_name` VARCHAR(45) NULL,
  PRIMARY KEY (`chat_id`),
  UNIQUE INDEX `chat_id_UNIQUE` (`chat_id` ASC))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
