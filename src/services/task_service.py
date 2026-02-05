from typing import List, Tuple, Dict, Optional
from src.models.TaskModel import TaskModel
from src.models.TaskStatus import TaskStatus

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

    def create_task(self, titulo: str, desc: str, tipo: str, prio: str, dev_id: int, prazo: str) -> Tuple[bool, str]:
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
                TrfRelCod=None,
                TrfSit=TaskStatus.ABERTO,   # Status inicial padrão
                TrfDatEnt=prazo
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
        Carrega os dados atuais antes para evitar sobrescrever campos obrigatórios (como Título) com NULL.
        """
        # 1. Busca a tarefa atual no banco
        # Precisamos dos dados completos para preencher o objeto Model
        current_data_list = TaskModel.find_all(where="TrfCod = ?", params=(task_id,))
        
        if not current_data_list:
            return False # Tarefa não encontrada
            
        current_data = current_data_list[0]
        
        # 2. Instancia o Model com os dados existentes (Preserva Título, Descrição, etc.)
        task = TaskModel(**current_data)
        
        # 3. Aplica a alteração pontual
        task.TrfSit = new_status
        
        # 4. Executa o Update
        return task.update()

    def assign_release(self, task_id: int, rel_id: int) -> bool:
        """
        Vincula uma tarefa a uma release.
        Carrega os dados atuais antes para evitar sobrescrever campos obrigatórios com NULL.
        """
        # 1. Busca a tarefa atual para garantir integridade
        current_data_list = TaskModel.find_all(where="TrfCod = ?", params=(task_id,))
        
        if not current_data_list:
            return False # Tarefa não encontrada
            
        current_data = current_data_list[0]
        
        # 2. Instancia o objeto completo
        task = TaskModel(**current_data)
        
        # 3. Aplica a alteração (Vincula a Release)
        task.TrfRelCod = rel_id
        
        # 4. Salva
        return task.update()

    def delete_task(self, task_id: int) -> bool:
        """
        Exclusão da tarefa.
        Se o TaskModel tiver FIELDS_AUDIT com AudDlt, será Soft Delete automático.
        """
        task = TaskModel(TrfCod=task_id)
        return task.delete()
    
    