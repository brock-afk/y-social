CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    created_by INT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (created_by) REFERENCES user_account(id)
);
