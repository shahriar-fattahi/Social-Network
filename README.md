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
> [Entity-Relationship Code link](https://dbdiagram.io/d/65a7c776ac844320ae1d14da)
![sn_db](https://github.com/shahriar-fattahi/Social-Network/assets/109045277/4f2617e4-a759-44f3-9336-956bc87e6e10)


## Getting Started
1. Clone this repository to your local machine:
```
git clone https://github.com/shahriar-fattahi/Social-Network
```

2- SetUp venv
```
python3 -m venv venv
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
