# NestJS REST-based Microservices with NATS

![NaNLABS Logo](/images/logo1.svg)
![NestJS Logo](https://nestjs.com/img/logo_text.svg)
![NATS Logo](https://nats.io/img/logos/nats-horizontal-color.png)

## Introduction

Welcome to the NestJS REST-based Microservices with NATS proof-of-concept (POC) repository! This project demonstrates the implementation of a microservices architecture using NestJS, a progressive Node.js framework, along with NATS for asynchronous event-based as well as synchronous request-reply messaging patterns.

This repository does not make use of Jeststream, the stream and persistence layer built on top of NATS. To see that in action please refer to [this repository](TBD)

## Table of Contents

- [NestJS REST-based Microservices with NATS](#nestjs-rest-based-microservices-with-nats)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
  - [Getting Started](#getting-started)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Resources](#resources)

## Technologies Used

This POC showcases the utilization of the following technologies:

- [NestJS](https://nestjs.com/): A powerful Node.js framework crafted for building efficient and scalable server-side applications.
- [NATS](https://nats.io/): A lightweight and high-performance messaging system that provides various messaging patterns.

## Getting Started

To get started with this POC:

1. Clone the repository: `git clone git@github.com:nanlabs/backend-reference.git`
2. Navigate to the project directory: `cd examples/nest-nats-microservices`
3. Start NATS server and all 3 sample microservices in 🐳 Docker `docker-compose up`
4. (Optional) Activate compose `watch` mode `docker compose alpha watch`
5. Follow the instructions in the [Usage](#usage) section to run and test the microservices.

## Project Structure

The project is structured as follows:

```text
project-root/
│
├── service-a/
│   ├── src/
│   │   └── ...
│   └── ...
│
├── service-b/
│   ├── src/
│   │   └── ...
│   └── ...
|
├── service-c/
│   ├── src/
│   │   └── ...
│   └── ...
│
└── ...
```

Each microservice is contained within its own directory and follows a similar structure with controllers, services, and other relevant components.

## Usage

1. Start NATS server and all 3 sample microservices in 🐳 Docker `docker-compose up`
2. Navigate to a specific microservice directory: `cd service-a`
3. Explore the implemented REST-based endpoints and messaging patterns.
4. Refer to the [Resources](#resources) section for more in-depth information on NATS and NestJS.

Service **A** contains 2 resources (resource 1 and resource 2) and exposes a RESTful API with public CRUD methods.

### Event based communication

Sending a _POST_ http request to `/resource1` will broadcast a `resource1_created` event which will be handled by Service **B**, outputting data in the console. This is an example of event-based asynchronous communication.

### Request-response based communication

Sending a _GET_ http request to `/resource2` will send a message and await for a reply. Service **C** will handle the message and respond. Service **A** will output the response to the client. This is an example of syncronous communication.

## Contributing

Contributions are welcome! If you find any issues or want to enhance this POC, feel free to open a pull request. Please review our [Contribution Guidelines](CONTRIBUTING.md) before getting started.

## Resources

- [NestJS Documentation](https://docs.nestjs.com/)
- [NATS Documentation](https://docs.nats.io/)

---

**Disclaimer**: This repository is a proof-of-concept and should be used for educational and illustrative purposes. It does not represent a production-ready application. Use at your own risk.
