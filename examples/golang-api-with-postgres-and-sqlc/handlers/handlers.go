package handlers

import (
	"encoding/json"
	"go-postgres-sqlc/db"
	"go-postgres-sqlc/users"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

func ListUsers(res http.ResponseWriter, req *http.Request) {
	users, err := db.Queries.ListUsers(db.Context)
	if err != nil {
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(res).Encode(users)
}

func GetUser(res http.ResponseWriter, req *http.Request) {
	vars := mux.Vars(req)
	id, _ := strconv.Atoi(vars["id"])
	user, err := db.Queries.GetUser(db.Context, int32(id))
	if err != nil {
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(res).Encode(user)
}

func CreateUser(res http.ResponseWriter, req *http.Request) {
	user := users.User{}
	err := json.NewDecoder(req.Body).Decode(&user)
	db.Queries.CreateUser(db.Context, users.CreateUserParams{Username: user.Username, Password: user.Password, Email: user.Email})
	if err != nil {
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(res).Encode(user)
}
