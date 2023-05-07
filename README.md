# API service for library written on DRF

## Features implemented:
1. CRUD functionality for Books, Users and Borrowings services
2. Create custom permission
3. JWT token authentication 
4. Filtering by active borrowings or by user (only for admin)
5. Return Borrowing functionality (custom action)
6. Implement the possibility of sending notifications via Telegram chatbot on each Borrowing creation 
7. Implement a daily-based function for checking borrowings overdue via Celery and if exist sending notifications to Telegram chat


## Installing using GitHub

1. Install PostgresSQL and create db
2. Copy this repository, by using your terminal:

```shell
git clone https://github.com/yanpurdenko/drf-library.git
```
3. Change directory
```shell
cd drf-library
```
4. Install venv, and activate it by using following commands:
```shell
python -m venv venv
```
to activate on Mac and Linux:
```shell
source venv/bin/activate
```
to activate on Windows:
```shell
venv\scripts\activate
```
5. Install dependencies (requirements):
```shell
pip install -r requirements.txt
```
6. Create file .env and change environment variables to yours as in .env.sample.


7. Run migrations to initialize database. Use this command:
```shell
python manage.py migrate
```
8. Run server
```shell
python manage.py runserver
```


## Run with docker

Docker should be installed

```shell
docker-compose build
docker-compose up
```
Alos use http://127.0.0.1:8000/ url instead of http://0.0.0.0:8000/


## Getting access

- create user via /api/users/tpken/
- get access token via /api/user/token/


## How to try it out
1. When you received access token, authorize with it on /api/doc/swagger/ and execute all endpoints
2. Or you can install ModHeader extension in Google Chrome and create request header with value Bearer `<Your access token>`
