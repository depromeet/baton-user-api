/*
테이블 변경사항 발생 시 이 테이블 정의 코드를 직접 수정합니다. commit 규칙은 아래와 같습니다.
1. commit당 한 테이블만 수정합니다.
2. commit message에는 SQL DDL 코드 앞부분을 적습니다.
   (예시) Alter table Ticket ADD, Create table Ticket
3. Alter table의 경우 ADD, DROP, MODIFY, CHANGE 연산을 허용하며,
   한 commit에 복수의 연산도 가능합니다. 쉼표로 구분하여 commit msg에 적습니다.
   (예시) Alter table Ticket ADD, DROP
4. 변경 이유는 코드 commit 후, history에 들어가 코드 변경 영역에 comment로 남깁니다.
*/

CREATE TABLE `accounts_socialuser` (
    `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) DEFAULT NULL,
    `is_superuser` tinyint(1) NOT NULL,
    `social_id` varchar(255) NOT NULL,
    `provider` varchar(30) NOT NULL
);

CREATE TABLE `User` (
    `id` int PRIMARY KEY NOT NULL,
    `nickname` varchar(255) NOT NULL,
    `gender` tinyint(1) DEFAULT NULL
);

CREATE TABLE `Ticket` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `seller_id` int NOT NULL,
    `location` varchar(255) NOT NULL,
    `price` int NOT NULL,
    `created_at` timestamp NOT NULL,
    `state` int NOT NULL, -- 0: 판매중, 1: 예약중, 2: 판매완료
    `tag_hash` bigint NOT NULL,
    `is_membership` boolean NOT NULL,
    `is_holding` tinyint(1) NOT NULL,
    `remaining_number` int,
    `type` int NOT NULL, -- 0: 헬스, 1: PT, 2: 필라테스 / 요가, 3: 기타
    `can_nego` tinyint(1) NOT NULL,
    `trade_type` int NOT NULL, -- 0: 대면, 1: 비대면, 2: 둘 다
    `has_shower` tinyint(1) NOT NULL,
    `has_locker` tinyint(1) NOT NULL,
    `has_clothes` tinyint(1) NOT NULL,
    `has_gx` tinyint(1) NOT NULL,
    `can_resell` tinyint(1) NOT NULL,
    `can_refund` tinyint(1) NOT NULL,
    `description` varchar(255) NOT NULL,
    `thumbnail` varchar(255) NOT NULL,
    `transfer_fee` int NOT NULL, -- 0: 판매자, 1: 구매자, 2: 해당 없음
    `point` point NOT NULL
);

CREATE TABLE `Buy` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `ticket_id` int UNIQUE NOT NULL,
    `date` datetime(0)
);

CREATE TABLE `Tag` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `subject` varchar(255) NOT NULL,
    `content` text NOT NULL
);

CREATE TABLE `Bookmark` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `ticket_id` int NOT NULL,
    UNIQUE KEY (`user_id`, `ticket_id`)
);

CREATE TABLE `TicketTag` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `ticket_id` int NOT NULL,
    `tag_id` int NOT NULL
);

CREATE TABLE `TicketImage` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `url` varchar(255) NOT NULL,
  `is_main` boolean NOT NULL
);

ALTER TABLE `User` ADD FOREIGN KEY (`id`) REFERENCES `accounts_socialuser` (`id`);

ALTER TABLE `Ticket` ADD FOREIGN KEY (`seller_id`) REFERENCES `User` (`id`);

ALTER TABLE `Buy` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Buy` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `Bookmark` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Bookmark` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `TicketTag` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `TicketTag` ADD FOREIGN KEY (`tag_id`) REFERENCES `Tag` (`id`);

ALTER TABLE `TicketImage` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `Ticket` ADD `address` varchar(255) not null;

ALTER TABLE `TicketImage` ADD `thumbnail_url` varchar(255) not null;

ALTER TABLE `Ticket` ADD `main_image` varchar(255);

INSERT INTO `Tag` VALUES (1, "친절한 선생님", "친절한 선생님"), (2, "체계적인 수업", "체계적인 수업"), (3, "맞춤케어", "맞춤케어"), (4, "넓은 시설", "넓은 시설"), (5, "다양한 기구", "다양한 기구"), (6, "최신 기구", "최신 기구"), (7, "사람이 많은", "사람이 많은"), (8, "사람이 적은", "사람이 적은"), (9, "쾌적한 환경", "쾌적한 환경"), (10, "조용한 분위기", "조용한 분위기"), (11, "역세권", "역세권");

ALTER TABLE `Ticket` add column expiry_date date;
