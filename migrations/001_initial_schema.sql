-- Tabela de Desenvolvedores
CREATE TABLE IF NOT EXISTS desenvolvedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    login_bitrix TEXT UNIQUE NOT NULL,
    cargo TEXT,
    bio TEXT,
    github_url TEXT,
    foto_path TEXT,
    AudIns DATETIME,
    AudUpd DATETIME,
    AudDlt DATETIME,
    AudUsr TEXT
);

-- Tabela de Releases
CREATE TABLE IF NOT EXISTS releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    versao TEXT UNIQUE NOT NULL,
    titulo_comunicado TEXT,
    data_publicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    AudIns DATETIME,
    AudUpd DATETIME,
    AudDlt DATETIME,
    AudUsr TEXT
);

-- Tabela de Tarefas
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bitrix_task_id INTEGER UNIQUE NOT NULL,
    titulo TEXT NOT NULL,
    descricao_tecnica TEXT,
    impacto_negocio TEXT,
    id_desenvolvedor INTEGER,
    id_release INTEGER,
    AudIns DATETIME,
    AudUpd DATETIME,
    AudDlt DATETIME,
    AudUsr TEXT,
    FOREIGN KEY (id_desenvolvedor) REFERENCES desenvolvedores (id),
    FOREIGN KEY (id_release) REFERENCES releases (id)
);