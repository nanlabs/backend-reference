package db

import (
	"context"
	"fmt"
	"go-postgres-sqlc/users"

	"github.com/jackc/pgx/v5"
)

var dsn = "host=db user=postgres password=postgres dbname=poc port=5432 sslmode=disable"

var Context = context.Background()
var db = func() (db *pgx.Conn) {
	conn, err := pgx.Connect(Context, dsn)
	if err != nil {
		panic(err)
	}
	fmt.Println("Connected to database")
	return conn
}()

var Queries = users.New(db)

func CreateUserTable() {
	query := `CREATE TABLE IF NOT EXISTS users (
		id SERIAL PRIMARY KEY,
		username VARCHAR(30) NOT NULL,
		password VARCHAR(100) NOT NULL,
		email VARCHAR(50),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	)`
	_, err := db.Exec(Context, query)
	if err != nil {
		panic(err)
	}
}
