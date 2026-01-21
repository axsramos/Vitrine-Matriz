-- 1. Tabela de Releases (Versões)
CREATE TABLE IF NOT EXISTS T_Rel (
    RelCod INTEGER PRIMARY KEY AUTOINCREMENT,
    RelVrs VARCHAR(50) NOT NULL,        -- Ex: 1.0.0
    RelTtlCmm VARCHAR(255),             -- Título/Comentário da versão
    RelDat DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data da publicação
    
    -- Campos de Auditoria
    RelAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
    RelAudUpd DATETIME,
    RelAudUsr VARCHAR(255)
);

-- 2. Tabela de Tarefas
CREATE TABLE IF NOT EXISTS T_Trf (
    TrfCod INTEGER PRIMARY KEY AUTOINCREMENT,
    TrfTtl VARCHAR(150) NOT NULL,       -- Título
    TrfDesc VARCHAR(4000),              -- Descrição
    TrfPrio VARCHAR(20) DEFAULT 'Média',-- Prioridade
    TrfStt VARCHAR(50) DEFAULT 'A Fazer', -- Status
    TrfDatEnt DATE,                     -- Prazo de Entrega
    
    -- Chaves Estrangeiras
    TrfDevCod INTEGER,                  -- Quem vai fazer (FK T_Dev)
    TrfRelCod INTEGER,                  -- A qual versão pertence (FK T_Rel)
    
    -- Campos de Auditoria
    TrfAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
    TrfAudUpd DATETIME,
    TrfAudDlt DATETIME,
    TrfAudUsr VARCHAR(255),
    
    -- Restrições
    FOREIGN KEY(TrfDevCod) REFERENCES T_Dev(DevCod) ON DELETE SET NULL,
    FOREIGN KEY(TrfRelCod) REFERENCES T_Rel(RelCod) ON DELETE SET NULL
);

-- 3. Índices para Performance
CREATE INDEX IF NOT EXISTS IDX_Trf_Dev ON T_Trf(TrfDevCod);
CREATE INDEX IF NOT EXISTS IDX_Trf_Rel ON T_Trf(TrfRelCod); -- Importante para o filtro de releases
CREATE INDEX IF NOT EXISTS IDX_Trf_Stt ON T_Trf(TrfStt);