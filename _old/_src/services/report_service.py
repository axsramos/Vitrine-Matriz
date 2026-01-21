import pandas as pd
from src.models import TaskModel, DevModel, ReleaseModel

class ReportService:
    def get_tasks_by_impact(self):
        """Agrupa tarefas por Impacto (TskImp)"""
        data = TaskModel.read_all(fields=['TskImp', 'TskCod'])
        df = pd.DataFrame(data)
        
        if df.empty: return pd.DataFrame()
        
        # Agrupa e conta
        return df.groupby('TskImp').count().rename(columns={'TskCod': 'Quantidade'})

    def get_tasks_by_developer(self):
        """Agrupa tarefas por Desenvolvedor (Join com T_DEV)"""
        # Usa o read_join para pegar o nome do Dev
        data = TaskModel.read_join()
        df = pd.DataFrame(data)
        
        if df.empty: return pd.DataFrame()
        
        # Agrupa por Nome do Dev
        if 'DevNme' in df.columns:
            return df['DevNme'].value_counts().to_frame(name="Tarefas")
        return pd.DataFrame()

    def get_tasks_by_release(self):
        """Agrupa tarefas por Release (Join com T_REL)"""
        data = TaskModel.read_join()
        df = pd.DataFrame(data)
        
        if df.empty: return pd.DataFrame()

        if 'RelVrs' in df.columns:
            # Filtra onde tem release preenchida
            df_rels = df.dropna(subset=['RelVrs'])
            return df_rels['RelVrs'].value_counts().to_frame(name="Tarefas")
        return pd.DataFrame()