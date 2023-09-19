# HELP =================================================================================================================
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## Display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

build:
	@go build -o bin/todo ./cmd/todo

run: build
	@./bin/todo
.PHONY: run

unittest:
	@go test -v ./... -cover
.PHONY: unittest

integrationtest:
	@go clean -testcache
	@go test -v ./test/integration --tags=integration
.PHONY: integrationtest

check_swagger_install:
	which swagger || go install github.com/go-swagger/go-swagger/cmd/swagger
swagger: check_swagger_install
	swagger generate spec -o ./docs/swagger.yaml --scan-models
	swagger generate spec -o ./third_party/swagger-ui-4.11.1/swagger.json --scan-models
.PHONY: swagger

check_mockery_install:
	which mockery || go install github.com/vektra/mockery/v2@latest
mocks: check_mockery_install
	go generate ./...
.PHONY: mocks

dcbuild:
	docker compose up --build -d
.PHONY: dcbuild

