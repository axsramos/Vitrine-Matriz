import pandas as pd
from src.models.TaskModel import TaskModel
from src.core.database import Database

class TaskService:
    def __init__(self):
        self.model = TaskModel()
        self.db = Database()

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
    
    def mark_as_completed(self, trf_id):
        """
        Atualiza o status da tarefa para 'Concluído' via CrudMixin.
        """
        try:
            # Usamos o ID da tarefa e passamos o novo valor para o campo TrfStt
            return self.model.update(trf_id, TrfStt="Concluído")
        except Exception as e:
            print(f"Erro ao concluir tarefa: {e}")
            return False
    
    def get_tasks_by_dev(self, dev_usr_cod):
        """
        Retorna tarefas pendentes vinculadas ao desenvolvedor logado.
        """
        sql = """
            SELECT t.* FROM T_Trf t
            JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE d.DevUsrCod = ? 
              AND t.TrfStt != 'Concluído' 
              AND t.TrfAudDlt IS NULL
        """
        # Usamos self.db diretamente em vez de self.model.db
        return self.db.select(sql, (dev_usr_cod,))
    
    def finalize_tasks_bulk(self, task_ids, user_lgn):
        """Finaliza múltiplas tarefas utilizando o método save() do CrudMixin."""
        try:
            for tid in task_ids:
                # Carregamos o objeto para garantir que o save() execute UPDATE
                task = TaskModel()
                if task.read_by_field("TrfCod", tid):
                    task.TrfStt = "Concluído"
                    task.TrfAudUsr = user_lgn
                    task.save()
            return True
        except Exception as e:
            print(f"Erro ao finalizar em massa: {e}")
            return False