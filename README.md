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

[![Markdown Lint][markdownlintbadge]][markdownlinturl]
[![Shell Check][shellcheckbadge]][shellcheckurl]
[![License: MIT][licensebadge]][licenseurl]

</div>

This repository contains different Python apps that are used in different projects
here at [NaN Labs](https://www.nanlabs.com/).

- [Applications](#applications)
- [Examples](#examples)
  - [CLI Tools](#cli-tools)
  - [FastAPI Examples](#fastapi-examples)
  - [Other related examples](#other-related-examples)
- [Contributing](#contributing)
- [Contributors](#contributors)

## Applications

Collection of examples that were created as a composition of different examples that
can be found separately in the [examples](./examples/) directory.
Read more about the examples in the [examples](#examples) section.

## Examples

Collection of examples that solve specific problems using small pieces of code.

### CLI Tools

- [CLI Base Example](./examples/cli-base/README.md)
- [CLI with Typer + Rich Example](./examples/cli-typer-base/README.md)

### FastAPI Examples

- [FastAPI Base Example](./examples/fastapi-base/README.md)
- [FastAPI CRUD Example](./examples/fastapi-crud/README.md)
- [FastAPI GraphQL Example + MongoDB](./examples/fastapi-gql-mongo/README.md)
- [FastAPI PostgreSQL](./examples/fastapi-postgres/README.md)

### Other related examples

> **Note**: These examples are not part of this repository, but they are related
> and part of the same GitHub organization.

- [AWS Glue using Docker and Docker Compose](https://github.com/nanlabs/infra-reference/tree/main/examples/docker/glue/) - Dockerfile and docker-compose.yml for AWS Glue development with AWS Glue Libs, Spark, Jupyter Notebook, AWS CLI among other tools.
- [AWS Glue](https://github.com/nanlabs/infra-reference/tree/main/examples/devcontainers/glue/) - DevContainer for AWS Glue development. Uses `docker-compose` to run VSCode attached to a container with all the necessary tools to develop AWS Glue jobs such us AWS Glue Libs, Spark, Jupyter Notebook, AWS CLI among other tools.
- [AWS AppSync + Python](https://github.com/nanlabs/infra-reference/tree/main/examples/serverless/serverless-appsync-python/) - Serverless Framework example to deploy an AWS AppSync API using Python. It also has a local development environment using [Serverless Offline](https://www.serverless.com/plugins/serverless-offline).
- [AWS Glue with Python Shell and PySpark Jobs](https://github.com/nanlabs/infra-reference/tree/main/examples/serverless/serverless-glue/) - Serverless Framework example to deploy an AWS Glue job using Python Shell and PySpark.
- [Serverless S3 Local example](https://github.com/nanlabs/infra-reference/tree/main/examples/serverless/serverless-s3-local/) - Serverless Framework example to run a lambda function locally using [Serverless S3 Local](https://www.serverless.com/plugins/serverless-s3-local).

## Contributing

Contributions are welcome!

## Contributors

<a href="https://github.com/nanlabs/python-reference/contributors">
  <img src="https://contrib.rocks/image?repo=nanlabs/python-reference"/>
</a>

Made with [contributors-img](https://contrib.rocks).

[markdownlintbadge]: https://github.com/nanlabs/python-reference/actions/workflows/markdownlint.yml/badge.svg
[shellcheckbadge]: https://github.com/nanlabs/python-reference/actions/workflows/shellcheck.yml/badge.svg
[licensebadge]: https://img.shields.io/badge/License-MIT-blue.svg
[markdownlinturl]: https://github.com/nanlabs/python-reference/actions/workflows/markdownlint.yml
[shellcheckurl]: https://github.com/nanlabs/python-reference/actions/workflows/shellcheck.yml
[licenseurl]: https://github.com/nanlabs/python-reference/blob/main/LICENSE
