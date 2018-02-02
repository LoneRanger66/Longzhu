CREATE SCHEMA `longzhu` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;

CREATE TABLE `longzhu`.`danmu` (
  `iddanmu` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NULL COMMENT '龙珠号',
  `username` VARCHAR(30) NULL COMMENT '用户名',
  `content` VARCHAR(60) NULL COMMENT '弹幕内容',
  `grade` INT NULL COMMENT '用户等级',
  `time` DATETIME NULL COMMENT '发言时间',
  `via` VARCHAR(10) NULL COMMENT '观看直播的设备',
  `name` VARCHAR(10) NULL COMMENT '粉丝牌的名字',
  `level` INT NULL COMMENT '粉丝牌等级',
  PRIMARY KEY (`iddanmu`))
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


