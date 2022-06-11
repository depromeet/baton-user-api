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

-- CREATE TABLE `accounts_socialuser` (
--   `id` int NOT NULL AUTO_INCREMENT,
--   `password` varchar(128) NOT NULL,
--   `last_login` datetime(6) DEFAULT NULL,
--   `is_superuser` tinyint(1) NOT NULL,
--   `uid` varchar(255) NOT NULL,
--   `provider` varchar(255) NOT NULL,
--   PRIMARY KEY (`id`)
-- );
use baton;

DROP TABLE IF EXISTS `Account`, `User`, `Ticket`, `Tag`, `Buy`, `Bookmark`, `TicketTag`, `TicketImage`;

CREATE TABLE `Account` (
    `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `holder` varchar(255) NOT NULL,
    `bank` varchar(255) NOT NULL,
    `number` varchar(255) NOT NULL
);

CREATE TABLE `User` (
    `id` int PRIMARY KEY NOT NULL,
    `name` varchar(255) NOT NULL,
    `nickname` varchar(255) NOT NULL,
    `phone_number` varchar(255)NOT NULL,
    `created_on` date NOT NULL,
    `account_id` int DEFAULT NULL,
    `address` varchar(255) NOT NULL,
    `detailed_address` varchar(255) NOT NULL,
    `check_terms_of_service` tinyint(1) NOT NULL,
    `check_privacy_policy` tinyint(1) NOT NULL,
    `point` point NOT NULL,
    UNIQUE KEY `account_id` (`account_id`),
--     FOREIGN KEY (`id`) REFERENCES `accounts_socialuser` (`id`),
    FOREIGN KEY (`account_id`) REFERENCES `Account` (`id`)
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
    `thumbnail` varchar(255),
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

ALTER TABLE `Ticket` add column expiry_date date;

ALTER TABLE `Ticket` add column bookmark_count int not null;


/*
DB 테스트 데이터 삽입 SQL 코드입니다. commit 규칙은 아래와 같습니다.
1. commit message에는 SQL DML(INSERT, UPDATE, DROP) 명령어 + 테이블 이름을 적습니다.
   테이블 이름은 여러 개 적어도 됩니다,
   (예시) INSERT Ticket / DELETE Ticket / UPDATE Ticket, User
2. 한 번에 명령어 한 종류만 commit 합니다.
4. 변경 이유는 코드 commit 후, history에 들어가 코드 변경 영역에 comment로 남깁니다.
*/

INSERT INTO `Tag` VALUES (1, "친절한 선생님", "친절한 선생님"), (2, "체계적인 수업", "체계적인 수업"), (3, "맞춤케어", "맞춤케어"), (4, "넓은 시설", "넓은 시설"), (5, "다양한 기구", "다양한 기구"), (6, "최신 기구", "최신 기구"), (7, "사람이 많은", "사람이 많은"), (8, "사람이 적은", "사람이 적은"), (9, "쾌적한 환경", "쾌적한 환경"), (10, "조용한 분위기", "조용한 분위기"), (11, "역세권", "역세권");

INSERT INTO `Account` (`id`, `holder`, `bank`, `number`) VALUES (1, '홍길동', 'KB국민은행', '11111111111111');

INSERT INTO `User` (`id`, `name`, `nickname`, `phone_number`, `created_on`,`point`,`address`,`detailed_address`,`check_terms_of_service`,`check_privacy_policy`)
   VALUES (1, '하나', '별명하나', '01011111111', '2022-06-03',ST_GeomFromText('POINT(37.287940866472375 127.05201020528645)', 4326),'경기도 수원시 영통구 도청로','광교중앙역 1번출구',1,1);
INSERT INTO `User` (`id`, `name`, `nickname`, `phone_number`, `created_on`,`point`, `account_id`,`address`,`detailed_address`,`check_terms_of_service`,`check_privacy_policy`)
    VALUES (2, '둘', '별명둘', '01022222222', '2022-06-04',ST_GeomFromText('POINT(37.287940866472375 127.05201020528645)', 4326), 1,'경기도 수원시 영통구 도청로','광교중앙역 1번출구',1,1);
INSERT INTO `User` (`id`, `name`, `nickname`, `phone_number`, `created_on`,`point`,`address`,`detailed_address`,`check_terms_of_service`,`check_privacy_policy`)
    VALUES (3, '셋', '별명셋', '01033333333', '2022-03-03',ST_GeomFromText('POINT(37.287940866472375 127.05201020528645)', 4326),'경기도 수원시 영통구 도청로','광교중앙역 1번출구',1,1);
INSERT INTO `User` (`id`, `name`, `nickname`, `phone_number`, `created_on`,`point`,`address`,`detailed_address`,`check_terms_of_service`,`check_privacy_policy`)
     VALUES (4, '넷', '별명넷', '01044444444', '2022-04-04',ST_GeomFromText('POINT(37.287940866472375 127.05201020528645)', 4326),'경기도 수원시 영통구 도청로','광교중앙역 1번출구',1,1);

INSERT INTO `Ticket` VALUES (1,1,'장ㅈ',10000,'2022-06-01 04:41:14',0,3,1,1,NULL,0,1,2,1,1,1,1,1,1,'사세',NULL,2,ST_GeomFromText('POINT(37.2511767810868 127.072240105848)', 4326),'경기도 수원시 영통구 봉영로',NULL,'2023-04-05', 1);
INSERT INTO `Ticket` VALUES (2,1,'장ㅈ',10000,'2022-06-01 15:38:16',0,3,1,1,NULL,0,1,2,1,1,1,1,1,1,'사세',NULL,2,ST_GeomFromText('POINT(37.2511767810868 127.072240105848)', 4326),'경기도 수원시 영통구 봉영로','https://depromeet11th.s3.ap-northeast-2.amazonaws.com/6team/s_26c56d80-70fc-4068-8f7e-5721252b5296.jpeg','2023-04-05', 1);
INSERT INTO `Ticket` VALUES (3,1,'장ㅈ',10000,'2022-06-01 17:53:15',0,3,1,1,NULL,0,1,2,1,1,1,1,1,1,'사세',NULL,2,ST_GeomFromText('POINT(37.2511767810868 127.072240105848)', 4326),'경기도 수원시 영통구 봉영로','https://depromeet11th.s3.ap-northeast-2.amazonaws.com/6team/s_698a8e1e-a7f1-42d2-9c39-14681148356e.jpeg','2023-04-05', 0);
INSERT INTO `Ticket` VALUES (4,2,'장ㅈ',10000,'2022-06-01 18:34:23',0,3,1,1,NULL,0,1,2,1,1,1,1,1,1,'사세',NULL,2,ST_GeomFromText('POINT(37.2511767810868 127.072240105848)', 4326),'경기도 수원시 영통구 봉영로',NULL,'2023-04-05', 1);

INSERT INTO `TicketImage` VALUES (1,2,'https://depromeet11th.s3.ap-northeast-2.amazonaws.com/6team/26c56d80-70fc-4068-8f7e-5721252b5296.jpeg',0,'https://depromeet11th.s3.ap-northeast-2.amazonaws.com/6team/s_26c56d80-70fc-4068-8f7e-5721252b5296.jpeg'),(2,3,'https://depromeet11th.s3.ap-northeast-2.amazonaws.com/6team/698a8e1e-a7f1-42d2-9c39-14681148356e.jpeg',0,'https://depromeet11th.s3.ap-northeast-2.amazonaws.com/6team/s_698a8e1e-a7f1-42d2-9c39-14681148356e.jpeg');

INSERT INTO `TicketTag` VALUES (1,1,2),(2,1,1),(3,2,2),(4,2,1),(5,3,1),(6,3,2);

INSERT INTO `Bookmark` (`user_id`, `ticket_id`) VALUES (3, 1);
INSERT INTO `Bookmark` (`user_id`, `ticket_id`) VALUES (3, 2);
INSERT INTO `Bookmark` (`user_id`, `ticket_id`) VALUES (1, 4);

INSERT INTO `Buy` (`user_id`, `ticket_id`) VALUES (3, 1);
INSERT INTO `Buy` (`user_id`, `ticket_id`, `date`) VALUES (2, 2, '2022-06-28 15:00:00');
