Телеграм бот для RT.

Для работы бота необходимо наличие MySQL сервера и 4 таблиц:

1. База данных пользователей Users:
+--------------+-----------+------+-----+---------+-------+
| Field        | Type      | Null | Key | Default | Extra |
+--------------+-----------+------+-----+---------+-------+
| user_id      | char(32)  | YES  |     | NULL    |       |
| first_name   | char(255) | YES  |     | NULL    |       |
| last_name    | char(255) | YES  |     | NULL    |       |
| phone_number | char(32)  | YES  |     | NULL    |       |
+--------------+-----------+------+-----+---------+-------+

2. База данных запросов пользователей Notifications:
+--------------+----------+------+-----+---------+-------+
| Field        | Type     | Null | Key | Default | Extra |
+--------------+----------+------+-----+---------+-------+
| user_id      | char(32) | YES  |     | NULL    |       |
| notification | text     | YES  |     | NULL    |       |
| date         | datetime | YES  |     | NULL    |       |
+--------------+----------+------+-----+---------+-------+

3. База данны для хранения всех слов (для проверки корректности). AllWords:\n
+-----------+-----------+------+-----+---------+-------+\n
| Field     | Type      | Null | Key | Default | Extra |\n
+-----------+-----------+------+-----+---------+-------+\n
| words     | char(255) | YES  |     | NULL    |       |\n
| frequency | char(20)  | YES  |     | NULL    |       |\n
+-----------+-----------+------+-----+---------+-------+\n

4. База данных для хранения стоп-слов. StopWords:
+-----------+-----------+------+-----+---------+-------+
| Field     | Type      | Null | Key | Default | Extra |
+-----------+-----------+------+-----+---------+-------+
| stopwords | char(255) | YES  |     | NULL    |       |
+-----------+-----------+------+-----+---------+-------+
