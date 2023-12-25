@echo off
set MYSQL_USER=root
set MYSQL_PASSWORD=root
set MYSQL_HOST=localhost
set DATABASE_NAME=bookstore

mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% -h%MYSQL_HOST% -e "CREATE DATABASE IF NOT EXISTS %DATABASE_NAME%;"
mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% -h%MYSQL_HOST% %DATABASE_NAME% -e ^
"^
DROP USER IF EXISTS 'user'@'localhost';^
FLUSH PRIVILEGES;CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';^
GRANT ALL PRIVILEGES ON %DATABASE_NAME%.* TO 'user'@'localhost';^
DROP DATABASE IF EXISTS %DATABASE_NAME%;^
CREATE DATABASE %DATABASE_NAME%;^
USE %DATABASE_NAME%;^
CREATE TABLE `pending_user` (^
  `pending_user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,^
  `name` varchar(128) DEFAULT NULL,^
  `email_or_phone_number` varchar(256) NOT NULL,^
  `validation_code` int(5) UNSIGNED NOT NULL,^
  `code_resend_attempts` int(3) UNSIGNED DEFAULT 0,^
  `role` varchar(10) DEFAULT 'customer',^
  `password_hash` varchar(512),^
  `salt` varchar(5),^
  `default_lang` varchar(2) DEFAULT 'en',^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`pending_user_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `user` (^
  `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,^
  `email` varchar(256) UNIQUE DEFAULT NULL,^
  `phone_number` varchar(25) UNIQUE DEFAULT NULL,^
  `password_hash` varchar(512),^
  `salt` varchar(5),^
  `default_lang` varchar(2) DEFAULT 'en',^
  `default_role` varchar(10) DEFAULT 'customer',^
  `name` varchar(128) DEFAULT NULL,^
  `image_id` char(36) DEFAULT NULL,^
  `is_active` bool DEFAULT true,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`user_id`)^
) ENGINE=InnoDB AUTO_INCREMENT=3120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `refresh_token` (^
  `token` varchar(256) NOT NULL,^
  `user_id` int(10) UNSIGNED NOT NULL,^
  `is_active` bool DEFAULT true,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  PRIMARY KEY (`token`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `system_admin` (^
  `user_id` int(10) UNSIGNED NOT NULL,^
  `is_active` bool DEFAULT true,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`user_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `customer` (^
  `user_id` int(10) UNSIGNED NOT NULL,^
  `active_parking_request_id` int(10) UNSIGNED DEFAULT NULL,^
  `active_return_request_id` int(10) UNSIGNED DEFAULT NULL,^
  `is_active` bool DEFAULT true,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`user_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `manager` (^
  `user_id` int(10) UNSIGNED NOT NULL,^
  `is_active` bool DEFAULT true,^
  `company_permissions` varchar(512) DEFAULT '',^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`user_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `book` (^
  `book_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,^
  `name` varchar(512) DEFAULT '',^
  `author` varchar(512) DEFAULT '',^
  `description` varchar(512) DEFAULT '',^
  `language` varchar(3) DEFAULT 'en',^
  `year` varchar(10) DEFAULT '',^
  `price` float DEFAULT 0,^
  `stock` int(10) UNSIGNED DEFAULT 0,^
  `image_id` char(36) DEFAULT NULL,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`book_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `product` (^
  `product_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,^
  `name` varchar(512) DEFAULT '',^
  `price` int(10) UNSIGNED NOT NULL,^
  `quantity` int(10) UNSIGNED NOT NULL,^
  `book_id` int(10) UNSIGNED NOT NULL,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`product_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `order` (^
  `order_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,^
  `quantity` int(10) UNSIGNED NOT NULL,^
  `book_id` int(10) UNSIGNED NOT NULL,^
  `customer_id` int(10) UNSIGNED NOT NULL,^
  `purchased` bool DEFAULT false,^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`order_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `payment` (^
  `payment_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,^
  `status` varchar(512) DEFAULT '',^
  `order_id` int(10) UNSIGNED NOT NULL,^
  `customer_id` int(10) UNSIGNED NOT NULL,^
  `date` varchar(512) DEFAULT '',^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`payment_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
CREATE TABLE `image` (^
  `image_id` char(36) DEFAULT (UUID()),^
  `url` varchar(256),^
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,^
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,^
  PRIMARY KEY (`image_id`)^
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;^
INSERT INTO `book` (`name`, `author`, `description`, `language`, `year`, `price`, `stock`, `image_id`)^
VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 'A classic novel about the American Dream', 'en', '1925', 19.99, 50, 'abc123'),('To Kill a Mockingbird', 'Harper Lee', 'A story of racial injustice in the American South', 'en', '1960', 15.99, 30, 'def456'),('1984', 'George Orwell', 'A dystopian novel about totalitarianism', 'en', '1949', 24.99, 40, 'ghi789'),('Pride and Prejudice', 'Jane Austen', 'A romantic novel about societal expectations', 'en', '1813', 12.99, 20, 'jkl012'),('The Hobbit', 'J.R.R. Tolkien', 'A fantasy adventure novel', 'en', '1937', 29.99, 25, 'mno345'),('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'The first book in the Harry Potter series', 'en', '1997', 18.99, 60, 'pqr678'),('The Catcher in the Rye', 'J.D. Salinger', 'A novel about teenage angst and rebellion', 'en', '1951', 17.99, 35, 'stu901'),('Moby-Dick', 'Herman Melville', 'A tale of the captains obsessive quest for the white whale', 'en', '1851', 22.99, 15, 'vwx234'),('The Lord of the Rings', 'J.R.R. Tolkien', 'An epic fantasy trilogy', 'en', '1954', 39.99, 55, 'yzab567'),('The Da Vinci Code', 'Dan Brown', 'A mystery-thriller novel', 'en', '2003', 26.99, 48, 'cde890'),('The Alchemist', 'Paulo Coelho', 'A philosophical novel about following ones dreams', 'en', '1988', 21.99, 42, 'fgh123'),('Brave New World', 'Aldous Huxley', 'A dystopian novel about a futuristic society', 'en', '1932', 28.99, 38, 'ijk456'),('Frankenstein', 'Mary Shelley', 'A classic Gothic novel about science and morality', 'en', '1818', 14.99, 27, 'lmn789'),('The Odyssey', 'Homer', 'An ancient Greek epic poem', 'en', '1999', 19.99, 23, 'opq012'),('The Shining', 'Stephen King', 'A horror novel about a haunted hotel', 'en', '1977', 31.99, 29, 'rst345'),('The Hunger Games', 'Suzanne Collins', 'A dystopian novel set in a post-apocalyptic world', 'en', '2008', 16.99, 33, 'uvw678'),('A Tale of Two Cities', 'Charles Dickens', 'A historical novel set during the French Revolution', 'en', '1859', 23.99, 36, 'xyz901'),('The Road', 'Cormac McCarthy', 'A post-apocalyptic novel about a father and sons journey', 'en', '2006', 25.99, 44, 'abc234'),('One Hundred Years of Solitude', 'Gabriel García Márquez', 'A magical realist novel about the Buendía family', 'en', '1967', 27.99, 50, 'def567'),('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 'A comedic science fiction series', 'en', '1979', 20.99, 22, 'ghi890'),('Wuthering Heights', 'Emily Brontë', 'A dark and passionate tale of love and revenge', 'en', '1847', 18.99, 28, 'jkl123'),('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'A psychological thriller novel', 'en', '2005', 29.99, 47, 'mno456'),('The Art of War', 'Sun Tzu', 'An ancient Chinese military treatise', 'en', '2005', 12.99, 18, 'pqr789'),('The Count of Monte Cristo', 'Alexandre Dumas', 'An adventure novel about revenge and redemption', 'en', '1844', 34.99, 31, 'stu012'),('The Picture of Dorian Gray', 'Oscar Wilde', 'A philosophical novel about the consequences of indulgence', 'en', '1890', 16.99, 39, 'vwx345'),('The Kite Runner', 'Khaled Hosseini', 'A novel about friendship, betrayal, and redemption', 'en', '2003', 21.99, 26, 'yzab678'),('The Grapes of Wrath', 'John Steinbeck', 'A novel about the struggles of the Joad family during the Great Depression', 'en', '1939', 24.99, 34, 'cde901'),('Crime and Punishment', 'Fyodor Dostoevsky', 'A psychological novel about morality and redemption', 'en', '1866', 28.99, 37, 'fgh234'),('The Brothers Karamazov', 'Fyodor Dostoevsky', 'A philosophical novel about family and morality', 'en', '1880', 30.99, 45, 'ijk567'),('The Scarlet Letter', 'Nathaniel Hawthorne', 'A novel about sin, guilt, and redemption in Puritan society', 'en', '1850', 19.99, 24, 'lmn890'),('The Sun Also Rises', 'Ernest Hemingway', 'A novel about the Lost Generation after World War I', 'en', '1926', 22.99, 32, 'opq123'),('Gone with the Wind', 'Margaret Mitchell', 'A historical novel set during the American Civil War', 'en', '1936', 26.99, 49, 'rst456'),('The Wind in the Willows', 'Kenneth Grahame', 'A classic children\'s novel about animal adventures', 'en', '1908', 14.99, 21, 'uvw789'),('The Silence of the Lambs', 'Thomas Harris', 'A psychological horror novel featuring Hannibal Lecter', 'en', '1988', 32.99, 41, 'xyz012');^
"

cd Fastapi-project1
start /b cmd /c python main.py

cd ..

cd library-front
start /b cmd /c ng serve --open

