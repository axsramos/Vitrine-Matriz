import pandas as pd
from src.models.TaskModel import TaskModel

class TaskService:
    def get_all_tasks(self):
        """Retorna todas as tarefas com dados enriquecidos (Join)."""
        data = TaskModel.read_join()
        
        # Se não houver dados, retorna DataFrame com colunas esperadas para não quebrar a tela
        if not data:
            cols = TaskModel.FIELDS + ['DevNome', 'RelVersao']
            return pd.DataFrame(columns=cols)
            
        # Pega as colunas do SELECT (Tabela + Aliases)
        # Nota: O read_join retorna tuplas, precisamos mapear para DataFrame corretamente
        # Aqui simplificamos assumindo a ordem do Model + Extras
        df = pd.DataFrame(data)
        
        # Ajuste técnico: O SQLite retorna tuplas sem cabeçalho no fetchall. 
        # Idealmente o select retornaria dicts, mas vamos mapear manualmente se necessário.
        # Para evitar complexidade agora, vamos confiar que o pandas resolve ou usar nomes fixos:
        expected_cols = TaskModel.FIELDS + ['DevNome', 'RelVersao']
        if len(df.columns) == len(expected_cols):
             df.columns = expected_cols
             
        return df

    def save_task(self, task_data: dict):
        try:
            task = TaskModel(**task_data)
            if task.save():
                return True, "Tarefa salva com sucesso!"
            return False, "Erro ao salvar no banco de dados."
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"

    def get_pending_tasks(self):
        """Tarefas sem release vinculada."""
        model = TaskModel()
        data = model.read_all(where="TrfRelCod IS NULL OR TrfRelCod = '' OR TrfRelCod = 0")
        if not data:
            return pd.DataFrame(columns=model.FIELDS)
        return pd.DataFrame(data)

    def update_task_release(self, task_id, release_id):
        model = TaskModel()
        if model.read_by_field('TrfCod', task_id):
            model.TrfRelCod = release_id
            return model.save()
        return False