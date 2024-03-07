# This Dockerfile is used to build a Docker image for a Go application with PostgreSQL.
# It sets the working directory to /go/src/app, copies the application code into the container,
# installs the dependencies using go get, and builds the application using go install.
# The resulting executable is set as the command to run when the container starts.

FROM golang:1.22

WORKDIR /go/src/app

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
COPY go.mod go.sum ./

# RUN go get -d -v ./...
RUN go mod download && go mod verify

COPY . .

# RUN go install -v ./...
RUN go build -v -o /usr/local/bin/app .

EXPOSE 8080

CMD ["app"]
