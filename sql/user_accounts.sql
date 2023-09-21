CREATE TABLE user_accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
)