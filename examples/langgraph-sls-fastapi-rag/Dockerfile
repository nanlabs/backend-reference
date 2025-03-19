# Stage 1: Build development dependencies
FROM python:3.12.0 AS builder-dev

WORKDIR /code

# Install system dependencies for psycopg2 and pipenv
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        libpq-dev \
        gcc=4:12.2.0-3 \
    && pip install --no-cache-dir --upgrade pip==24.1.2 \
    && pip install --no-cache-dir pipenv==2024.0.1

# Copy Pipfiles
COPY Pipfile Pipfile.lock ./

# Install development dependencies
RUN pipenv install --dev --system --deploy



# Stage 2: Build production dependencies
FROM python:3.12.0-alpine AS builder-prod

WORKDIR /code

# Install system dependencies for psycopg2 and pipenv
RUN apk update \
    && apk add --no-cache \
        postgresql15-dev=15.7-r0 \
        gcc=12.2.1_git20220924-r10 \
        musl-dev=1.2.4-r2 \
    && pip install --no-cache-dir --upgrade pip==24.1.4 \
    && pip install --no-cache-dir pipenv==2024.0.1

# Copy Pipfiles
COPY Pipfile Pipfile.lock ./

# Install production dependencies
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system

# Stage 3: Final image
FROM python:3.12.0-alpine as production

WORKDIR /code

# Install runtime dependencies for psycopg2
RUN apk update \
    && apk add libpq=15.7-r0

# Copy production dependencies from builder-prod stage
COPY --from=builder-prod /usr/local /usr/local

# Copy the application code
COPY ./app ./app

# Create a non-root user to run the application
RUN adduser -D -H nonroot

# Switch to the non-root user
USER nonroot

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Stage 4: Lambda function
FROM public.ecr.aws/lambda/python:3.12 as lambda

WORKDIR ${LAMBDA_TASK_ROOT}

# Install system dependencies for psycopg2 and pipenv
RUN dnf install -y \
        postgresql-devel \
        gcc-11.4.1-2.amzn2023.0.2.x86_64 \
    && pip install --no-cache-dir --upgrade pip==24.1.2 \
    && pip install --no-cache-dir pipenv==2024.0.1 \
    && dnf clean all

# Copy Pipfiles
COPY Pipfile Pipfile.lock ${LAMBDA_TASK_ROOT}/

# Install production dependencies
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

# Copy the lambda handler code
COPY . ${LAMBDA_TASK_ROOT}

CMD ["app/main.handler"]
