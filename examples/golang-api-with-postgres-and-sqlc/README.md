# Go API with Docker Compose

This project containerizes a Go API and a PostgreSQL database using Docker Compose.

## Motivation for Using `sqlc`

Incorporating `sqlc` into a Go project provides numerous advantages:

- **Strong Type Safety**: Compile-time checks ensure that type errors are caught early in the development process, reducing runtime errors and increasing code reliability.
- **Enhanced Developer Productivity**: By automating the generation of SQL queries and their corresponding Go code, `sqlc` allows developers to concentrate on building application features instead of writing boilerplate database interaction code.
- **Improved Readability and Maintainability**: Using native SQL queries directly in the codebase makes the queries more transparent and easier to understand, debug, and optimize. This approach aligns well with the principles of clean code and maintainability.
- **Optimized Performance**: `sqlc` enables developers to write and fine-tune raw SQL queries, providing greater control over database interactions compared to ORM-based solutions. This can lead to more efficient query execution and better overall performance.

## Prerequisites

- Docker
- Docker Compose
- `sqlc`

## Setup

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/nanlabs/backend-reference
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd backend-reference/examples/golang-api-with-postgres-and-sqlc
    ```

3. **Generate SQL Queries and Models with `sqlc`**:

    ```bash
    sqlc generate
    ```

4. **Build and Run the Docker Containers**:

    ```bash
    docker-compose build
    docker-compose up
    ```

The Go API will be accessible at `localhost:8080`.

## Stopping the Application

To stop the application and remove the containers, networks, and volumes defined in `docker-compose.yml`, run:

```bash
docker-compose down
docker volume rm db_data
```
