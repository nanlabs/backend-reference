package main

import (
	"go-postgres-sqlc/db"
	"go-postgres-sqlc/handlers"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	db := db.New("postgres://postgres:postgres@db:5432/poc?sslmode=disable")
	runMigrations(db)

	handlers := handlers.New(db)

	router := mux.NewRouter()
	base := router.PathPrefix("/api").Subrouter()

	base.HandleFunc("/user", handlers.ListUsers).Methods(http.MethodGet)
	base.HandleFunc("/user/{id:[0-9]+}", handlers.GetUser).Methods(http.MethodGet)
	base.HandleFunc("/user", handlers.CreateUser).Methods(http.MethodPost)

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
