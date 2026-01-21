import pandas as pd
from src.models.TaskModel import TaskModel

class TaskService:
    def get_all_tasks(self):
        # Usa o read_join do Model que já traz DevNome e RelVersao
        data = TaskModel.read_join()
        
        # Colunas extras geradas pelo JOIN
        extra_cols = ['DevNome', 'RelVersao']
        all_cols = TaskModel.FIELDS + extra_cols
        
        if not data:
            return pd.DataFrame(columns=all_cols)
        
        df = pd.DataFrame(data, columns=all_cols)
        return df

    def save_task(self, task_data: dict):
        try:
            task = TaskModel(**task_data)
            # Define usuário de auditoria se não vier (ex: system)
            if not task.TrfAudUsr:
                task.TrfAudUsr = 'system_user' 
                
            if task.save():
                return True, "Tarefa salva com sucesso!"
            return False, "Erro ao gravar no banco."
        except Exception as e:
            return False, f"Erro: {str(e)}"

    def get_pending_tasks(self):
        """Tarefas sem release (TrfRelCod IS NULL) e não deletadas."""
        return self.get_all_tasks_filtered(where="t.TrfRelCod IS NULL")

    def get_all_tasks_filtered(self, where):
        """Helper para chamar read_join com filtro."""
        data = TaskModel.read_join(where=where)
        extra_cols = ['DevNome', 'RelVersao']
        all_cols = TaskModel.FIELDS + extra_cols
        
        if not data: return pd.DataFrame(columns=all_cols)
        return pd.DataFrame(data, columns=all_cols)

    def update_task_release(self, task_id, release_id):
        """Atualiza o TrfRelCod de uma tarefa."""
        model = TaskModel()
        tasks = model.read_all(where="TrfCod = ?", params=(task_id,))
        if tasks:
            # Reconstrói objeto
            current = tasks[0]
            task_obj = TaskModel(**current)
            task_obj.TrfRelCod = release_id
            return task_obj.save()
        return False