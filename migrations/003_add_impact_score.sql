-- migrations/03_add_impact_score.sql
ALTER TABLE tarefas ADD COLUMN impacto TEXT DEFAULT 'Médio';
-- Valores sugeridos: 'Crítico', 'Alto', 'Médio', 'Baixo'