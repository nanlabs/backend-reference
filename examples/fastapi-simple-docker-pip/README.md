# Example Fast API

This repository contains the source code for the note-go API. The API is built using FastAPI.

## Requirements 🛠️

To get started, make sure you have the following tools installed on your machine:

- [Docker](https://www.docker.com/) for local development.
- [Docker Compose](https://docs.docker.com/compose/) to manage multi-container Docker applications.
- [pyenv](https://github.com/pyenv/pyenv) to easily switch Python versions between different projects.
- [Pipenv](https://pipenv.pypa.io/en/latest/) to manage Python dependencies.

  **Python Version:** You'll need Python 3.12 installed on your local development machine. You can use [pyenv](https://github.com/pyenv/pyenv) to easily switch Python versions between different projects. If you're on Windows, consider using [pyenv-win](https://github.com/pyenv-win/pyenv-win).

## ⚡️ Quickstart

**Install Python**, **Python Dependencies**, and set the **Pre-commit Hooks**

```sh
pyenv install
pyenv local
pipenv install --dev
pipenv run pre-commit install
pipenv shell
```

## Running the App 🏃‍♀️🏃‍♂️

To launch the app, simply run:

```sh
cp .env.example .env.local # Then edit .env.local file with your own values
./scripts/ctl --backend # You can run ./bin/ctl --help to see all available commands
```

Your app will be up and running in no time! 🚀🎉

This will start the following services:

- `web`: FastAPI server running at [http://localhost:8000](http://localhost:8000)
