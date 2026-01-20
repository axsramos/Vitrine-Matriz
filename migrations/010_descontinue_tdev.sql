BEGIN TRANSACTION;

-- 1. Renomeia a tabela antiga
ALTER TABLE T_Dev RENAME TO T_Dev_Old;

-- 2. Cria a nova T_Dev (Somente dados técnicos)
-- Mantive DevNme por segurança, mas idealmente nome é do usuário
CREATE TABLE T_Dev (
    DevCod INTEGER PRIMARY KEY AUTOINCREMENT,
    DevNme TEXT,      
    DevUsrCod INTEGER,
    -- Adicione aqui campos técnicos se houver (Ex: Stack, Senioridade Técnica)
    FOREIGN KEY(DevUsrCod) REFERENCES T_Usr(UsrCod)
);

-- 3. Copia apenas os dados mantidos
INSERT INTO T_Dev (DevCod, DevNme, DevUsrCod)
SELECT DevCod, DevNme, DevUsrCod
FROM T_Dev_Old;

-- 4. Apaga a velha
DROP TABLE T_Dev_Old;

-- 5. (Opcional) Limpar a coluna UsrFto de T_Usr se quiser deixá-la puramente para Auth
-- ALTER TABLE T_Usr DROP COLUMN UsrFto; (Lembrando que em SQLite precisa recriar a tabela também)

COMMIT;