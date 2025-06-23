<!--lint disable double-link awesome-heading awesome-git-repo-age awesome-toc-->

<div align="center">
<p>
    <img
        style="width: 200px"
        width="200"
        src="https://avatars.githubusercontent.com/u/4426989?s=200&v=4"
    >
</p>
<h1>Python Reference</h1>

[Changelog](#) |
[Contributing](./CONTRIBUTING.md)

</div>
<div align="center">

[![Awesome](https://awesome.re/mentioned-badge.svg)](https://github.com/nanlabs/awesome-nan)
[![Continious Integration][cibadge]][ciurl]
[![License: MIT][licensebadge]][licenseurl]

</div>

This repository contains different Backend related resources like applications, examples, libraries,
tools and more!

## Contents

- [Apps and Boilerplates](#apps-and-boilerplates)
- [Examples](#examples)
  - [Backend](#backend)
    - [CLI Tools](#cli-tools)
    - [FastAPI](#fastapi)
    - [ThirdParty Integrations](#thirdparty-integrations)
      - [Stripe](#stripe)
    - [Microservices](#microservices)
    - [SQLC](#sqlc)
  - [DevOps](#devops)
    - [Infrastructure as Code](#infrastructure-as-code)
      - [Serverless Framework, SAM and CloudFormation](#serverless-framework-sam-and-cloudformation)
    - [Containers, Orchestration and Serverless](#containers-orchestration-and-serverless)
      - [Containers and Compositions (Docker, Docker Compose, Buildpacks and more)](#containers-and-compositions-docker-docker-compose-buildpacks-and-more)

- [Contributing](#contributing)
- [Contributors](#contributors)

## Apps and Boilerplates

| Name                                                                                                                                                         | Description                                                                                                                                                                                                                                                                                       | Keywords                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [FastAPI Example with PostgreSQL and Serverless Framework](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-postgres-with-serverless) | A REST API built with FastAPI and PostgreSQL, deployed to AWS Lambda using the Serverless Framework. Includes database migrations with Alembic.                                                                                                                                                   | _Python3_, _FastAPI_, _PostgreSQL_, _Serverless_, _AWS Lambda_, _Alembic_                                                                                                                                                  |
| [FastAPI Simple example with Docker Compose and PIP](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-simple-docker-pip)              | A lightweight FastAPI example demonstrating containerization with Docker Compose and dependency management with PIP.                                                                                                                                                                              | _Python3_, _FastAPI_, _Docker_, _PIP_                                                                                                                                                                                      |
| [FastAPI with MongoDB and Docker Compose](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-mongo-with-docker-compose)                 | A REST API built with FastAPI and MongoDB, containerized using Docker Compose for seamless development and deployment.                                                                                                                                                                            | _Python3_, _FastAPI_, _MongoDB_, _Docker_, _Docker Compose_                                                                                                                                                                |
| [Golang REST API boilerplate](https://github.com/nanlabs/nancy.go/tree/main/examples/golang-todo-rest-crud/)                                                 | A comprehensive REST API boilerplate in Golang, featuring CRUD operations, structured logging, rate limiting, unit and integration tests, and API documentation with Swagger. Includes Docker Compose for MongoDB setup and tools like Gorilla Mux, Zap, and Mockery for streamlined development. | _Golang_, _REST API_, _MongoDB_, _Gorilla Mux_, _Go Swagger_, _Tollbooth_, _Zap_, _Viper_, _Mockery_, _Makefile_, _Pre-commit_, _Docker_, _Docker Compose_, _DockerTest_, _Swagger_, _Rate Limiting_, _Logging_, _Testing_ |
| [LangGraph SLS FastAPI RAG](https://github.com/nanlabs/backend-reference/tree/main/examples/langgraph-sls-fastapi-rag)                                       | A Proof of Concept (POC) for a Retrieval Augmented Generation (RAG) system using LangGraph, deployed with the Serverless Framework on AWS Lambda. It integrates FastAPI for API development and DynamoDB for state management.                                                                    | _Python3_, _FastAPI_, _LangGraph_, _Serverless Framework_, _AWS Lambda_, _DynamoDB_, _Docker_, _RAG_, _Retrieval Augmented Generation_                                                                                     |
| [SQLC with Go, PostgreSQL, Docker Compose](https://github.com/nanlabs/backend-reference/tree/main/examples/golang-api-with-postgres-and-sqlc)                | A REST API built with Go and SQLC, showcasing database operations with PostgreSQL and containerized development using Docker Compose.                                                                                                                                                             | _Golang_, _SQLC_, _PostgreSQL_, _Docker_, _Docker Compose_                                                                                                                                                                 |

## Examples

### Backend

#### CLI Tools

| Name                                                                                                                   | Description                                                                                                                                       | Keywords                                             |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [Python CLI Basic Example](https://github.com/nanlabs/backend-reference/tree/main/examples/cli-base)                   | A minimal Python CLI example showcasing how to create commands without requiring the explicit use of the Python interpreter or script path.       | _Python3_, _CLI_, _Command Line_                     |
| [Python CLI with Typer + Rich Example](https://github.com/nanlabs/backend-reference/tree/main/examples/cli-typer-base) | A Python CLI tool built with Typer and Rich, demonstrating interaction with external APIs for currency exchange rates and styled console outputs. | _Python3_, _Typer_, _Rich_, _API Integration_, _CLI_ |

#### FastAPI

| Name                                                                                                                                                         | Description                                                                                                                                                                                                                    | Keywords                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| [FastAPI Basic Example](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-base)                                                        | A simple REST API built with FastAPI that retrieves mock data using the Faker library, showcasing basic API development.                                                                                                       | _Python3_, _FastAPI_, _Faker_, _Mock Data_, _Pydantic_                                                                                 |
| [FastAPI Complete CRUD Example](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-crud)                                                | A complete CRUD API built with FastAPI, featuring endpoints for managing employees and companies, along with database population using Faker.                                                                                  | _Python3_, _FastAPI_, _CRUD_, _SQLAlchemy_, _Alembic_, _Docker_, _PostgreSQL_                                                          |
| [FastAPI Example with PostgreSQL and Serverless Framework](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-postgres-with-serverless) | A REST API built with FastAPI and PostgreSQL, deployed to AWS Lambda using the Serverless Framework. Includes database migrations with Alembic.                                                                                | _Python3_, _FastAPI_, _PostgreSQL_, _Serverless_, _AWS Lambda_, _Alembic_                                                              |
| [FastAPI GraphQL](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-gql)                                                               | A GraphQL API built with FastAPI and Strawberry, retrieving mock company data using the Faker library.                                                                                                                         | _Python3_, _FastAPI_, _GraphQL_, _Strawberry_, _Faker_                                                                                 |
| [FastAPI Simple example with Docker Compose and PIP](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-simple-docker-pip)              | A lightweight FastAPI example demonstrating containerization with Docker Compose and dependency management with PIP.                                                                                                           | _Python3_, _FastAPI_, _Docker_, _PIP_                                                                                                  |
| [FastAPI with MongoDB and Docker Compose](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-mongo-with-docker-compose)                 | A REST API built with FastAPI and MongoDB, containerized using Docker Compose for seamless development and deployment.                                                                                                         | _Python3_, _FastAPI_, _MongoDB_, _Docker_, _Docker Compose_                                                                            |
| [LangGraph SLS FastAPI RAG](https://github.com/nanlabs/backend-reference/tree/main/examples/langgraph-sls-fastapi-rag)                                       | A Proof of Concept (POC) for a Retrieval Augmented Generation (RAG) system using LangGraph, deployed with the Serverless Framework on AWS Lambda. It integrates FastAPI for API development and DynamoDB for state management. | _Python3_, _FastAPI_, _LangGraph_, _Serverless Framework_, _AWS Lambda_, _DynamoDB_, _Docker_, _RAG_, _Retrieval Augmented Generation_ |

#### ThirdParty Integrations

##### Stripe

| Name                                                                                                                                                  | Description                                                                                                                                            | Keywords                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| [Stripe Integration with Node.js and TypeScript](https://github.com/nanlabs/backend-reference/tree/main/examples/stripe-integration-node-typescript/) | A robust Stripe integration example using Node.js and TypeScript, enabling operations like customer creation, checkout sessions, and webhook handling. | _Node.js_, _TypeScript_, _Stripe_, _Payments_, _Webhooks_, _API Integration_ |

#### Microservices

| Name                                                                                                                                  | Description                                                                                                                  | Keywords                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [NestJS REST-based Microservices with NATS](https://github.com/nanlabs/backend-reference/tree/main/examples/nest-nats-microservices/) | A microservices architecture example using NestJS and NATS, demonstrating asynchronous messaging and request-reply patterns. | _Node.js_, _NestJS_, _Microservices_, _NATS_, _Messaging_, _REST_ |

#### SQLC

| Name                                                                                                                                          | Description                                                                                                                           | Keywords                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [SQLC with Go, PostgreSQL, Docker Compose](https://github.com/nanlabs/backend-reference/tree/main/examples/golang-api-with-postgres-and-sqlc) | A REST API built with Go and SQLC, showcasing database operations with PostgreSQL and containerized development using Docker Compose. | _Golang_, _SQLC_, _PostgreSQL_, _Docker_, _Docker Compose_ |

### DevOps

#### Infrastructure as Code

##### Serverless Framework, SAM and CloudFormation

| Name                                                                                                                                                         | Description                                                                                                                                                                                                                    | Keywords                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| [FastAPI Example with PostgreSQL and Serverless Framework](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-postgres-with-serverless) | A REST API built with FastAPI and PostgreSQL, deployed to AWS Lambda using the Serverless Framework. Includes database migrations with Alembic.                                                                                | _Python3_, _FastAPI_, _PostgreSQL_, _Serverless_, _AWS Lambda_, _Alembic_                                                              |
| [LangGraph SLS FastAPI RAG](https://github.com/nanlabs/backend-reference/tree/main/examples/langgraph-sls-fastapi-rag)                                       | A Proof of Concept (POC) for a Retrieval Augmented Generation (RAG) system using LangGraph, deployed with the Serverless Framework on AWS Lambda. It integrates FastAPI for API development and DynamoDB for state management. | _Python3_, _FastAPI_, _LangGraph_, _Serverless Framework_, _AWS Lambda_, _DynamoDB_, _Docker_, _RAG_, _Retrieval Augmented Generation_ |

#### Containers, Orchestration and Serverless

##### Containers and Compositions (Docker, Docker Compose, Buildpacks and more)

| Name                                                                                                                                            | Description                                                                                                                           | Keywords                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [FastAPI Simple example with Docker Compose and PIP](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-simple-docker-pip) | A lightweight FastAPI example demonstrating containerization with Docker Compose and dependency management with PIP.                  | _Python3_, _FastAPI_, _Docker_, _PIP_                       |
| [FastAPI with MongoDB and Docker Compose](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-mongo-with-docker-compose)    | A REST API built with FastAPI and MongoDB, containerized using Docker Compose for seamless development and deployment.                | _Python3_, _FastAPI_, _MongoDB_, _Docker_, _Docker Compose_ |
| [SQLC with Go, PostgreSQL, Docker Compose](https://github.com/nanlabs/backend-reference/tree/main/examples/golang-api-with-postgres-and-sqlc)   | A REST API built with Go and SQLC, showcasing database operations with PostgreSQL and containerized development using Docker Compose. | _Golang_, _SQLC_, _PostgreSQL_, _Docker_, _Docker Compose_  |

## Contributing

- Contributions make the open source community such an amazing place to learn, inspire, and create.
- Any contributions you make are **truly appreciated**.
- Check out our [contribution guidelines](./CONTRIBUTING.md) for more information.

## Contributors

<a href="https://github.com/nanlabs/backend-reference/contributors">
  <img src="https://contrib.rocks/image?repo=nanlabs/backend-reference" alt="Contributors"/>
</a>

Made with [contributors-img](https://contrib.rocks).

[cibadge]: https://github.com/nanlabs/backend-reference/actions/workflows/ci.yml/badge.svg
[licensebadge]: https://img.shields.io/badge/License-MIT-blue.svg
[ciurl]: https://github.com/nanlabs/backend-reference/actions/workflows/ci.yml
[licenseurl]: https://github.com/nanlabs/backend-reference/blob/main/LICENSE
