// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.26.0

package sqlc

import (
	"time"

	"github.com/jackc/pgx/v5/pgtype"
)

type User struct {
	ID        int64
	Username  string
	Password  string
	Email     pgtype.Text
	CreatedAt time.Time
}