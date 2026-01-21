-- // Tabela de Usuários
CREATE TABLE T_Usr (
            UsrCod INTEGER PRIMARY KEY AUTOINCREMENT,
            UsrNom VARCHAR(255) NOT NULL,
            UsrLgn VARCHAR(255) NOT NULL UNIQUE,
            UsrPwd VARCHAR(255) NOT NULL,
            UsrPrm VARCHAR(255) DEFAULT 'user',
            
            -- Auditoria
            UsrAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            UsrAudUpd DATETIME,
            UsrAudDlt DATETIME,
            UsrAudUsr VARCHAR(255)
        );
CREATE INDEX IF NOT EXISTS IDX_USR_01 ON T_USR (UsrAudIns);
CREATE INDEX IF NOT EXISTS IDX_USR_02 ON T_USR (UsrNom);
CREATE INDEX IF NOT EXISTS IDX_USR_03 ON T_USR (UsrPrm, UsrNom);

-- // Tabela de Perfis de Usuários
CREATE TABLE T_UsrPrf (
            UsrPrfCod INTEGER PRIMARY KEY AUTOINCREMENT,
            UsrPrfBio VARCHAR(4000),
            UsrPrfFto VARCHAR(255),
            UsrPrfUrl VARCHAR(255),
            UsrPrfCgo VARCHAR(255),
            
            -- Chave Estrangeira (1:1 com T_Usr)
            UsrPrfUsrCod INTEGER UNIQUE,
            
            -- Auditoria
            UsrPrfAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            UsrPrfAudUpd DATETIME,
            UsrPrfAudDlt DATETIME,
            UsrPrfAudUsr VARCHAR(255),
            
            FOREIGN KEY(UsrPrfUsrCod) REFERENCES T_Usr(UsrCod) ON DELETE CASCADE
        );

-- // UsrPwd: admin123
INSERT INTO T_Usr (UsrNom, UsrLgn, UsrPwd, UsrPrm) 
        VALUES ('Administrador', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');

INSERT INTO T_UsrPrf (UsrPrfBio, UsrPrfFto, UsrPrfUrl, UsrPrfCgo, UsrPrfUsrCod)
        VALUES ('Administrador do sistema', 'admin.png', 'admin.com', 'Administrador', 1);