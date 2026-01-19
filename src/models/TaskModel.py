from src.core.crud_mixin import CrudMixin
from src.models.TskMD import TskMD

class TaskModel(CrudMixin, TskMD):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Exemplo de método helper específico de Tarefa
    # def is_critical(self):
    #     return self.TskImp == 'Crítico'