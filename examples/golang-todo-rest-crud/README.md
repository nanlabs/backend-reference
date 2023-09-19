# ToDo API proof of concept

- [ToDo API proof of concept](#todo-api-proof-of-concept)
  - [Introduction](#introduction)
  - [Environment](#environment)
  - [Docker](#docker)
  - [Run](#run)
  - [Make File](#make-file)
  - [Unit test coverage](#unit-test-coverage)
  - [Integration test](#integration-test)
  - [Swagger](#swagger)
  - [Generate mocks](#generate-mocks)
  - [Graceful shutdown](#graceful-shutdown)
  - [Pre commit](#pre-commit)
  - [Project Layout](#project-layout)
  - [API Definition](#api-definition)
    - [Create Note](#create-note)
      - [Create Note Request](#create-note-request)
      - [Create Note Response](#create-note-response)
    - [Update Note](#update-note)
      - [Update Note Request](#update-note-request)
      - [Update Note Response](#update-note-response)
    - [Get Note](#get-note)
      - [Get Note Request](#get-note-request)
      - [Get Note Response](#get-note-response)
      - [Get Notes Request](#get-notes-request)
      - [Get Notes Response](#get-notes-response)
    - [Get Health](#get-health)
      - [Get Health Request](#get-health-request)
      - [Get Health Response](#get-health-response)
    - [Get Swagger UI](#get-swagger-ui)
      - [Get Swagger UI Request](#get-swagger-ui-request)
  - [Logging](#logging)
    - [Log levels](#log-levels)
    - [Log body](#log-body)
    - [Example of Create Note Request](#example-of-create-note-request)
    - [Example of Create Note Request Logging](#example-of-create-note-request-logging)
    - [Example of Create Note Response Logging](#example-of-create-note-response-logging)
    - [Example of Fatal level error when .env file is missing](#example-of-fatal-level-error-when-env-file-is-missing)
    - [Example of Error level error when 500 error occurs](#example-of-error-level-error-when-500-error-occurs)
  - [Rate Limiting](#rate-limiting)
    - [Get Health Rate Limit](#get-health-rate-limit)
      - [Get Health Request Rate Limit](#get-health-request-rate-limit)
      - [Get Health Response Rate Limit](#get-health-response-rate-limit)
  - [Trace](#trace)
    - [Get Health Trace](#get-health-trace)
      - [Get Health Request Without Trace Id](#get-health-request-without-trace-id)
      - [Get Health Response With Trace Id](#get-health-response-with-trace-id)
      - [Get Health Request With Trace Id](#get-health-request-with-trace-id)
      - [Get Health Response With System Trace Id](#get-health-response-with-system-trace-id)

## Introduction

Welcome! 👋

The purpose of this project is to make a simple proof of concept of a RESTful API using Go and gorilla/mux.

You should visit Go's website [here](https://go.dev/) if you have yet to meet Go. For instructions on how to install Go, see the docs [here](https://go.dev/learn/).

We developed this project using Go v1.9.4

## Environment

We used the [Viper]("https://github.com/spf13/viper") library to handle environment variables, and reading these from `.env`, `.json`, or `.yaml` files,

The `.env.example` file is included in the root directory to provide development environment variables. Rename it to `.env` to make it usable.

## Docker

We used the [NaN Labs Devops reference](https://github.com/nanlabs/devops-reference/tree/main/examples/docker/mongodb) repository to create MongoDB and MongoDB Express containers.

## Run

To run the code, you will need docker and docker-compose installed on your machine; see the docs [here](https://docs.docker.com/get-started/08_using_compose/). In the project root, run `docker compose up --build -d` or `make dcbuild` if you have make installed to create and start all the containers.

> Executing the entire solution in containers requires the 'MONGO_HOST' env variable to be set to 'mongodb', like this: MONGO_HOST=mongodb

To run the TODO API on your local environment, and have it consuming MongoDB on Docker, use the command `go run ./cmd/todo` or `make run`, to make it work.

> Executing the TODO API on the local environmet requires the 'MONGO_HOST' env variable to be set to 'localhost', like this: MONGO_HOST=localhost

After that, you have a RESTful API that is running at `http://127.0.0.1:8080`.

## Make File

The [Make File]("https://linuxhint.com/install-make-ubuntu/") library was used to make a list of useful commands.

- `make build`                  run go build
- `make run`                    run go run
- `make unittest`               run go unit tests with coverage
- `make integrationtest`        run go integration tests package
- `make check_swagger_install`  define a dependency to install go-swagger cli
- `make swagger`                run go generate to generate swagger .yaml and json
- `make check_mockery_install`  define a dependency to install mockery cli
- `make mocks`                  run go generate to generate mocks of interfaces with go generate tag
- `make dcbuild`                run all the containers

## Unit test coverage

Use the command `make unittest` to run all the unit tests, including coverage.

## Integration test

We used the [Dockertest]("https://github.com/ory/dockertest") package to perform integrations tests. The idea behind this is to create two containers, one for the TODO API, and one for MongoDB; effectively separating the integration environment from the development environment. Run the integration tests by making requests to the test api, and finally deleting both containers.

Use the command `make integrationtest` to run all the integration tests.

## Swagger

We choose [Go swagger]("https://goswagger.io/") for the api documentation. Using the "design first" approach, the documentation can be generated through code annotations.

To install mockery CLI, run `go install github.com/go-swagger/go-swagger/cmd/swagger`.

Use the command `make swagger` to generate the `/docs/swagger.yaml` and `third_party/swagger-ui-4.11.1/swagger.json` files from the go-swagger models.

## Generate mocks

We used [Mockery]("https://github.com/vektra/mockery") to generate the mocks.

Run `go install github.com/vektra/mockery/v2@latest` to install mockery CLI.

Use the command `make mocks` to generate the mocks of the interfaces in `/internal/todo/note` folder.

## Graceful shutdown

A `graceful shutdown in a process` is when the OS (operating system) can safely shutdown its processes and close all connections, taking as much time as needed.

To be able to achieve that, one has to listen to [Termination signals]("https://www.gnu.org/software/libc/manual/html_node/Termination-Signals.html") that are sent to the application by the process manager, and act accordingly. A delay of 30 seconds was implemented at the moment of listening for a termination signal in order to shut down the server.

## Pre commit

To maintain high code quality we opted to use [Pre commit]("https://pre-commit.com/") which allows to run hooks to automatically point out problems in code such as missing semicolons, trailing whitespace, and debug statements. It can also be configured to run tests, linter, dependency checking and other commands.

It can be installed using python running `pip install pre-commit`

Check the `.pre-commit-config.yaml` file to see the hooks

More details on [Pre Commit Golang]("https://github.com/dnephin/pre-commit-golang")

## Project Layout

The project uses the following project layout:

```text
.
├── cmd                main applications
│   └── todo             api server setup
├── docs               api documentation
├── test               non-unit tests
│   └── integration      integration tests
├── internal           private application and library code
│   ├── config           configuration library
│   ├── platform         provide support for databases, authentication
│   │     └── mongo         mongo client
│   ├── ratelimit        api rate limiting
│   ├── todo             todo related features
│   │     └── note          note related features
│   └── trace          package for generating request and trace ids
├── pkg                public library code
│   ├── apierror         standard api errors
│   ├── encode           encode and decode helpers
│   ├── health           health check definition
│   └── logs             logs setup
└── third_party        third party libraries
     └── swagger-ui        static files from swagger ui

```

The top level directories `cmd`, `internal`, `pkg` are commonly found in other popular Go projects, as explained in
[Standard Go Project Layout](https://github.com/golang-standards/project-layout) and [Package Oriented Design]("https://www.ardanlabs.com/blog/2017/02/package-oriented-design.html").

Within `internal` and `pkg`, packages are structured by features in order to achieve the so-called
[screaming architecture](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html). For example,
the `todo` directory contains the application logic related with the todo feature.

Within each feature package, code are organized in layers (handlers, service, repository), following the dependency guidelines as described in the [clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).

## API Definition

### Create Note

#### Create Note Request

```js
POST api/v1/notes
```

```json
{
    "name": "Go to the bank",
    "description":"Schedule an appointment to the bank",
}
 ```

#### Create Note Response

```js
201 Created
```

```json
{
    "name": "Go to the bank",
    "description":"Schedule an appointment to the bank",
    "status":"To Do",
}
 ```

### Update Note

#### Update Note Request

 ```js
PATCH /api/v1/notes/{noteId}
```

```json
{
    "name": "Go shopping",
    "description":"Buy groceries for the week",
    "status" : "In Progress"
}
```

#### Update Note Response

```js
204 No Content
```

### Get Note

#### Get Note Request

```js
GET /api/v1/notes/{noteId}
```

#### Get Note Response

```js
200 Ok
```

```json
{
    "name": "Go shopping",
    "description":"Buy groceries for the week",
    "status" : "In Progress"
}
```

#### Get Notes Request

```js
GET api/v1/notes
```

#### Get Notes Response

```js
200 Ok
```

```json
[
  {
    "name": "Go shopping",
    "description":"Buy groceries for the week",
    "status" : "To Do"
  },
  {
    "name": "Go to the bank",
    "description":"Schedule an appointment to the bank",
    "status" : "In Progress"
  },
]
```

### Get Health

#### Get Health Request

```js
GET /api/v1/health
```

#### Get Health Response

```js
200 Ok
```

```json
{
    "status" : "Healthy"
}
```

### Get Swagger UI

#### Get Swagger UI Request

```js
GET /api/v1/swagger/
```

## Logging

Logging plays a vital role in identifying issues, evaluating performances, and knowing the process status within the application. For this reason it was decided to select structured logging, using Uber's library [Zap](https://github.com/uber-go/zap).

### Log levels

For simplicity it was decided to use three types of log levels

- `Info`  Generally useful information to log.
- `Error` Anything that can potentially cause application oddities including 50x server errors.
- `Fatal` Any error that is forcing a shutdown of the service or application to prevent data loss.

### Log body

The log itself is a json structure with the following keys

- `level`       define log level
- `ts`          define log timestamp
- `caller`      define the file where the log was called
- `msg`         define the main info of the log
- `method`      define the request method
- `url`         define the resource called in the api
- `statusCode`  define the response status code
- `duration`    define the duration of the request in nanoseconds
- `detail`     define extra error information
- `stacktrace`  define extra trace information

Logging was included at the beginning and end of the requests in order to maintain traceability.

### Example of Create Note Request

```js
POST api/v1/notes
```

```json
{
    "name": "Go to the bank",
    "description":"Schedule an appointment to the bank",
}
 ```

### Example of Create Note Request Logging

```json
{
    "level": "info",
    "ts": 1674960805.3700233,
    "caller": "todo/middleware.go:64",
    "msg": "Start http request",
    "method": "POST",
    "url": "/api/v1/notes"
}
 ```

### Example of Create Note Response Logging

```json
{
    "level": "info",
    "ts": 1674960805.3718014,
    "caller": "todo/middleware.go:87",
    "msg": "Finish http request",
    "method": "POST",
    "url": "/api/v1/notes",
    "statusCode": 201,
    "duration": 0.0017783
}
 ```

### Example of Fatal level error when .env file is missing

```json
{
    "level": "fatal",
    "ts": 1674963617.935728,
    "caller": "todo/main.go:29",
    "msg": "Cannot load config",
    "detail": "Config File \".env\" Not Found in \"[C:\\\\Users\\\\User\\\\Documents\\\\todo-api-golang C:\\\\Users\\\\User\\\\Documents\\\\todo-api-golang\\\\cmd\\\\todo]\"",
    "stacktrace": "main.main\n\tC:/Users/User/Documents/todo-api-golang/cmd/todo/main.go:29\nruntime.main\n\tC:/Program Files/Go/src/runtime/proc.go:250"
}
 ```

### Example of Error level error when 500 error occurs

In this case a body of the response is included to provide additional information in order to identify the issue.

```json
{
    "level": "error",
    "ts": 1674965353.375559,
    "caller": "todo/middleware.go:84",
    "msg": "Finish http request",
    "method": "POST",
    "url": "/api/v1/notes",
    "statusCode": 500,
    "duration": 0.0005219,
    "body": "{\"type\":\"INTERNAL\",\"message\":\"Internal server error.\",\"code\":500,\"detail\":\"error creating note id\"}\n",
    "stacktrace": "todo-api-golang/internal/todo.LogMiddleware.func1.1\n\tC:/Users/Chelo/Documents/todo-api-golang/internal/todo/middleware.go:84\nnet/http.HandlerFunc.ServeHTTP\n\tC:/Program Files/Go/src/net/http/server.go:2109\ngithub.com/gorilla/mux.(*Router).ServeHTTP\n\tC:/Users/Chelo/go/pkg/mod/github.com/gorilla/mux@v1.8.0/mux.go:210\nnet/http.serverHandler.ServeHTTP\n\tC:/Program Files/Go/src/net/http/server.go:2947\nnet/http.(*conn).serve\n\tC:/Program Files/Go/src/net/http/server.go:1991"
}
 ```

## Rate Limiting

Rate limiting is a technique used to control the number of requests a user can make to an API over a given period of time. Using the library [Toolbooth]("https://github.com/didip/tollbooth") which provides a simple API to perform rate limiting.

It can be configured by the following client variables

- `HTTP_RATE_LIMIT=3`
- `HTTP_RATE_INTERVAL=second`
- `INTEGRATION_HTTP_RATE_LIMIT=100`
- `INTEGRATION_HTTP_RATE_INTERVAL=minute`

The interval has the values as listed below

- `second` default value
- `minute`
- `hour`

### Get Health Rate Limit

#### Get Health Request Rate Limit

```js
GET /api/v1/health
```

#### Get Health Response Rate Limit

```js
429 Too Many Requests
```

```text
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Ratelimit-Limit: 3
Ratelimit-Remaining: 0
Ratelimit-Reset: 1
X-Rate-Limit-Duration: 1
X-Rate-Limit-Limit: 3.00
X-Rate-Limit-Request-Remote-Addr: 172.25.0.1:54948
```

```json
{
  "type":"TOO_MANY_REQUEST",
  "message":"You have reached maximum request limit.",
  "code":429
}
```

## Trace

To maintain the traceability of a request it is always useful to use unique identifiers when generating logs and calling other services. That is why the use of `X-Request-Id` and `X-Trace-Id` was implemented, when entering a request to the api will automatically generate a unique identifier `X-Request-Id`, then it will be verified in the header if there is any trace identifier `X-Trace-Id`, if there is one it will be kept the same if not it will be assigned the `X-Request-Id`, both identifiers will be transmitted in the context of the request, and both will be returned in the request response as headers.

### Get Health Trace

#### Get Health Request Without Trace Id

```js
GET /api/v1/health
```

#### Get Health Response With Trace Id

```js
200 Ok
```

```text
X-Request-Id: 3d54f2f9-4418-4e50-90c6-d5209dc25d5d
X-Trace-Id: 3d54f2f9-4418-4e50-90c6-d5209dc25d5d
```

```json
{
    "status" : "Healthy"
}
```

#### Get Health Request With Trace Id

```js
GET /api/v1/health
```

```text
X-Trace-Id: trace id from other system
```

#### Get Health Response With System Trace Id

```js
200 Ok
```

```text
X-Request-Id: 3d54f2f9-4418-4e50-90c6-d5209dc25d5d
X-Trace-Id: trace id from other system
```

```json
{
    "status" : "Healthy"
}
```
