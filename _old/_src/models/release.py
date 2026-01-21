from src.core.crud_mixin import CrudMixin
from src.core.database import get_connection

class Release(CrudMixin):
    """
    Modelo para a tabela 'releases'.
    Herda funcionalidades CRUD dinâmicas (similar ao CrudOperationsTrait.php).
    """
    
    # Metadados da Tabela
    TABLE_NAME = "releases"
    FIELDS_PK = ["id"]
    
    # Lista consolidada de campos (Negócio + Auditoria)
    FIELDS = [
        "id", 
        "versao", 
        "titulo_comunicado", 
        "data_publicacao", 
        "AudIns", 
        "AudUpd", 
        "AudDlt", 
        "AudUsr"
    ]

    def __init__(self, data=None):
        """
        Inicializa o modelo com um dicionário de atributos.
        Equivalente ao comportamento de $this->att no PHP.
        """
        self.att = data or {}

    def get_db_connection(self):
        """
        Método exigido pelo CrudMixin para realizar operações no banco.
        Utiliza a conexão centralizada do projeto.
        """
        return get_connection()