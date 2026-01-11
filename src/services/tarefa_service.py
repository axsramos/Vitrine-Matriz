from src.core.database import get_connection
import pandas as pd

class TarefaService:
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