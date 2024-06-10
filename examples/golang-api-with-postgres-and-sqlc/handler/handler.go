package handler

import (
	"encoding/json"
	"fmt"
	"go-postgres-sqlc/model"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"

	"go-postgres-sqlc/service"
)

// UserHandler holds the dependencies for the HTTP handlers.
type UserHandler struct {
	userSvc service.IUserService
}

// NewUser initializes a new Handlers instance.
func NewUser(userSvc service.IUserService) *UserHandler {
	return &UserHandler{
		userSvc: userSvc,
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
func (h *UserHandler) ListUsers(rw http.ResponseWriter, r *http.Request) {
	users, err := h.userSvc.ListUsers(r.Context())
	if err != nil {
		writeError(rw, err, http.StatusInternalServerError)
		return
	}
	usersResponse := make([]User, len(users))
	for i, user := range users {
		usersResponse[i] = User{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			CreatedAt: user.CreatedAt,
		}
	}
	writeResponse(rw, http.StatusOK, ListUsersResponse{Users: usersResponse})
}

type GetUserResponse User

// GetUser handles retrieving a user by ID.
func (h *UserHandler) GetUser(rw http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.ParseInt(vars["id"], 10, 64)
	if err != nil {
		writeError(rw, fmt.Errorf("invalid user ID: %v", err), http.StatusBadRequest)
		return
	}
	user, err := h.userSvc.GetUser(r.Context(), id)
	if err != nil {
		writeError(rw, err, http.StatusInternalServerError)
		return
	}
	userResponse := GetUserResponse{
		ID:        user.ID,
		Username:  user.Username,
		Email:     user.Email,
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
	Email     string    `json:"email,omitempty"`
	CreatedAt time.Time `json:"createdAt"`
}

// CreateUser handles creating a new user.
func (h *UserHandler) CreateUser(rw http.ResponseWriter, r *http.Request) {
	var createUserReq CreateUserRequest
	err := json.NewDecoder(r.Body).Decode(&createUserReq)
	if err != nil {
		writeError(rw, err, http.StatusUnprocessableEntity)
		return
	}
	user := model.User{
		Username: createUserReq.Username,
		Password: createUserReq.Password,
		Email:    createUserReq.Email,
	}
	newUser, err := h.userSvc.CreateUser(r.Context(), user)
	if err != nil {
		writeError(rw, err, http.StatusInternalServerError)
		return
	}
	createUserResponse := CreateUserResponse{
		ID:        newUser.ID,
		Username:  newUser.Username,
		Email:     newUser.Email,
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
	rw.Header().Set("Content-Type", "application/problem+json")
	rw.WriteHeader(statusCode)
	err = json.NewEncoder(rw).Encode(ErrorResponse{
		Message:    err.Error(),
		StatusCode: statusCode,
	})
	if err != nil {
		http.Error(rw, "Failed to encode response: "+err.Error(), http.StatusInternalServerError)
	}
}
