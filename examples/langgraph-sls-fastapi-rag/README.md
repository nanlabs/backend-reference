# RAG LangGraph POC with Serverless and FastAPI 🚀

This repository contains a Proof of Concept (POC) for a Retrieval Augmented Generation (RAG) system using LangGraph, deployed with Serverless Framework on AWS Lambda.

## Acknowledgements 🙏

This POC was created by NaNLABS, drawing inspiration from:

- [LangGraph RAG Examples](https://github.com/langchain-ai/langgraph-examples): For RAG implementation patterns
- [FastAPI Serverless Examples](https://github.com/nanlabs/devops-reference/tree/main/examples/serverless-fastapi/): For API structure and deployment strategies
- [LocalStack Integration Examples](https://github.com/nanlabs/devops-reference/tree/main/examples/localstack-resources/): For local AWS service emulation

## Requirements 🛠️

To get started, make sure you have the following tools installed on your machine:

- Docker 🐳
- Docker Compose 🐳
- Python 🐍

  **Python Version:** You'll need Python 3.12 installed on your local development machine. You can use [pyenv](https://github.com/pyenv/pyenv) to easily switch Python versions between different projects. If you're on Windows, consider using [pyenv-win](https://github.com/pyenv-win/pyenv-win).

### Using pipenv

We recommend using `pipenv` to manage project dependencies and create virtual environments. Install pipenv globally using your package manager (e.g., `pip install pipenv`). Then, navigate to your project directory and run:

```sh
pipenv install
```

This will create a virtual environment and install all the required dependencies listed in `Pipfile.lock`.

### Gotchas for Certain Environments 🧐

Depending on your development environment, pipenv might automatically handle virtual environment creation. However, for some setups, you may still need to activate it manually:

```sh
pipenv shell
```

For Windows users using WSL2, ensure you have Docker Desktop installed, running, and configured with a [WSL2 connection](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers).

## Setup the Development Environment 🛠️

- Install the project dependencies:

  ```sh
  pre-commit install --dev
  ```

## Running the App 🏃‍♀️🏃‍♂️

To launch the app, simply run:

```sh
cp .env.example .env.local # Then edit .env.local file with your own values
```

Your app will be up and running in no time! 🚀🎉

This will start the following services:

- `web`: FastAPI server running at [http://localhost:3000](http://localhost:3000)
- `localstack`: LocalStack services running at [http://localhost:4566](http://localhost:4566)

### Running with Docker 🐳

If you prefer to run the application using Docker, we provide Docker support out of the box:

1. Build the Docker image:

   ```sh
   docker build -t rag-langgraph-api .
   ```

2. Run the container:

   ```sh
   docker run -p 3000:3000 --env-file .env.local rag-langgraph-api
   ```

### Running with Docker Compose 🐳

For a more complete development environment that includes all services, use Docker Compose:

1. Start all services:

   ```sh
   docker-compose up
   ```

2. Start in detached mode (run in background):

   ```sh
   docker-compose up -d
   ```

3. View logs:

   ```sh
   docker-compose logs -f
   ```

4. Stop all services:

   ```sh
   docker-compose down
   ```

The Docker Compose setup includes:

- FastAPI application
- LocalStack for AWS services emulation
- Any additional services defined in docker-compose.yml

## Running with LangGraph Studio 🎨

LangGraph Studio provides a powerful UI for visualizing, testing, and debugging your RAG agents. To use it:

1. Install the LangGraph CLI:

   ```sh
   pip install "langgraph-cli[inmem]"
   ```

2. Start the development server:

   ```sh
   npx @langchain/langgraph-cli@latest dev
   ```

This will:

- Start the LangGraph server at `http://127.0.0.1:2024`
- Automatically open Studio in your browser

Alternatively, you can manually access Studio by visiting:
`https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

### Features

- Visualize your RAG flows and agent graphs
- Test your RAG pipeline by running it from the UI
- Debug your retrieval and generation steps
- View embeddings and vector representations
- Create and manage assistants
- Track context window utilization
- View and manage threads
- Add node input/outputs to LangSmith datasets for testing

## Deployment 🚀

To deploy the application to AWS, follow these steps:

1. Configure AWS Credentials:

   ```sh
   aws configure
   ```

   Enter your AWS Access Key ID, Secret Access Key, and preferred region.

2. Install Serverless Framework globally:

   ```sh
   npm install -g serverless
   ```

3. Deploy to AWS:

   ```sh
   serverless deploy --stage prod
   ```

   This will:
   - Package your application
   - Create necessary AWS resources (Lambda, API Gateway, etc.)
   - Deploy your API to AWS Lambda

4. After successful deployment, you'll receive:
   - API Gateway endpoint URL
   - Lambda function ARN
   - Other AWS resource details

### Environment Variables for Production 🔐

Before deploying, ensure you've set up the following:

1. Create a production environment file:

   ```sh
   cp .env.example .env.prod
   ```

2. Update the production environment variables with appropriate values

3. Use AWS Secrets Manager or Parameter Store to securely store sensitive environment variables

### Monitoring and Logs 📊

- View Lambda logs:

  ```sh
   serverless logs -f app -t
  ```

- Monitor your application using AWS CloudWatch

For more detailed deployment information and advanced configurations, check out our [deployment documentation](./docs/deployment.md).
