Телеграм бот для RT.

Для работы бота необходимо наличие MySQL сервера и 4 таблиц:

1. База данных пользователей Users:  <br/>
 Field     --- Type:  <br/>
 user_id     ---  char(32);   <br/>
first_name --- char(255); <br/>
last_name --- char(255); <br/>
phone_number --- char(32). <br/>

2. База данных запросов пользователей Notifications:  <br/>
 Field     --- Type:  <br/>
 user_id     ---  char(32);   <br/>
 notification  --- text; <br/>
date --- datetime.  <br/>

3. База данны для хранения всех слов (для проверки корректности). AllWords: <br/>
 Field     --- Type:  <br/>
 words     ---  char(255)  <br/>
 frequency  --- char(20)  <br/>


4. База данных для хранения стоп-слов. StopWords: <br/>
 Field     --- Type:  <br/>
 stopwords     ---  char(255)  <br/>