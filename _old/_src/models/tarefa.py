from src.core.crud_mixin import CrudMixin
from src.core.database import get_connection

class Tarefa(CrudMixin):
    TABLE_NAME = "tarefas"
    FIELDS_PK = ["id"]
    
    # Campos que cruzam dados do Bitrix com a Release e o Autor
    FIELDS = [
        "id",
        "bitrix_task_id",
        "titulo",
        "descricao_tecnica",
        "impacto",
        "impacto_negocio",
        "id_desenvolvedor",
        "id_release",
        "AudIns", 
        "AudUpd", 
        "AudDlt", 
        "AudUsr"
    ]

    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
        return get_connection()