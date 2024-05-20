package repository

import (
	"context"
	"go-postgres-sqlc/db"
	"go-postgres-sqlc/db/sqlc"
	"go-postgres-sqlc/model"

	"github.com/jackc/pgx/v5/pgtype"
)

type IUserRepository interface {
	CreateUser(ctx context.Context, user model.User) (model.User, error)
	GetUser(ctx context.Context, userID int64) (model.User, error)
	ListUsers(ctx context.Context) ([]model.User, error)
}

type UserRepository struct {
	db *db.DB
}

func NewUser(db *db.DB) IUserRepository {
	return &UserRepository{
		db: db,
	}
}

func (r *UserRepository) CreateUser(ctx context.Context, user model.User) (model.User, error) {
	userRepo, err := r.db.Queries.CreateUser(ctx, sqlc.CreateUserParams{
		Username: user.Username,
		Password: user.Password,
		Email:    NewText(user.Email),
	})
	if err != nil {
		return model.User{}, err
	}
	newUser := model.User{
		ID:        userRepo.ID,
		Username:  userRepo.Username,
		Email:     userRepo.Email.String,
		CreatedAt: userRepo.CreatedAt,
	}
	return newUser, nil
}

func (r *UserRepository) GetUser(ctx context.Context, userID int64) (model.User, error) {
	userRepo, err := r.db.Queries.GetUser(ctx, userID)
	if err != nil {
		return model.User{}, err
	}
	user := model.User{
		ID:        userRepo.ID,
		Username:  userRepo.Username,
		Email:     userRepo.Email.String,
		CreatedAt: userRepo.CreatedAt,
	}
	return user, nil
}

func (r *UserRepository) ListUsers(ctx context.Context) ([]model.User, error) {
	var users []model.User
	usersRepo, err := r.db.Queries.ListUsers(ctx)
	if err != nil {
		return users, err
	}
	for _, userRepo := range usersRepo {
		user := model.User{
			ID:        userRepo.ID,
			Username:  userRepo.Username,
			Email:     userRepo.Email.String,
			CreatedAt: userRepo.CreatedAt,
		}
		users = append(users, user)
	}
	return users, nil
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
