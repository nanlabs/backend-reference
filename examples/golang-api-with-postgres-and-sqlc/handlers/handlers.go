package handlers

import (
	"encoding/json"
	"fmt"
	"go-postgres-sqlc/db"
	"go-postgres-sqlc/db/sqlc"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	"github.com/jackc/pgx/v5/pgtype"
)

// Handlers holds the dependencies for the HTTP handlers.
type Handlers struct {
	DB *db.DB
}

// New initializes a new Handlers instance.
func New(db *db.DB) *Handlers {
	return &Handlers{
		DB: db,
	}
}

type ListUsersResponse struct {
	Users []User `json:"users"`
}
type User struct {
	ID        int64     `json:"id"`
	Username  string    `json:"username"`
	Email     string    `json:"email,omitempty"`
	CreatedAt time.Time `json:"createdAt"`
}

// ListUsers handles listing all users.
func (h *Handlers) ListUsers(rw http.ResponseWriter, r *http.Request) {
	users, err := h.DB.Queries.ListUsers(r.Context())
	if err != nil {
		writeError(rw, err, http.StatusInternalServerError)
		return
	}
	usersResponse := make([]User, len(users))
	for i, user := range users {
		usersResponse[i] = User{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email.String,
			CreatedAt: user.CreatedAt,
		}
	}
	writeResponse(rw, http.StatusOK, ListUsersResponse{Users: usersResponse})
}

type GetUserResponse User

// GetUser handles retrieving a user by ID.
func (h *Handlers) GetUser(rw http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.ParseInt(vars["id"], 10, 64)
	if err != nil {
		writeError(rw, fmt.Errorf("invalid user ID: %v", err), http.StatusBadRequest)
		return
	}
	user, err := h.DB.Queries.GetUser(r.Context(), id)
	if err != nil {
		writeError(rw, err, http.StatusInternalServerError)
		return
	}
	userResponse := GetUserResponse{
		ID:        user.ID,
		Username:  user.Username,
		Email:     user.Email.String,
		CreatedAt: user.CreatedAt,
	}
	writeResponse(rw, http.StatusOK, userResponse)
}

type CreateUserRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Email    string `json:"email,omitempty"`
}
type CreateUserResponse struct {
	ID        int64     `json:"id"`
	Username  string    `json:"username"`
	Password  string    `json:"password"`
	Email     string    `json:"email,omitempty"`
	CreatedAt time.Time `json:"createdAt"`
}

// CreateUser handles creating a new user.
func (h *Handlers) CreateUser(rw http.ResponseWriter, r *http.Request) {
	var user CreateUserRequest
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		writeError(rw, err, http.StatusUnprocessableEntity)
		return
	}
	newUser, err := h.DB.Queries.CreateUser(r.Context(), sqlc.CreateUserParams{
		Username: user.Username,
		Password: user.Password,
		Email:    NewText(user.Email),
	})
	if err != nil {
		writeError(rw, err, http.StatusInternalServerError)
		return
	}
	createUserResponse := CreateUserResponse{
		ID:        newUser.ID,
		Username:  newUser.Username,
		Password:  newUser.Password,
		Email:     newUser.Email.String,
		CreatedAt: newUser.CreatedAt,
	}
	writeResponse(rw, http.StatusCreated, createUserResponse)
}

// writeResponse writes the response as JSON to the ResponseWriter.
func writeResponse(rw http.ResponseWriter, statusCode int, data interface{}) {
	rw.Header().Set("Content-Type", "application/json")
	rw.WriteHeader(statusCode)
	if data != nil {
		err := json.NewEncoder(rw).Encode(data)
		if err != nil {
			http.Error(rw, "Failed to encode response: "+err.Error(), http.StatusInternalServerError)
		}
	}
}

type ErrorResponse struct {
	Message    string `json:"message"`
	StatusCode int    `json:"statusCode"`
}

// writeError writes an error response to the ResponseWriter.
func writeError(rw http.ResponseWriter, err error, statusCode int) {
	rw.Header().Set("Content-Type", "application/json+problem")
	rw.WriteHeader(statusCode)
	err = json.NewEncoder(rw).Encode(ErrorResponse{
		Message:    err.Error(),
		StatusCode: statusCode,
	})
	if err != nil {
		http.Error(rw, "Failed to encode response: "+err.Error(), http.StatusInternalServerError)
	}
}

func NewText(s string) pgtype.Text {
	if s == "" {
		return pgtype.Text{}
	}
	return pgtype.Text{
		String: s,
		Valid:  true,
	}
}
