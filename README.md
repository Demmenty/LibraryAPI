# Library Management API


## Technologies

Python, FastAPI, PostgreSQL, Alembic, Docker, Redis

## Installation

- create .env file with your settings according to .env.example
- install docker

- run application in docker containers
```
docker-compose up -d --build
```

- run database migrations
```
docker exec -it api alembic -c alembic.ini upgrade head
```

- create admin
```
docker exec -it api python -m app.main createadmin
```

- run tests
- (change setting for using test database!)
```
docker exec -it api python -m pytest
```
