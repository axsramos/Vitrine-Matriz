import pandas as pd
from src.core.database import Database

class DashboardService:
    def __init__(self):
        self.db = Database()

    def get_task_status_distribution(self):
        """Retorna a contagem de tarefas por Status."""
        sql = """
            SELECT TrfStt, COUNT(TrfCod) as total 
            FROM T_Trf 
            WHERE TrfAudDlt IS NULL 
            GROUP BY TrfStt
        """
        rows = self.db.select(sql)
        return pd.DataFrame(rows, columns=['Status', 'Quantidade'])

    def get_priority_impact_matrix(self):
        """Retorna dados para análise de Prioridade vs Impacto."""
        sql = """
            SELECT TrfPrio, TrfImp, COUNT(TrfCod) as total 
            FROM T_Trf 
            WHERE TrfAudDlt IS NULL 
            GROUP BY TrfPrio, TrfImp
        """
        rows = self.db.select(sql)
        return pd.DataFrame(rows, columns=['Prioridade', 'Impacto', 'Total'])

    def get_dev_workload(self):
        """Retorna a carga de trabalho atual por Desenvolvedor."""
        sql = """
            SELECT d.DevNom, COUNT(t.TrfCod) as total
            FROM T_Dev d
            LEFT JOIN T_Trf t ON d.DevCod = t.TrfDevCod AND t.TrfAudDlt IS NULL
            WHERE d.DevAudDlt IS NULL
            GROUP BY d.DevNom
        """
        rows = self.db.select(sql)
        return pd.DataFrame(rows, columns=['Desenvolvedor', 'Tarefas'])