-- Adiciona a coluna DevUsrCod na tabela T_Dev 
ALTER TABLE T_Dev ADD COLUMN DevUsrCod INTEGER;

-- Se nao existit, Adiciona restrição de chave estrangeira
-- ALTER TABLE T_Dev 
--     ADD CONSTRAINT IF NOT EXISTS FK_Dev_01 
--     FOREIGN KEY (DevUsrCod) 
--     REFERENCES T_Usr(UsrCod) 
--     ON DELETE SET NULL;

-- Atualiza os perfis de desenvolvedor existentes para vincular ao usuário correto
UPDATE T_Dev SET DevUsrCod = (SELECT UsrCod FROM T_Usr WHERE UsrLgn = DevLgnExt);

-- -- # PARA SQLINT # --
-- BEGIN TRANSACTION;

-- -- 1. Renomeia a original
-- ALTER TABLE T_Dev RENAME TO T_Dev_old;

-- -- 2. Cria a nova com a FK configurada
-- CREATE TABLE T_Dev (
--     DevCod INTEGER PRIMARY KEY AUTOINCREMENT,
--     DevNom TEXT NOT NULL,
--     DevUsrCod INTEGER, -- A coluna de ligação
--     -- ... inclua aqui as demais colunas originais ...

--     CONSTRAINT FK_Dev_01 FOREIGN KEY (DevUsrCod) 
--     REFERENCES T_Usr (UsrCod) 
--     ON DELETE SET NULL
-- );

-- -- 3. Migra os dados da antiga para a nova
-- INSERT INTO T_Dev (DevCod, DevNom, DevUsrCod) -- Liste todas as colunas
-- SELECT DevCod, DevNom, DevUsrCod FROM T_Dev_old;

-- -- 4. Remove a tabela antiga
-- DROP TABLE T_Dev_old;

-- COMMIT;
