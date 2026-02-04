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
    
    # def get_recent_activity(self, limit: int = 5) -> List[Dict]:
    #     """Retorna as últimas tarefas atualizadas."""
    #     db = Database()
    #     sql = """
    #         SELECT t.TrfTit as Tarefa, t.TrfSit as Status, t.TrfAudUpd as Data, d.DevNom as Autor
    #         FROM T_Trf t
    #         LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
    #         WHERE t.TrfAudDlt IS NULL
    #         ORDER BY t.TrfAudUpd DESC
    #         LIMIT ?
    #     """
    #     return db.select(sql, (limit,))
    
    def get_kpis(self) -> Dict[str, int]:
        """
        Retorna os indicadores principais (Cards do Topo).
        Chaves esperadas: total_open, total_closed, total_releases, active_devs
        """
        db = Database()
        
        # 1. Tarefas Abertas (Tudo que não é 'Concluído')
        sql_open = "SELECT COUNT(*) as total FROM T_Trf WHERE TrfStt != 'Concluído' AND TrfAudDlt IS NULL"
        res_open = db.select(sql_open)
        total_open = res_open[0]['total'] if res_open else 0
        
        # 2. Tarefas Concluídas
        sql_closed = "SELECT COUNT(*) as total FROM T_Trf WHERE TrfStt = 'Concluído' AND TrfAudDlt IS NULL"
        res_closed = db.select(sql_closed)
        total_closed = res_closed[0]['total'] if res_closed else 0
        
        # 3. Total de Releases
        sql_rel = "SELECT COUNT(*) as total FROM T_Rel WHERE RelAudDlt IS NULL"
        res_rel = db.select(sql_rel)
        total_rel = res_rel[0]['total'] if res_rel else 0
        
        # 4. Devs Ativos
        sql_dev = "SELECT COUNT(*) as total FROM T_Dev WHERE DevAudDlt IS NULL"
        res_dev = db.select(sql_dev)
        total_dev = res_dev[0]['total'] if res_dev else 0

        return {
            "total_open": total_open,
            "total_closed": total_closed,
            "total_releases": total_rel,
            "active_devs": total_dev
        }

    def get_tasks_by_dev(self) -> List[Dict]:
        """
        Retorna produtividade por desenvolvedor.
        Usado no Gráfico de Barras.
        Retorna: [{'Desenvolvedor': 'Nome', 'Tarefas': 10}, ...]
        """
        db = Database()
        sql = """
            SELECT 
                d.DevNom as Desenvolvedor, 
                COUNT(t.TrfCod) as Tarefas
            FROM T_Dev d
            LEFT JOIN T_Trf t ON d.DevCod = t.TrfDevCod AND t.TrfAudDlt IS NULL
            WHERE d.DevAudDlt IS NULL
            GROUP BY d.DevNom
            ORDER BY Tarefas DESC
        """
        return db.select(sql) or []

    def get_tasks_by_status(self) -> List[Dict]:
        """
        Retorna distribuição de status.
        Usado no Gráfico de Donut.
        Retorna: [{'Status': 'Aberto', 'Quantidade': 5}, ...]
        """
        db = Database()
        sql = """
            SELECT 
                TrfStt as Status, 
                COUNT(TrfCod) as Quantidade 
            FROM T_Trf 
            WHERE TrfAudDlt IS NULL 
            GROUP BY TrfStt
        """
        return db.select(sql) or []
    
    def get_recent_activity(self, limit: int = 5) -> List[Dict]:
        """
        Retorna as últimas tarefas modificadas para a tabela de atividades.
        """
        db = Database()
        sql = f"""
            SELECT 
                t.TrfTit as Tarefa,
                t.TrfStt as Status,
                COALESCE(t.TrfAudUpd, t.TrfAudIns) as Data,
                d.DevNom as Dev
            FROM T_Trf t
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE t.TrfAudDlt IS NULL
            ORDER BY Data DESC
            LIMIT {limit}
        """
        return db.select(sql) or []