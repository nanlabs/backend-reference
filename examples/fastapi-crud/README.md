# CRUD FastAPI + Docker + Postgres + Alembic - PoC

This PoC was made using the following project as base:

- [FastApiBase](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-base)

---

## Prerequisites

- Python 3.10
- Docker 20.10
- Docker Compose 2.6

## Add .env file

In the root directory of the project create a `.env` file with the following fields:

```bash
TITLE=Title
VERSION=0.0.1
DEBUG=True
HOST=0.0.0.0
PORT=8000
ALLOW_ORIGINS='["*"]'
ALLOW_CREDENTIALS='["*"]'
ALLOW_METHODS='["*"]'
ALLOW_HEADERS='["*"]'
```

If this file is not added the project will use default variables to allow you run the application by default.

## Add .env.database

This file is required to run the Database's container.
In the root directory of the project create a `.env.database` file with the following fields:

```bash
POSTGRES_HOST=db-fastapi
POSTGRES_PORT=5432
POSTGRES_USER=fastapi
POSTGRES_PASSWORD=fastapi
POSTGRES_NAME=fastapi
PGADMIN_DEFAULT_EMAIL=fastapi@localhost.com
PGADMIN_DEFAULT_PASSWORD=fastapi
```

**IMPORTANT** The value of `POSTGRES_HOST` should be the name of the db container.

## How to run locally

- Open your terminal on the root project directory
- Run the command:

```bash
docker-compose up --build
```

In newer versions of docker run the previous command without dash as is shown below:

```bash
docker compose up --build
```

- To see docs ands schemas you can access:

  - OpenApi documentation

    ```bash
    http://0.0.0.0:8000/docs
    ```

  - ReDoc documentation:

    ```bash
    http://0.0.0.0:8000/redoc
    ```

- To access directly to DB in your browser go to:

```bash
  http://127.0.0.1:5050
```

PGAdmin credentials are in the `.env.database` file.

---

## How to create development environment

## Create venv

To create a Native Python virtual environment simply run the following command on the project's folder:

`python -m venv .venv --prompt fastapi`

## Install dependencies

Be sure you have the virtual environment active.
If not in the root folder of the project execute:
`source .venv/bin/activate`

Once the virtual environment is activated run:

- For development

  ```bash
  pip install -r requirements-dev.txt
  ```

- For production

  ```bash
  pip install -r requirements-prod.txt
  ```

## Install pre-commit

To install pre-commit in the .git hooks folder you only need to run the following command in the root folder of the project:

```bash
pre-commit install
```

## Create migration

```bash
alembic revision --autogenerate -m "<message>"
```

## Apply migration

**IMPORTANT**: This step is run when the containers are created, by entrypoint, so it would not be necessary to execute it manually.

`/scripts/startup.sh`

- In order to apply the last committed revision go inside `src` directory and execute the following command:

```bash
alembic upgrade head
```

- To apply one specific revision execute this command

```bash
alembic upgrade <revision_code>
```

---

## Create Mock data

In order to improve the testing experience 2 specific endpoints have been added to populate DB with mock data using faker library.

### Generate fake data in DB

In order to improve the testing experience, two specific endpoints have been added to populate DB with mock data using the Faker library:

- Generate fake companies in DB: `http://localhost:8000/api/v0/companies/mock-company/{quantity}`
- Generate fake employees in DB: `http://localhost:8000/api/v0/employees/mock-employee/{quantity}`

You can access these endpoints via the [Docs page](http://localhost:8000/docs#) or with Postman (in this case you must add the header `Accept: application/json`)

- `quantity` is an integer greater than 0 that specifies how many fake companies/employees should be created.
- The **response** is a list of all new companies/employees created with all their information.
- The `mock-employee` endpoint has an **optional query parameter** `company_id`. If it is sent, first checks if the company exists in DB, if so, it creates the specified quantity of new mock employees with that specific company id.
