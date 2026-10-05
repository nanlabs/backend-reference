# FastAPI Example with PostgreSQL and Serverless Framework 🚀

We use [Serverless](https://www.serverless.com/) to deploy our API to AWS Lambda.

## Acknowledgements 🙏

This example was created as a combination of the following examples:

- [PostgreSQL using Docker and Docker Compose](https://github.com/nanlabs/devops-reference/tree/main/examples/compose-postgres/): Dockerfile and compose.yml to run PostgreSQL locally with initialization scripts.

## Requirements

**You’ll need Node.js 20 or later and a Serverless Framework account** on your local development machine. Serverless Framework v4 requires authentication; run `npx serverless login` before using the commands below. You can use [fnm](https://github.com/Schniz/fnm) to switch Node versions between projects.

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

This example has a local development setup that uses the file `.env.local` to configure the local environment.
Run the following command to start the local development server:

```sh
npm run sls:offline
```

### Using S3 locally

The sample provisions its S3 bucket when deployed to AWS. Local S3 emulation is currently unsupported in this example. Its former plugin dependency had unresolved critical vulnerabilities, so this sample no longer installs an emulator. Use the deployed AWS bucket for S3 operations until a safe local emulator is documented.

## Deployment

To deploy the app to AWS, you'll first need to configure your AWS credentials. There are many ways
to set your credentials, for more information refer to the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

Once set you can deploy your app using the serverless framework with:

```sh
npm run sls:deploy -- --verbose --stage <stage>
```
