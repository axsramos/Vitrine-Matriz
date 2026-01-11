from src.core.database import get_connection
import pandas as pd

class DevService:
    def get_team_stats(self):
        """Retorna dados dos devs com contagem de tarefas e releases."""
        query = """
            SELECT 
                d.id, d.nome, d.cargo, d.bio, d.github_url, d.foto_path,
                COUNT(t.id) as total_tarefas,
                COUNT(DISTINCT t.id_release) as total_releases
            FROM desenvolvedores d
            LEFT JOIN tarefas t ON d.id = t.id_desenvolvedor
            WHERE d.AudDlt IS NULL
            GROUP BY d.id, d.nome, d.cargo, d.bio, d.github_url, d.foto_path
        """
        with get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_dev_full_profile(self, dev_id):
        """Retorna dados do dev e lista de suas tarefas com nomes das releases."""
        query = """
            SELECT d.*, t.titulo as tarefa_titulo, t.impacto_negocio, r.versao
            FROM desenvolvedores d
            LEFT JOIN tarefas t ON d.id = t.id_desenvolvedor
            LEFT JOIN releases r ON t.id_release = r.id
            WHERE d.id = ? AND d.AudDlt IS NULL
        """
        with get_connection() as conn:
            return pd.read_sql_query(query, conn, params=(dev_id,))