# 🚀 Go API with Docker Compose 🌟

This project showcases a powerful and scalable Go API containerized with PostgreSQL using Docker Compose. Perfect for modern developers looking to leverage cutting-edge technology!

## 🎯 Why Use `sqlc`?

Integrating `sqlc` into your Go project brings a host of benefits:

- **🔒 Strong Type Safety**: Catch type errors early in the development process with compile-time checks, reducing runtime errors and boosting code reliability.
- **⚡ Enhanced Developer Productivity**: Automate the generation of SQL queries and corresponding Go code, freeing up time to focus on building amazing features.
- **📖 Improved Readability and Maintainability**: Use native SQL queries directly in your codebase for clearer, easier-to-understand queries that are simple to debug and optimize.
- **🚀 Optimized Performance**: Write and fine-tune raw SQL queries for superior control over database interactions, leading to more efficient query execution and better performance compared to ORM-based solutions.

## 🛠 Prerequisites

- Docker
- Docker Compose
- `sqlc`

## 📝 Setup Instructions

1. **🔗 Clone the Repository**:

    ```bash
    git clone https://github.com/nanlabs/backend-reference
    ```

2. **📂 Navigate to the Project Directory**:

    ```bash
    cd backend-reference/examples/golang-api-with-postgres-and-sqlc
    ```

3. **⚙️ Generate SQL Queries and Models with `sqlc`**:

    ```bash
    sqlc generate
    ```

4. **🐳 Build and Run the Docker Containers**:

    ```bash
    docker-compose build
    docker-compose up
    ```

🎉 Your Go API will be live at `localhost:8080`.

## ⏹ Stopping the Application

To gracefully stop the application and remove all containers, networks, and volumes defined in `docker-compose.yml`, run:

```bash
docker-compose down
docker volume rm db_data
```
