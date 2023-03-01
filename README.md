# Проектное задание: Docker-compose

Проект по докеризации и развртыванию сервисов онлайн кинотеатра, который является домашней работой по курсу Яндекс.Практикума Мидл Python-разработчик. 
Включает: 
- Базу данных Postgres (.ddl файл в папке postgresql) 
- Панель админа для добавления новых фильмов, актеров, жанров с использованием Django
- Пример переноса данных из SQLite в Postgres (/admin/data)
- Проверку переноса данных с использованием PyTest (/admin/test)
- ElasticSearch для организации полнотексового поиска по фильмам 
- ETL для переноса данных из Postgres в ElasticSearch (elastic/etl)
- Movie API для доступа к данным ElasticSearch, написанный на FastAPI (movei_api)

# Запуск проекта в тестовом режиме

`docker compose -d --build up`

`docker compose up`

Адмика живет по адресу: http://127.0.0.1/admin login: admin, password: 123qwe.
Movie API swagger документация http://127.0.0.1/movie/api/v1/docs можно поискать Star

