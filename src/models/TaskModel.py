from src.core.crud_mixin import CrudMixin
from src.models.md.TrfMD import TrfMD
from src.core.database import Database

class TaskModel(CrudMixin, TrfMD):
    def __init__(self, **kwargs):
        super().__init__()
        for field in self.FIELDS:
            setattr(self, field, None)
        if kwargs:
            for k, v in kwargs.items():
                if hasattr(self, k): setattr(self, k, v)

    @classmethod
    def read_join(cls, where=None, params=()):
        """
        Retorna tarefas enriquecidas com Nome do Dev e Versão da Release.
        Filtra automaticamente registros deletados (TrfAudDlt IS NULL).
        """
        db = Database()
        
        # Query base com JOINs
        sql = f"""
            SELECT 
                t.*,
                d.DevNom as DevNome,
                r.RelVrs as RelVersao
            FROM {cls.TABLE_NAME} t
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            LEFT JOIN T_Rel r ON t.TrfRelCod = r.RelCod
            WHERE t.TrfAudDlt IS NULL
        """
        
        if where:
            sql += f" AND ({where})"
            
        return db.select(sql, params)
    
    def finalize_multiple_tasks(self, task_ids, auditoria_usr):
        """
        Finaliza uma lista de tarefas em massa.
        """
        try:
            for trf_id in task_ids:
                # Buscamos o objeto via Mixin para garantir auditoria
                res = self.model.read_all(where="TrfCod = ?", params=(trf_id,))
                if res:
                    task_obj = TrfModel(**res[0])
                    task_obj.TrfStt = "Concluído"
                    task_obj.TrfAudUsr = auditoria_usr
                    task_obj.save() # O Mixin cuidará do UPDATE e AudUpd
            return True
        except Exception as e:
            print(f"Erro ao finalizar tarefas: {e}")
            return False