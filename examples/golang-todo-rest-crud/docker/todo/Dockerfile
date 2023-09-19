# Build stage
FROM golang:1.19-buster AS builder
WORKDIR /build

# Copy module files first so that they don't need to be downloaded again if no change
COPY go.* ./
RUN go mod download
RUN go mod verify

# Copy source files and build the binary
COPY . .
RUN go build -o todo ./cmd/todo

# Run stage
FROM gcr.io/distroless/base-debian11

WORKDIR /build

COPY --from=builder /build/todo .
COPY --from=builder /build/.env .
COPY --from=builder /build/third_party/swagger-ui-4.11.1 /build/third_party/swagger-ui-4.11.1

USER nonroot:nonroot

CMD ["/build/todo"]

