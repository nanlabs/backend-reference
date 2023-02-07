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

[![Continious Integration][cibadge]][ciurl]
[![License: MIT][licensebadge]][licenseurl]

</div>

This repository contains different Python apps that are used in different projects
here at [NaN Labs](https://www.nanlabs.com/).

## Contents

- [Examples](#examples)

  - [DevOps](#devops)
    - [Shell Scripting and CLI Tools](#shell-scripting-and-cli-tools)
  - [Backend](#backend)
    - [FastAPI](#fastapi)

- [Contributing](#contributing)
- [Contributors](#contributors)

## Examples

### DevOps

#### Shell Scripting and CLI Tools

- [Python CLI Basic Example](https://github.com/python-reference/tree/main/examples/cli-base) - Basic structure to create a command without passing the python command and the python file's path. _Keywords: Python3, PyCMD_
- [Python CLI with Typer + Rich Example](https://github.com/python-reference/tree/main/examples/cli-typer-base) - Interaction with an external API, to retrieve some currencies exchange rates, make conversion returning styled console output. _Keywords: Python3, Requests, Rich, Typer_

### Backend

#### FastAPI

- [FastAPI Basic Example](https://github.com/python-reference/tree/main/examples/fastapi-base) - Rest API that retrieves mock data using Faker library. _Keywords: Python3, Faker, Factory-Boy, FastAPI, Pydantic_
- [FastAPI Complete CRUD Example](https://github.com/python-reference/tree/main/examples/fastapi-crud) - Rest API that allows to create, read, update and delete employees and companies in the db, besides that, has endpoints to populate the db with Mock Data using faker. _Keywords: Python3, Faker, FastAPI, Pydantic, SQLAlchemy, Alembic, Docker, Docker Compose, PGAdmin, PostgreSQL_
- [FastAPI GraphQL](https://github.com/python-reference/tree/main/examples/fastapi-gql) - GraphQL API that retrieves fake companies using Faker library. _Keywords: Python3, Factory-boy, Faker, FastAPI, Pydantic, Strawberry-graphql_

## Contributing

- Contributions make the open source community such an amazing place to learn, inspire, and create.
- Any contributions you make are **truly appreciated**.
- Check out our [contribution guidelines](./CONTRIBUTING.md) for more information.

## Contributors

<a href="https://github.com/nanlabs/python-reference/contributors">
  <img src="https://contrib.rocks/image?repo=nanlabs/python-reference"/>
</a>

Made with [contributors-img](https://contrib.rocks).

[cibadge]: https://github.com/nanlabs/python-reference/actions/workflows/ci.yml/badge.svg
[licensebadge]: https://img.shields.io/badge/License-MIT-blue.svg
[ciurl]: https://github.com/nanlabs/python-reference/actions/workflows/ci.yml
[licenseurl]: https://github.com/nanlabs/python-reference/blob/main/LICENSE
