from src.core.database import get_connection
import pandas as pd

class TaskService:
    def get_unreleased_tasks(self):
        """Retorna tarefas que não possuem vínculo com release (id_release IS NULL)."""
        query = """
            SELECT t.id, t.bitrix_task_id, t.titulo, d.nome as desenvolvedor
            FROM tarefas t
            JOIN desenvolvedores d ON t.id_desenvolvedor = d.id
            WHERE t.id_release IS NULL AND t.AudDlt IS NULL
            ORDER BY t.AudIns DESC
        """
        with get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_all_tasks_for_release(self):
        """Retorna todas as tarefas, priorizando as novas (sem release)."""
        query = """
            SELECT 
                t.id, 
                t.bitrix_task_id, 
                t.titulo, 
                d.nome as desenvolvedor,
                CASE 
                    WHEN t.id_release IS NULL THEN '⭐ Nova' 
                    ELSE '✅ Publicada' 
                END as status_vinculo
            FROM tarefas t
            JOIN desenvolvedores d ON t.id_desenvolvedor = d.id
            WHERE t.AudDlt IS NULL
            ORDER BY (CASE WHEN t.id_release IS NULL THEN 0 ELSE 1 END), t.AudIns DESC
        """
        with get_connection() as conn:
            import pandas as pd
            return pd.read_sql_query(query, conn)
    
    def create(self, titulo, descricao, id_release, id_desenvolvedor, impacto="Médio"):
        """Salva uma nova tarefa no banco de dados."""
        query = """
            INSERT INTO tarefas (titulo, descricao, id_release, id_desenvolvedor, impacto)
            VALUES (?, ?, ?, ?, ?)
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (titulo, descricao, id_release, id_desenvolvedor, impacto))
            conn.commit()

    def get_all_with_details(self, start_date=None, end_date=None):
        """ Retorna tarefas detalhadas com filtro opcional por período. """
        
        # Base da consulta com os JOINs necessários para o relatório
        query = """
            SELECT 
                t.titulo, 
                t.impacto, 
                t.impacto_negocio,
                d.nome as dev, 
                COALESCE(r.versao, 'Aguardando') as release,
                t.AudIns as data_criacao
            FROM tarefas t
            JOIN desenvolvedores d ON t.id_desenvolvedor = d.id
            LEFT JOIN releases r ON t.id_release = r.id
            WHERE t.AudDlt IS NULL
        """
        
        params = []
        
        # Adiciona o filtro de data se os parâmetros forem fornecidos
        if start_date and end_date:
            query += " AND date(t.AudIns) BETWEEN ? AND ?"
            params = [start_date, end_date]
            
        query += " ORDER BY t.AudIns DESC"

        with get_connection() as conn:
            # O pandas lida com os parâmetros através do argumento params
            return pd.read_sql_query(query, conn, params=params)