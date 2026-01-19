-- Objetivo: Migrar os dados das tabelas antigas
-- (usuarios, desenvolvedores, releases, tarefas) para as novas tabelas reestruturadas
-- (T_USR, T_DEV, T_REL, T_TSK).

DELETE FROM T_TSK;
DELETE FROM sqlite_sequence WHERE name='T_TSK';

DELETE FROM T_REL;
DELETE FROM sqlite_sequence WHERE name='T_REL';

DELETE FROM T_DEV;
DELETE FROM sqlite_sequence WHERE name='T_DEV';

DELETE FROM T_USR;
DELETE FROM sqlite_sequence WHERE name='T_USR';

-- copy data table usuarios to table T_USR
INSERT INTO T_USR (UsrNme, UsrLgn, UsrPwdHash, UsrRle)
SELECT nome AS UsrNme, username AS UsrLgn, password_hash AS UsrPwdHash, role AS UsrRle
FROM usuarios;
-- copy data table desenvolvedores to table T_DEV
INSERT INTO T_DEV (DevNme, DevLgnExt, DevCgo, DevBio, DevPgeUrl, DevFto)
SELECT Nome AS DevNme, login_bitrix AS DevLgnExt, cargo AS DevCgo, bio AS DevBio, github_url AS DevPgeUrl, foto_path AS DevFto
FROM desenvolvedores;
-- copy data table releases to table T_REL
INSERT INTO T_REL (RelVrs, RelTtlCmm, RelDtaPub)
SELECT versao AS RelVrs, titulo_comunicado AS RelTtlCmm, data_publicacao AS RelDtaPub
FROM releases;
-- copy data table tarefas to table T_TSK
INSERT INTO T_TSK (TskExtCod, TskTtl, TskDsc, TskImp, DevCod, RelCod)
SELECT
    T.bitrix_task_id,                               -- Código externo da tarefa
    T.titulo,                                       -- Título da tarefa
    T.descricao_tecnica,                            -- Descrição da tarefa
    T.impacto_negocio,                              -- Impacto da tarefa
    (SELECT DevCod FROM T_DEV WHERE DevLgnExt = D.login_bitrix) AS DevCod, -- Busca o novo DevCod usando o login
    (SELECT RelCod FROM T_REL WHERE RelVrs = R.versao) AS RelCod           -- Busca o novo RelCod usando a versão
FROM
    tarefas AS T
LEFT JOIN
    desenvolvedores AS D ON T.id = D.id -- 1. Encontra o desenvolvedor original
LEFT JOIN
    releases AS R ON T.id = R.id;             -- 2. Encontra a release original
-- end of file
