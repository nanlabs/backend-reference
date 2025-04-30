
# Music Licensing Platform Backend

This is the backend service for the Music Licensing Workflow application. It provides both REST and GraphQL APIs, along with WebSocket support for real-time updates.

This application is built using **FastAPI**, **Strawberry GraphQL**, **SQLAlchemy**, **Pydantic**, and **PostgreSQL**.

## Key Features

* **REST API**: Comprehensive set of RESTful endpoints for CRUD operations on movies, songs, scenes, and licenses.
* **GraphQL API**: A flexible GraphQL API that allows for detailed queries and mutations, enhancing data retrieval and manipulation.
* **WebSocket Support**: Real-time updates for license statuses, ensuring that clients are always up-to-date with the latest changes.
* **Database Integration**: Robust PostgreSQL database to store and manage all application data.
* **Docker Support**: Containerized deployment with Docker and Docker Compose for easy setup and scalability.

## Tech Stack

* **Python 3.11**: The core programming language for the backend.
* **FastAPI**: High-performance web framework for building APIs.
* **Strawberry GraphQL**: Library for creating GraphQL APIs in Python.
* **SQLAlchemy**: Powerful ORM for database interaction.
* **Pydantic**: Data validation and settings management using Python type annotations.
* **PostgreSQL**: Robust relational database management system.
* **WebSockets**: For real-time communication and updates.

## Project Structure

The project is organized as follows:

## Setup

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Set up environment variables:

```bash
cp env.example .env
# Edit .env with your configuration
```

- Run the application:

```bash
uvicorn src.main:app --reload
```

## API Documentation

- REST API: <http://localhost:8000/docs>
- GraphQL Playground: <http://localhost:8000/api/graphql>

## Docker

To run the application using Docker:

```bash
docker-compose up --build
```

## API Endpoints

### REST API

- `GET /api/movies` - List all movies
- `GET /api/movies/?id={id}` - Get movie details
- `GET /api/movies/scenes` - Get all scenes
- `GET /api/movies/scenes/?id={id}` - Get scene details

### GraphQL

#### Queries

- allMovies: [Movie!]!
- movie(id: ID!): Movie
- scene(id: ID!): Scene
- allScenes: [Scene!]!
- allLicenseStatus: [LicenseStatus!]!
 -song(id: ID!): Song

#### Mutations

- updateSong(id: ID!, licenseStatus: LicenseStatusEnum = null): Song

### WebSocket

- `ws://localhost:8000/api/graphql` - example WebSocket endpoint for real-time license status updates
