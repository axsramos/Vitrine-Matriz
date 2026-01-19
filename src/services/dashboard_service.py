import pandas as pd
from src.models import TaskModel, ReleaseModel
from datetime import datetime, timedelta

class DashboardService:
    def get_impact_distribution(self, start_date=None, end_date=None):
        """
        Retorna a distribuição de tarefas por Impacto (TskImp).
        """
        where_clause = None
        params = ()
        
        if start_date and end_date:
            where_clause = "TskAudIns BETWEEN ? AND ?"
            params = (str(start_date), str(end_date))

        # Busca dados via Model (Tabela T_TSK)
        data = TaskModel.read_all(fields=['TskImp', 'TskCod'], where=where_clause, params=params)
        df = pd.DataFrame(data)

        if df.empty:
            return pd.DataFrame(columns=['Impacto', 'Total'])

        # Agrupa e renomeia
        df_grouped = df.groupby('TskImp').size().reset_index(name='Total')
        df_grouped.rename(columns={'TskImp': 'Impacto'}, inplace=True)
        
        return df_grouped

    def get_tasks_evolution(self, days=30):
        """
        Retorna a evolução de tarefas criadas nos últimos X dias.
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        data = TaskModel.read_all(
            fields=['TskAudIns', 'TskCod'],
            where="TskAudIns >= ?",
            params=(cutoff_date,)
        )
        df = pd.DataFrame(data)

        if df.empty:
            return pd.DataFrame(columns=['Data', 'Quantidade'])

        # Converte para data e agrupa
        df['Data'] = pd.to_datetime(df['TskAudIns']).dt.date
        df_grouped = df.groupby('Data').size().reset_index(name='Quantidade')
        
        return df_grouped

    def get_latest_releases(self, limit=5):
        """
        Retorna as últimas releases publicadas.
        """
        data = ReleaseModel.read_all()
        df = pd.DataFrame(data)

        if df.empty:
            return pd.DataFrame(columns=['Versao', 'Data', 'Titulo'])

        if 'RelDtaPub' in df.columns:
            df['RelDtaPub'] = pd.to_datetime(df['RelDtaPub'])
            df = df.sort_values(by='RelDtaPub', ascending=False).head(limit)
            
            return df[['RelVrs', 'RelDtaPub', 'RelTtlCmm']].rename(
                columns={'RelVrs': 'Versao', 'RelDtaPub': 'Data', 'RelTtlCmm': 'Titulo'}
            )
        
        return df