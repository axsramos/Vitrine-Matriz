from src.core.crud_mixin import CrudMixin
from src.models.TrfMD import TrfMD
from src.core.database import Database

class TaskModel(CrudMixin, TrfMD):
    def __init__(self, **kwargs):
        super().__init__()
        # Inicializa todos os campos como None
        for field in self.FIELDS:
            setattr(self, field, None)
        
        # Popula se receber dicionário
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key) or key in self.FIELDS:
                    setattr(self, key, value)

    @classmethod
    def read_join(cls, where=None, params=()):
        """
        Busca tarefas trazendo os nomes (JOIN) de T_Dev e T_Rel.
        """
        db = Database()
        
        # ATENÇÃO: Corrigido DevNme para DevNom e T_TSK para T_Trf
        sql = f"""
            SELECT 
                t.*,
                d.DevNom as DevNome,   -- Nome do Desenvolvedor
                r.RelVrs as RelVersao  -- Versão da Release
            FROM {cls.TABLE_NAME} t
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            LEFT JOIN T_Rel r ON t.TrfRelCod = r.RelCod
        """
        
        if where:
            sql += f" WHERE {where}"
            
        return db.select(sql, params)