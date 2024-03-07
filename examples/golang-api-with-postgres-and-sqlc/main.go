package main

import (
	"go-postgres-sqlc/handlers"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	db.CreateUserTable()

	mux := mux.NewRouter()
	mux.HandleFunc("/api/user", handlers.ListUsers).Methods("GET")
	mux.HandleFunc("/api/user/{id:[0-9]+}", handlers.GetUser).Methods("GET")
	mux.HandleFunc("/api/user", handlers.CreateUser).Methods("POST")

	log.Fatal(http.ListenAndServe(":8080", mux))

}
