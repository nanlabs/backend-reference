// main package include the entry point of the todo api application
package main

import (
	"log"
	"todo-api-golang/internal/config"
	"todo-api-golang/internal/platform/mongo"
	"todo-api-golang/internal/todo"
	"todo-api-golang/pkg/logs"

	"go.uber.org/zap"
)

// main is the entry point of the todo rest api.
func main() {
	logs, err := logs.New()
	if err != nil {
		log.Fatalf("Error initializing zap: %s\n", err)
	}

	config, err := config.LoadConfig("./../..")
	if err != nil {
		logs.Logger.Fatal("Cannot load config", zap.String("detail", err.Error()))
	}

	mongoClient, err := mongo.NewDbClient(config, logs)
	if err != nil {
		logs.Logger.Fatal("Error starting mongo client", zap.String("detail", err.Error()))
	}

	todoApi, err := todo.NewApi(config, logs, mongoClient)
	if err != nil {
		logs.Logger.Fatal("Cannot create ToDo API", zap.String("detail", err.Error()))
	}

	errC, err := todoApi.Start()
	if err != nil {
		logs.Logger.Fatal("Error starting ToDo API", zap.String("detail", err.Error()))
	}

	if err := <-errC; err != nil {
		logs.Logger.Fatal("Error while running ToDo API", zap.String("detail", err.Error()))
	}
}
