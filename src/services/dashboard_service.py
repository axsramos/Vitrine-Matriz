from src.core.database import get_connection

class DashboardService:
    def get_summary_stats(self):
        """Retorna números globais para os cartões de métricas."""
        with get_connection() as conn:
            cursor = conn.cursor()
            stats = {}
            # Total de Releases
            cursor.execute("SELECT COUNT(*) FROM releases")
            stats['total_releases'] = cursor.fetchone()[0]
            # Total de Tarefas
            cursor.execute("SELECT COUNT(*) FROM tarefas WHERE AudDlt IS NULL")
            stats['total_tarefas'] = cursor.fetchone()[0]
            # Total de Desenvolvedores
            cursor.execute("SELECT COUNT(*) FROM desenvolvedores WHERE AudDlt IS NULL")
            stats['total_devs'] = cursor.fetchone()[0]
            return stats
    
    def get_tasks_per_dev(self):
        """Retorna contagem de tarefas por desenvolvedor para o gráfico."""
        query = """
            SELECT d.nome, COUNT(t.id) as total
            FROM desenvolvedores d
            LEFT JOIN tarefas t ON d.id = t.id_desenvolvedor
            WHERE d.AudDlt IS NULL AND t.AudDlt IS NULL
            GROUP BY d.nome
            ORDER BY total DESC
        """
        with get_connection() as conn:
            import pandas as pd
            return pd.read_sql_query(query, conn)