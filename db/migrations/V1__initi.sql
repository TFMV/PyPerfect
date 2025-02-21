-- V1__init.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message TEXT NOT NULL,
    level TEXT CHECK (level IN ('INFO', 'WARN', 'ERROR')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
