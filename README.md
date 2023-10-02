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

- [Contributing](#contributing)
- [Contributors](#contributors)

## Apps and Boilerplates

| Name                                                                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                     | Keywords                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Golang REST API boilerplate](https://github.com/nanlabs/nancy.go/tree/main/examples/golang-todo-rest-crud/) | REST API to create, update and retrieve Entities, including graceful shutdown, rate limiting, structured logging, unit tests, integration tests, environment variables, health check and API documentation with swagger. Technologies: Golang 1.19, MongoDB (with Docker Compose), Gorilla Mux, Go Swagger, Tollbooth (rate limiting), Zap (logging), Viper, Mockery, Makefile, Pre-commit, and DockerTest (integration tests). | _Golang_, _REST API_, _MongoDB_, _Gorilla Mux_, _Go Swagger_, _Tollbooth_, _Zap_, _Viper_, _Mockery_, _Makefile_, _Pre-commit_, _Docker_, _Docker Compose_, _DockerTest_ |

## Examples

### Backend

#### CLI Tools

| Name                                                                                                                   | Description                                                                                                                    | Keywords                               |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| [Python CLI Basic Example](https://github.com/nanlabs/backend-reference/tree/main/examples/cli-base)                   | Basic structure to create a command without passing the python command and the python file's path.                             | _Python3_, _PyCMD_                     |
| [Python CLI with Typer + Rich Example](https://github.com/nanlabs/backend-reference/tree/main/examples/cli-typer-base) | Interaction with an external API, to retrieve some currencies exchange rates, make conversion returning styled console output. | _Python3_, _Requests_, _Rich_, _Typer_ |

#### FastAPI

| Name                                                                                                          | Description                                                                                                                                                           | Keywords                                                                                                                |
| ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [FastAPI Basic Example](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-base)         | Rest API that retrieves mock data using Faker library.                                                                                                                | _Python3_, _Faker_, _Factory-Boy_, _FastAPI_, _Pydantic_                                                                |
| [FastAPI Complete CRUD Example](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-crud) | Rest API that allows to create, read, update and delete employees and companies in the db, besides that, has endpoints to populate the db with Mock Data using faker. | _Python3_, _Faker_, _FastAPI_, _Pydantic_, _SQLAlchemy_, _Alembic_, _Docker_, _Docker Compose_, _PGAdmin_, _PostgreSQL_ |
| [FastAPI GraphQL](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-gql)                | GraphQL API that retrieves fake companies using Faker library.                                                                                                        | _Python3_, _Factory-boy_, _Faker_, _FastAPI_, _Pydantic_, _Strawberry-graphql_                                          |

#### ThirdParty Integrations

##### Stripe

| Name                                                                                                                                                  | Description                                                                                                                                                                                                                                                                                    | Keywords                                                                               |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [Stripe Integration with Node.js and TypeScript](https://github.com/nanlabs/backend-reference/tree/main/examples/stripe-integration-node-typescript/) | This project offers a seamless Stripe integration with Node.js and TypeScript, providing a powerful API for managing basic operations like customer creation, checkout sessions, and portal sessions. It empowers developers to effortlessly handle payment-related tasks with the Stripe API. | _Node.js_, _TypeScript_, _Stripe_, _Payment Gateway_, _API_, _Integration_, _Webhooks_ |

#### Microservices

| Name                                                                                                                                  | Description                                                                                                                                                                                                                       | Keywords                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [NestJS REST-based Microservices with NATS](https://github.com/nanlabs/backend-reference/tree/main/examples/nest-nats-microservices/) | This project demonstrates the implementation of a microservices architecture using NestJS, a progressive Node.js framework, along with NATS for asynchronous event-based as well as synchronous request-reply messaging patterns. | _Microservices_, _Node.js_, _NestJS_, _NATS_, _REST_, _Messaging Patterns_, _Proof of Concept_ |

## Contributing

- Contributions make the open source community such an amazing place to learn, inspire, and create.
- Any contributions you make are **truly appreciated**.
- Check out our [contribution guidelines](./CONTRIBUTING.md) for more information.

## Contributors

<a href="https://github.com/nanlabs/backend-reference/contributors">
  <img src="https://contrib.rocks/image?repo=nanlabs/backend-reference"/>
</a>

Made with [contributors-img](https://contrib.rocks).

[cibadge]: https://github.com/nanlabs/backend-reference/actions/workflows/ci.yml/badge.svg
[licensebadge]: https://img.shields.io/badge/License-MIT-blue.svg
[ciurl]: https://github.com/nanlabs/backend-reference/actions/workflows/ci.yml
[licenseurl]: https://github.com/nanlabs/backend-reference/blob/main/LICENSE
