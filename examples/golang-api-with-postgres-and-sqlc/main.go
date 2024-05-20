package main

import (
	"go-postgres-sqlc/db"
	"go-postgres-sqlc/handler"
	"log"
	"net/http"

	"go-postgres-sqlc/repository"
	"go-postgres-sqlc/service"

	"github.com/gorilla/mux"
)

func main() {
	db := db.New("postgres://postgres:postgres@db:5432/poc?sslmode=disable")
	runMigrations(db)

	userRepo := repository.NewUser(db)
	userSvc := service.NewUser(userRepo)
	userHandler := handler.NewUser(userSvc)

	router := mux.NewRouter()
	base := router.PathPrefix("/api").Subrouter()

	base.HandleFunc("/user", userHandler.ListUsers).Methods(http.MethodGet)
	base.HandleFunc("/user/{id:[0-9]+}", userHandler.GetUser).Methods(http.MethodGet)
	base.HandleFunc("/user", userHandler.CreateUser).Methods(http.MethodPost)

	err := http.ListenAndServe(":8080", base)
	if err != nil {
		log.Fatal(err)
	}
}

func runMigrations(db *db.DB) {
	query := `CREATE TABLE IF NOT EXISTS users (
		id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		username VARCHAR(30) NOT NULL,
		password VARCHAR(100) NOT NULL,
		email VARCHAR(50),
		created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
	)`
	_, err := db.Conn.Exec(db.Context, query)
	if err != nil {
		log.Fatalf("Failed to create users table: %v", err)
	}
	log.Println("Users table created or already exists.")
}
