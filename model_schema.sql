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
    `latitude` double NOT NULL,
    `longitude` double NOT NULL,
    `tag_hash` bigint NOT NULL,
    `is_membership` boolean NOT NULL,
    `expiry_date` date,
    `remaining_number` int
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
    `ticket_id` int NOT NULL
);

CREATE TABLE `TicketTag` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `ticket_id` int NOT NULL,
    `tag_id` int NOT NULL
);

ALTER TABLE `User` ADD FOREIGN KEY (`id`) REFERENCES `accounts_socialuser` (`id`);

ALTER TABLE `Ticket` ADD FOREIGN KEY (`seller_id`) REFERENCES `User` (`id`);

ALTER TABLE `Buy` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Buy` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `Bookmark` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Bookmark` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `TicketTag` ADD FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`id`);

ALTER TABLE `TicketTag` ADD FOREIGN KEY (`tag_id`) REFERENCES `Tag` (`id`);
