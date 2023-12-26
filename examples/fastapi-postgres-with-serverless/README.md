# FastAPI Example with PostgreSQL and Serverless Framework 🚀

We use [Serverless](https://www.serverless.com/) to deploy our API to AWS Lambda.

## Acknowledgements 🙏

This example was created as a combination of the following examples:

- [PostgreSQL using Docker and Docker Compose](https://github.com/nanlabs/devops-reference/tree/main/examples/compose-postgres/): Dockerfile and compose.yml to run PostgreSQL locally with initialization scripts.
- [Serverless S3 Local](https://github.com/nanlabs/devops-reference/tree/main/examples/serverless-s3-local/): Serverless Framework example to run a lambda function locally using [Serverless S3 Local](https://www.serverless.com/plugins/serverless-s3-local).

## Requirements

**You’ll need to have Node 18.17.0 or later on your local development machine** (but it’s not required on the server). You can use [fnm](https://github.com/Schniz/fnm) to easily switch Node versions between different projects.

```sh
fnm use
npm install
```

**You'll also need to have Python 3.9 installed on your local development machine**. You can use [pyenv](https://github.com/pyenv/pyenv) to easily switch Python versions between different projects. If you are using Windows, you should use [pyenv-win](https://github.com/pyenv-win/pyenv-win).

```sh
pyenv install
pyenv local
```

### Gotchas for Certain Environments

**Depending on your dev environment, it may also be necessary to create and initiate a virtualenv for python**. Do so by running the below commands:

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

For windows user using WSL2, you may also need to have Docker Desktop installed, running, and with the [WSL2 connection](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers) set up.

## Local Development

In order to develop locally, you'll need to install the dependencies and run the application using Serverless Offline.

### Install Dependencies

```sh
npm run sls requirements install
```

### Run the Database Locally

We use Docker Compose to run the database locally. You can check the directory [postgres/](./postgres/README.md) for more information
about the database setup for local development.

### Run the Application

This repo has a local development set up that uses the file `.env.local` to configure the local environment.
Run the following command to start the local development server:

```sh
npm run sls:offline
```

### Using S3 Offline

We use the plugin `serverless-s3-local` to emulate S3 locally. First, using aws configure set up a new profile, i.e. `aws configure --profile s3local`. The default creds are

```sh
aws_access_key_id = S3RVER
aws_secret_access_key = S3RVER
```

then you can interact with S3 locally doing the following:

```sh
aws --endpoint-url=http://localhost:8000 s3 cp .gitignore s3://s3-local-extra/ --profile s3local
```

## Deployment

To deploy the app to AWS, you'll first need to configure your AWS credentials. There are many ways
to set your credentials, for more information refer to the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

Once set you can deploy your app using the serverless framework with:

```sh
npm run sls:deploy -- --verbose --stage <stage>
```
