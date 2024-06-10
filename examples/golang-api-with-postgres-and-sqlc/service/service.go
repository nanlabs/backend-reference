package service

import (
	"context"
	"crypto/md5"
	"encoding/hex"
	"go-postgres-sqlc/model"
	"go-postgres-sqlc/repository"
)

type IUserService interface {
	CreateUser(ctx context.Context, user model.User) (model.User, error)
	GetUser(ctx context.Context, userID int64) (model.User, error)
	ListUsers(ctx context.Context) ([]model.User, error)
}

type UserService struct {
	repo repository.IUserRepository
}

func NewUser(repo repository.IUserRepository) IUserService {
	return &UserService{
		repo: repo,
	}
}

func (s *UserService) CreateUser(ctx context.Context, user model.User) (model.User, error) {
	user.Password = GetMd5(user.Password)
	newUser, err := s.repo.CreateUser(ctx, user)
	if err != nil {
		return model.User{}, err
	}
	return newUser, nil
}

func (s *UserService) GetUser(ctx context.Context, userID int64) (model.User, error) {
	user, err := s.repo.GetUser(ctx, userID)
	if err != nil {
		return model.User{}, err
	}
	return user, nil
}

func (s *UserService) ListUsers(ctx context.Context) ([]model.User, error) {
	users, err := s.repo.ListUsers(ctx)
	if err != nil {
		return nil, err
	}
	return users, nil
}

func GetMd5(input string) string {
	hash := md5.New()
	defer hash.Reset()
	hash.Write([]byte(input))
	return hex.EncodeToString(hash.Sum(nil))
}
