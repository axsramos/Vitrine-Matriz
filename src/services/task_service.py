import pandas as pd
from src.models import TaskModel

class TaskService:
    def get_all_tasks(self):
        data = TaskModel.read_join()
        df = pd.DataFrame(data)
        if df.empty: return pd.DataFrame(columns=TaskModel.FIELDS)
        return df

    def get_tasks_by_release(self, rel_cod: int):
        # Busca tarefas de uma release específica
        data = TaskModel.read_join(where="T_TSK.RelCod = ?", params=(rel_cod,))
        return pd.DataFrame(data)

    def get_pending_tasks(self):
        # NOVO: Busca tarefas sem release (RelCod é NULL ou 0)
        # O Mixin monta: SELECT ... WHERE T_TSK.RelCod IS NULL
        data = TaskModel.read_join(where="T_TSK.RelCod IS NULL OR T_TSK.RelCod = ''")
        return pd.DataFrame(data)

    def save_task(self, task_data: dict):
        try:
            task = TaskModel(**task_data)
            if task.save():
                return True, "Tarefa salva com sucesso!"
            return False, "Erro ao persistir tarefa."
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"
            
    def update_task_release(self, task_cod: int, rel_cod: int):
        # Atualiza apenas o RelCod de uma tarefa
        try:
            task = TaskModel()
            if task.load(task_cod):
                task.RelCod = rel_cod
                task.save()
                return True
            return False
        except:
            return False