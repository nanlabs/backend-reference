# Build stage
FROM golang:1.22 AS builder

WORKDIR /go/src/app

# Pre-copy/cache go.mod and go.sum for pre-downloading dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go application
RUN go build -v -o /go/bin/app .

# Final stage
FROM gcr.io/distroless/base-debian12:latest

# Copy the compiled binary from the build stage
COPY --from=builder /go/bin/app /

# Expose the application port
EXPOSE 8080

# Set the command to run the application
CMD ["/app"]
