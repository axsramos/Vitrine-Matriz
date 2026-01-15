import pandas as pd
from src.core.database import get_connection

class DashboardService:
    def get_summary_stats(self, start_date, end_date):
        """Retorna estatísticas gerais filtradas por período."""
        stats = {}
        # Filtro comum para as queries
        date_filter = "AND date(AudIns) BETWEEN ? AND ?"
        params = (start_date, end_date)

        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Total de Tarefas no período
            cursor.execute(f"SELECT COUNT(*) FROM tarefas WHERE AudDlt IS NULL {date_filter}", params)
            stats['total_tarefas'] = cursor.fetchone()[0]
            
            # Total de Releases no período
            cursor.execute(f"SELECT COUNT(*) FROM releases WHERE AudDlt IS NULL {date_filter}", params)
            stats['total_releases'] = cursor.fetchone()[0]
            
            # Total de Desenvolvedores ativos (geralmente não filtra por data, mas mantemos o padrão se necessário)
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
    
    def get_impact_distribution(self, start_date, end_date):
        """Retorna a distribuição de impacto filtrada por período."""
        query = """
            SELECT impacto, COUNT(*) as total 
            FROM tarefas 
            WHERE AudDlt IS NULL 
            AND date(AudIns) BETWEEN ? AND ?
            GROUP BY impacto
        """
        with get_connection() as conn:
            return pd.read_sql_query(query, conn, params=(start_date, end_date))