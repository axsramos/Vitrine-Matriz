
/*
-- // opcional // --
-- 1. Inserir uma Release (Ajustado para T_Rel conforme setup)
INSERT INTO T_Rel (RelVrs, RelDat, RelTtlCmm, RelAudUsr, RelAudIns) 
VALUES ('1.0.5', date('now', '-2 days'), 'Versão de Estabilidade e Dashboard', 'admin', datetime('now'));

-- 2. Inserir Tarefas Variadas (Ajustado para T_Trf conforme setup)

-- Tarefa Atrasada (Crítica)
INSERT INTO T_Trf (TrfTtl, TrfDesc, TrfPrio, TrfStt, TrfDatEnt, TrfDevCod, TrfAudUsr, TrfAudIns)
VALUES ('Correção de Login Crítico', 'Erro ao logar com senha especial', 'Alta', 'Pendente', date('now', '-5 days'), 1, 'admin', datetime('now'));

-- Tarefa Atrasada (Média)
INSERT INTO T_Trf (TrfTtl, TrfDesc, TrfPrio, TrfStt, TrfDatEnt, TrfDevCod, TrfAudUsr, TrfAudIns)
VALUES ('Ajustar CSS da Home', 'Alinhar botões', 'Média', 'Em Andamento', date('now', '-1 day'), 1, 'admin', datetime('now'));

-- Tarefa No Prazo (Futura)
INSERT INTO T_Trf (TrfTtl, TrfDesc, TrfPrio, TrfStt, TrfDatEnt, TrfDevCod, TrfAudUsr, TrfAudIns)
VALUES ('Desenvolver API de Pagamento', 'Integração com Gateway', 'Alta', 'Pendente', date('now', '+5 days'), 2, 'admin', datetime('now'));

-- Tarefas Concluídas
INSERT INTO T_Trf (TrfTtl, TrfDesc, TrfPrio, TrfStt, TrfDatEnt, TrfDevCod, TrfAudUsr, TrfAudIns)
VALUES ('Modelagem do Banco', 'Criação do DER', 'Alta', 'Concluído', date('now', '-10 days'), 1, 'admin', datetime('now'));

INSERT INTO T_Trf (TrfTtl, TrfDesc, TrfPrio, TrfStt, TrfDatEnt, TrfDevCod, TrfAudUsr, TrfAudIns)
VALUES ('Configuração do Servidor', 'Setup AWS', 'Média', 'Concluído', date('now', '-8 days'), 2, 'admin', datetime('now'));
*/

