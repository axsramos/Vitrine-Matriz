CREATE TABLE T_Dev (
            DevCod INTEGER PRIMARY KEY AUTOINCREMENT,
            DevNom VARCHAR(255) NOT NULL,
            DevUsrCod INTEGER UNIQUE,
            
            -- Auditoria Completa (Padrão AudMD)
            DevAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            DevAudUpd DATETIME,
            DevAudDlt DATETIME,
            DevAudUsr VARCHAR(255),
            
            FOREIGN KEY(DevUsrCod) REFERENCES T_Usr(UsrCod) ON DELETE CASCADE
        );

CREATE INDEX IF NOT EXISTS IDX_DEV_01 ON T_DEV (DevAudIns);
CREATE INDEX IF NOT EXISTS IDX_DEV_02 ON T_DEV (DevNom);

INSERT INTO T_Dev (DevNom, DevUsrCod, DevAudUsr)
        VALUES ('Administrador', 1, 'system_setup');