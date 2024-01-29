# Library Management API


## Technologies

Python, FastAPI, PostgreSQL, Alembic, Docker, Redis

## Installation

- create .env file in root with your settings according to .env.example

- install docker

- run application with its dependencies in docker containers
```
docker-compose up -d --build
```

- run database migrations
```
docker exec -it api alembic -c alembic.ini upgrade head
```

- create admin if needed
```
docker exec -it api python -m app.main createadmin
```

## Testing

- dont forget to change settings if you want to use test database here: 
alembic.ini, docker-compose.yaml, .env

- run tests
```
docker exec -it api coverage run -m pytest
```

- check coverage
```
docker exec -it api coverage report -m 
```