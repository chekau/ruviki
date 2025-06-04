CREATE TABLE IF NOT EXISTS articles (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             content TEXT NOT NULL,
             filename TEXT,
             anotation TEXT NOT NULL,
             views INTEGER,
             author_id INTEGER,
             FOREIGN KEY (author_id) REFERENCES users (id)
);




CREATE TABLE IF NOT EXISTS users (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
    

);