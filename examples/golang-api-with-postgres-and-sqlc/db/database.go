package db

import (
	"context"
	"go-postgres-sqlc/db/sqlc"
	"log"

	"github.com/jackc/pgx/v5"
)

// DB holds the database connection configuration
type DB struct {
	DSN     string
	Context context.Context
	Conn    *pgx.Conn
	Queries *sqlc.Queries
}

// New initializes a new DBConfig instance
func New(dsn string) *DB {
	ctx := context.Background()
	conn, err := pgx.Connect(ctx, dsn)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	log.Println("Connected to database")

	queries := sqlc.New(conn)

	return &DB{
		DSN:     dsn,
		Context: ctx,
		Conn:    conn,
		Queries: queries,
	}
}
