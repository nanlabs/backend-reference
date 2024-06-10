-- name: GetUser :one
SELECT 
  id,
  username,
  email,
  created_at
FROM users
WHERE id = @user_id
LIMIT 1;

-- name: ListUsers :many
SELECT 
  id,
  username,
  email,
  created_at
FROM users
ORDER BY username;

-- name: CreateUser :one
INSERT INTO users (
  username,
  password,
  email
) VALUES (
  @username,
  @password,
  @email
) RETURNING *;
