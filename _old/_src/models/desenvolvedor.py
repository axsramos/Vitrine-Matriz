from src.core.crud_mixin import CrudMixin
from src.core.database import get_connection

class Desenvolvedor(CrudMixin):
    TABLE_NAME = "desenvolvedores"
    FIELDS_PK = ["id"]
    
    # Campos de Negócio + Auditoria
    FIELDS = [
        "id", 
        "nome", 
        "login_bitrix", 
        "cargo", 
        "bio", 
        "github_url",
        "foto_path",
        "AudIns", 
        "AudUpd", 
        "AudDlt", 
        "AudUsr"
    ]

    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
        return get_connection()