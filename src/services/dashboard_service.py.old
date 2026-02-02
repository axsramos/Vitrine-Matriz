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
    
    def get_kpis_gerais(self):
        """
        Retorna indicadores macro. Campos de T_Trf: TrfStt, TrfDatEnt, TrfAudDlt.
        """
        sql = """
            SELECT 
                COUNT(*) as Total,
                SUM(CASE WHEN TrfStt = 'Concluído' THEN 1 ELSE 0 END) as Concluidas,
                SUM(CASE WHEN date(TrfDatEnt) < date('now') AND TrfStt != 'Concluído' THEN 1 ELSE 0 END) as Atrasadas
            FROM T_Trf
            WHERE TrfAudDlt IS NULL
        """
        result = self.db.select(sql)
        
        if result:
            row = result[0]
            total = row['Total'] or 0
            concluidas = row['Concluidas'] or 0
            atrasadas = row['Atrasadas'] or 0
            
            pct = (concluidas / total * 100) if total > 0 else 0.0
            
            return {
                "total": total,
                "concluidas": concluidas,
                "atrasadas": atrasadas,
                "percentual": round(pct, 1)
            }
        return {"total": 0, "concluidas": 0, "atrasadas": 0, "percentual": 0.0}

    def get_ultima_release(self):
        """
        CORREÇÃO: Busca RelVrs e RelDat em vez de RelVer/RelDatPub.
        """
        sql = "SELECT RelVrs, RelDat FROM T_Rel ORDER BY RelCod DESC LIMIT 1"
        res = self.db.select(sql)
        if res:
            return res[0]
        return {"RelVrs": "Não definida", "RelDat": None}

    def get_tarefas_por_status(self):
        """Dados para gráfico de Pizza."""
        sql = """
            SELECT TrfStt as Status, COUNT(*) as Quantidade 
            FROM T_Trf 
            WHERE TrfAudDlt IS NULL 
            GROUP BY TrfStt
        """
        data = self.db.select(sql)
        return pd.DataFrame(data) if data else pd.DataFrame(columns=["Status", "Quantidade"])

    def get_carga_trabalho_devs(self):
        """Dados para gráfico de Barras."""
        sql = """
            SELECT d.DevNom as Desenvolvedor, COUNT(t.TrfCod) as Tarefas
            FROM T_Trf t
            JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE t.TrfAudDlt IS NULL AND t.TrfStt != 'Concluído'
            GROUP BY d.DevNom
            ORDER BY Tarefas DESC
        """
        data = self.db.select(sql)
        return pd.DataFrame(data) if data else pd.DataFrame(columns=["Desenvolvedor", "Tarefas"])

    def get_tarefas_atrasadas_detalhe(self, limit=5):
        """Lista as tarefas críticas."""
        sql = """
            SELECT t.TrfTtl, t.TrfDatEnt, d.DevNom, t.TrfPrio
            FROM T_Trf t
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE date(t.TrfDatEnt) < date('now') 
              AND t.TrfStt != 'Concluído' 
              AND t.TrfAudDlt IS NULL
            ORDER BY t.TrfDatEnt ASC
            LIMIT ?
        """
        return self.db.select(sql, (limit,))