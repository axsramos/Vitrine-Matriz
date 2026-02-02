from typing import List, Dict
from src.core.database import Database
from src.models.TaskModel import TaskModel
from src.models.ReleaseModel import ReleaseModel

class DashboardService:
    """
    Serviço de Inteligência de Dados.
    Fornece métricas e agregações para os painéis de controle.
    Retorna listas de dicionários (Python nativo) em vez de DataFrames.
    """

    def get_general_stats(self) -> Dict[str, int]:
        """
        Retorna os números para os cartões de topo (KPIs).
        Usa o método .count() otimizado dos Models.
        """
        return {
            "total_tasks": TaskModel.count(include_deleted=False),
            "pending_tasks": len(TaskModel.find_all("TrfRelCod IS NULL")), # Backlog
            "active_releases": len(ReleaseModel.find_all("RelSit = 'Aberto'"))
        }

    def get_task_status_distribution(self) -> List[Dict]:
        """
        Retorna distribuição de tarefas por status.
        Ex: [{'Status': 'Aberto', 'Quantidade': 15}, ...]
        """
        db = Database()
        sql = """
            SELECT TrfStt as Status, COUNT(TrfCod) as Quantidade 
            FROM T_Trf 
            WHERE TrfAudDlt IS NULL 
            GROUP BY TrfStt
        """
        return db.select(sql)

    def get_priority_impact_matrix(self) -> List[Dict]:
        """
        Retorna dados para análise de Prioridade vs Impacto.
        Ex: [{'Prioridade': 'Alta', 'Impacto': 'Alto', 'Total': 5}, ...]
        """
        db = Database()
        sql = """
            SELECT TrfPri as Prioridade, TrfImp as Impacto, COUNT(TrfCod) as Total 
            FROM T_Trf 
            WHERE TrfAudDlt IS NULL 
            GROUP BY TrfPri, TrfImp
        """
        return db.select(sql)

    def get_dev_workload(self) -> List[Dict]:
        """
        Retorna a carga de trabalho por Desenvolvedor.
        Ex: [{'Desenvolvedor': 'Ana', 'Total': 8}, ...]
        """
        db = Database()
        sql = """
            SELECT d.DevNom as Desenvolvedor, COUNT(t.TrfCod) as Total
            FROM T_Dev d
            LEFT JOIN T_Trf t ON d.DevCod = t.TrfDevCod AND t.TrfAudDlt IS NULL
            WHERE d.DevAudDlt IS NULL
            GROUP BY d.DevNom
            ORDER BY Total DESC
        """
        return db.select(sql)
    
    def get_recent_activity(self, limit: int = 5) -> List[Dict]:
        """Retorna as últimas tarefas atualizadas."""
        db = Database()
        sql = """
            SELECT t.TrfTit as Tarefa, t.TrfSit as Status, t.TrfAudUpd as Data, d.DevNom as Autor
            FROM T_Trf t
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE t.TrfAudDlt IS NULL
            ORDER BY t.TrfAudUpd DESC
            LIMIT ?
        """
        return db.select(sql, (limit,))