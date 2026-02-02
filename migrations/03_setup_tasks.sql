CREATE TABLE T_Rel (
            RelCod INTEGER PRIMARY KEY AUTOINCREMENT,
            RelVrs VARCHAR(50) NOT NULL,    -- Versão (ex: 1.0.0)
            RelTtlCmm VARCHAR(255),         -- Título/Comentário
            RelSit VARCHAR(50) DEFAULT 'Aberto', -- Situação
            RelDat DATE,                    -- Data da Publicação
            
            -- Auditoria
            RelAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            RelAudUpd DATETIME,
            RelAudDlt DATETIME,
            RelAudUsr VARCHAR(255)
        );
CREATE INDEX IF NOT EXISTS IDX_REL_01 ON T_Rel (RelAudIns);
CREATE INDEX IF NOT EXISTS IDX_REL_02 ON T_Rel (RelVrs);

CREATE TABLE T_Trf (
            TrfCod INTEGER PRIMARY KEY AUTOINCREMENT,
            TrfTtl VARCHAR(150) NOT NULL,
            TrfDesc VARCHAR(4000),
            TrfPrio VARCHAR(20) DEFAULT 'Média',
            TrfImp VARCHAR(20) DEFAULT 'Médio',  -- Campo Impacto
            TrfStt VARCHAR(50) DEFAULT 'A Fazer',
            TrfDatEnt DATE,
            
            -- FKs
            TrfDevCod INTEGER,
            TrfRelCod INTEGER,
            
            -- Auditoria
            TrfAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            TrfAudUpd DATETIME,
            TrfAudDlt DATETIME,
            TrfAudUsr VARCHAR(255),
            
            FOREIGN KEY(TrfDevCod) REFERENCES T_Dev(DevCod) ON DELETE SET NULL,
            FOREIGN KEY(TrfRelCod) REFERENCES T_Rel(RelCod) ON DELETE SET NULL
        );

CREATE INDEX IF NOT EXISTS IDX_TRF_01 ON T_Trf (TrfAudIns);
CREATE INDEX IF NOT EXISTS IDX_TRF_02 ON T_Trf (TrfDevCod);
CREATE INDEX IF NOT EXISTS IDX_TRF_03 ON T_Trf (TrfRelCod);
CREATE INDEX IF NOT EXISTS IDX_TRF_04 ON T_Trf (TrfStt);
CREATE INDEX IF NOT EXISTS IDX_TRF_05 ON T_Trf (TrfAudDlt);