# Go API with Docker Compose

This project is a Go API that uses PostgreSQL as its database. The application and the database are containerized using Docker Compose.

## Prerequisites

- Docker
- Docker Compose
- sqlc

## Setup

1. Clone the repository:

```bash
git clone https://github.com/nanlabs/backend-reference
```

2. Navigate to the project directory

```bash
cd backend-reference/examples/golang-api-with-postgres-and-sqlc
```

3. We are using [sqlc](https://docs.sqlc.dev/en/stable/index.html) to generate the queries and models.
To generate the queries run

```bash
sqlc generate
```

3. Build and run the Docker containers: 

```bash
docker-compose build
```

4. Run the containers

```bash
docker-compose up
```



The Go API will be accessible at localhost:8080.

## Stopping the Application
To stop the application and remove the containers, networks, and volumes defined in docker-compose.yml, run the following command:

```bash
docker-compose down
```
