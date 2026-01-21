-- migrations/02_create_users_table.sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'Admin', -- Admin ou Viewer
    AudIns DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Inserindo um admin inicial (Senha padrão: admin123)
-- Nota: Em produção, você deve gerar o hash via código.
INSERT INTO usuarios (nome, username, password_hash, role) 
VALUES ('Administrador', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin');
-- VALUES ('Administrador', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Admin');