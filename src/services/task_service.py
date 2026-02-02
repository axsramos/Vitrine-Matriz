from typing import List, Tuple, Dict, Optional
from src.models.TaskModel import TaskModel

class TaskService:
    
    def get_all_tasks(self) -> List[Dict]:
        """
        Retorna todas as tarefas cadastradas.
        Substitui o antigo retorno em DataFrame por Lista de Dicionários.
        """
        # O find_all já trata a conexão e filtros básicos
        return TaskModel.find_all()
    
    def get_detailed_tasks(self, where: str = None, params: tuple = None) -> List[Dict]:
        """
        Retorna tarefas enriquecidas com nomes de Dev e Release.
        Este método chama a query específica com JOINs no Model.
        """
        # Chama o método estático/classe definido no TaskModel
        return TaskModel.get_detailed_tasks(where, params)

    def get_tasks_by_release(self, rel_id: int) -> List[Dict]:
        """Busca tarefas vinculadas a uma release específica."""
        return TaskModel.find_all("TrfRelCod = ?", (rel_id,))

    def get_pending_tasks(self) -> List[Dict]:
        """
        Busca tarefas do Backlog (sem release vinculada).
        O Mixin já filtra automaticamente os deletados (Soft Delete).
        """
        return TaskModel.find_all("TrfRelCod IS NULL")

    def create_task(self, titulo: str, desc: str, tipo: str, prio: str, dev_id: int, rel_id: int = None) -> Tuple[bool, str]:
        """
        Cria uma nova tarefa.
        Auditoria (Data/Autor) é injetada automaticamente pelo Mixin.
        """
        try:
            # Instancia o modelo com os dados (Active Record)
            task = TaskModel(
                TrfTit=titulo,
                TrfDsc=desc,
                TrfTip=tipo,
                TrfPri=prio,
                TrfDevCod=dev_id,
                TrfRelCod=rel_id,
                TrfSit="Aberto"  # Status inicial padrão
            )
            
            # O create() trata o INSERT e auditoria
            if task.create():
                return True, "Tarefa criada com sucesso!"
            else:
                return False, "Não foi possível registrar a tarefa."
                
        except Exception as e:
            return False, f"Erro técnico ao criar tarefa: {str(e)}"

    def update_task_status(self, task_id: int, new_status: str) -> bool:
        """
        Atualiza apenas o status da tarefa.
        Substitui a query manual UPDATE T_Trf...
        """
        # Instancia apenas com PK e o campo a alterar
        task = TaskModel(TrfCod=task_id, TrfSit=new_status)
        return task.update()

    def assign_release(self, task_id: int, rel_id: int) -> bool:
        """Vincula uma tarefa a uma release."""
        task = TaskModel(TrfCod=task_id, TrfRelCod=rel_id)
        return task.update()

    def delete_task(self, task_id: int) -> bool:
        """
        Exclusão da tarefa.
        Se o TaskModel tiver FIELDS_AUDIT com AudDlt, será Soft Delete automático.
        """
        task = TaskModel(TrfCod=task_id)
        return task.delete()