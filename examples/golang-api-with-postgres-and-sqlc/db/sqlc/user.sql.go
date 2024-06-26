// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.26.0
// source: user.sql

package sqlc

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5/pgtype"
)

const createUser = `-- name: CreateUser :one
INSERT INTO users (
  username,
  password,
  email
) VALUES (
  $1,
  $2,
  $3
) RETURNING id, username, password, email, created_at
`

type CreateUserParams struct {
	Username string
	Password string
	Email    pgtype.Text
}

func (q *Queries) CreateUser(ctx context.Context, arg CreateUserParams) (User, error) {
	row := q.db.QueryRow(ctx, createUser, arg.Username, arg.Password, arg.Email)
	var i User
	err := row.Scan(
		&i.ID,
		&i.Username,
		&i.Password,
		&i.Email,
		&i.CreatedAt,
	)
	return i, err
}

const getUser = `-- name: GetUser :one
SELECT 
  id,
  username,
  email,
  created_at
FROM users
WHERE id = $1
LIMIT 1
`

type GetUserRow struct {
	ID        int64
	Username  string
	Email     pgtype.Text
	CreatedAt time.Time
}

func (q *Queries) GetUser(ctx context.Context, userID int64) (GetUserRow, error) {
	row := q.db.QueryRow(ctx, getUser, userID)
	var i GetUserRow
	err := row.Scan(
		&i.ID,
		&i.Username,
		&i.Email,
		&i.CreatedAt,
	)
	return i, err
}

const listUsers = `-- name: ListUsers :many
SELECT 
  id,
  username,
  email,
  created_at
FROM users
ORDER BY username
`

type ListUsersRow struct {
	ID        int64
	Username  string
	Email     pgtype.Text
	CreatedAt time.Time
}

func (q *Queries) ListUsers(ctx context.Context) ([]ListUsersRow, error) {
	rows, err := q.db.Query(ctx, listUsers)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	items := []ListUsersRow{}
	for rows.Next() {
		var i ListUsersRow
		if err := rows.Scan(
			&i.ID,
			&i.Username,
			&i.Email,
			&i.CreatedAt,
		); err != nil {
			return nil, err
		}
		items = append(items, i)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return items, nil
}
