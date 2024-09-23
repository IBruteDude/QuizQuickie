-- setup the app's mysql user and db

CREATE DATABASE IF NOT EXISTS `quizquickie_db`;

CREATE USER IF NOT EXISTS 'quizquickie_usr'@'localhost' IDENTIFIED BY 'quizquickie_pwd';

GRANT ALL PRIVILEGES ON `quizquickie_db`.* TO 'quizquickie_usr'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
