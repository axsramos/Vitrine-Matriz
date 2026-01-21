-- Garante a limpeza (já que você informou que fez o Drop, mas por segurança)
DROP TABLE IF EXISTS T_Trf;

CREATE TABLE T_Trf (
    -- Identificação
    TrfCod INTEGER PRIMARY KEY AUTOINCREMENT,
    TrfTtl VARCHAR(150),                -- Título (Mantido para não quebrar a tela de listagem)
    TrfDesc VARCHAR(4000),              -- Descrição
    
    -- Gestão
    TrfPrio VARCHAR(20) DEFAULT 'Média',-- Prioridade
    TrfStt VARCHAR(50) DEFAULT 'A Fazer', -- Status
    TrfDatEnt DATE,                     -- Data de Entrega
    
    -- Relacionamentos (Foreign Keys)
    TrfDevCod INTEGER,                  -- Desenvolvedor
    TrfRelCod INTEGER,                  -- Release
    
    -- Auditoria Completa
    TrfAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
    TrfAudUpd DATETIME,
    TrfAudDlt DATETIME,
    TrfAudUsr VARCHAR(255),
    
    -- Restrições de Integridade
    CONSTRAINT FK_Trf_01 FOREIGN KEY (TrfDevCod) REFERENCES T_Dev(DevCod) ON DELETE SET NULL,
    CONSTRAINT FK_Trf_02 FOREIGN KEY (TrfRelCod) REFERENCES T_Rel(RelCod) ON DELETE SET NULL
);

-- Índices para otimizar as consultas das telas
CREATE INDEX IDX_Trf_Dev ON T_Trf(TrfDevCod);
CREATE INDEX IDX_Trf_Rel ON T_Trf(TrfRelCod);
CREATE INDEX IDX_Trf_Stt ON T_Trf(TrfStt);