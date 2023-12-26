# FastAPI with MongoDB and Docker Compose 🚀

## Acknowledgements 🙏

This example was created as a combination of the following examples:

- [MongoDB + Mongo Express using Docker and Docker Compose](https://github.com/nanlabs/devops-reference/tree/main/examples/compose-mongodb/): Dockerfile and compose.yml to run MongoDB and Mongo Express locally with initialization scripts.
- [FastAPI Complete CRUD Example](https://github.com/nanlabs/backend-reference/tree/main/examples/fastapi-crud/): Rest API that allows to create, read, update and delete employees and companies in the db, besides that, has endpoints to populate the db with Mock Data using faker.

## Requirements 🛠️

To get started, make sure you have the following tools installed on your machine:

- Docker 🐳
- Docker Compose 🐳
- Python 🐍

  **Python Version:** You'll need Python 3.12 installed on your local development machine. You can use [pyenv](https://github.com/pyenv/pyenv) to easily switch Python versions between different projects. If you're on Windows, consider using [pyenv-win](https://github.com/pyenv-win/pyenv-win).

  ```sh
  pyenv install
  pyenv local
  ```

### Gotchas for Certain Environments 🧐

Depending on your development environment, you may also need to create and activate a virtual environment for Python. Follow these steps:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.dev.txt
```

For Windows users using WSL2, ensure you have Docker Desktop installed, running, and configured with a [WSL2 connection](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers).

## Setup the Development Environment 🛠️

- Install the project dependencies:

  ```sh
  pip install -r requirements.dev.txt
  ```

- Install pre-commit hooks:

  ```sh
  pre-commit install
  ```

## Running the App 🏃‍♀️🏃‍♂️

To launch the app, simply run:

```sh
cp .env.example .env # Then Edit .env file with your own values
docker-compose up
```

Your app will be up and running in no time! 🚀🎉

This will start the following services:

- `web`: FastAPI server running at [http://localhost:80](http://localhost:80)
- `mongodb`: MongoDB server
- `mongo-express`: Mongo Express server running at [http://localhost:8081](http://localhost:8081)

### MongoDB Initialization

When the MongoDB container is started for the first time it will execute files with extensions `.sh` and `.js` that are found in `mongo/initdb.d/`. Files will be executed in alphabetical order. `.js` files will be executed by mongo using the database specified by the `MONGO_INITDB_DATABASE` variable, if it is present, or test otherwise. You may also switch databases within the `.js` script.
