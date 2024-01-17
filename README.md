# Social Network
A social network API built using Django Rest Framework.

## About Project
This project is based on the description of this file([ASSIGNMENT.MD](https://github.com/shahriar-fattahi/Social-Network/blob/main/ASSIGNMENT.md)).  In short, in this social network, users can share their desired post with their followers.

## Built with
- Django
- Django Rest Framework

## Technologies Used
- Docker
- Redis
- PostgreSQL
- Celery

## ER Diagram
Database Relationship diagram generated using [dbdiagram](https://dbdiagram.io/home)
> [Entity-Relationship Code link](https://dbdiagram.io/d/E-commerce-6561c3da3be1495787b58a33)
![E-commerce](https://github.com/shahriar-fattahi/django-ecommerce-api/assets/109045277/4d650bd8-3db8-4c4c-82ff-6a8ffc2afe99)

## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd Social Network
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```
