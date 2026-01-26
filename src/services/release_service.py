import os
import pandas as pd
from datetime import datetime
from src.models.ReleaseModel import ReleaseModel
from src.core.database import Database

class ReleaseService:
    def __init__(self):
        self.db = Database()
        self.model = ReleaseModel()

    def create_release(self, version, title, user_audit="system"):
        try:
            model = ReleaseModel()
            exists = model.read_all(where="RelVrs = ?", params=(version,))
            if exists:
                return False, f"A versão {version} já existe."

            model.RelVrs = version
            model.RelTtlCmm = title
            model.RelAudUsr = user_audit
            model.RelDat = datetime.now().strftime('%Y-%m-%d')
            
            if model.save():
                new_rel = model.read_all(where="RelVrs = ?", params=(version,))
                return True, new_rel[0]['RelCod']
            return False, "Erro ao salvar release."
        except Exception as e:
            return False, str(e)

    def get_release_details(self):
        """Busca releases com agregados de desenvolvedores e tarefas para a UI."""
        sql = """
            SELECT 
                r.RelCod, r.RelVrs, r.RelDat, r.RelTtlCmm,
                GROUP_CONCAT(DISTINCT d.DevNom) as Desenvolvedores,
                GROUP_CONCAT(t.TrfTtl, '||') as ListaTarefas,
                COUNT(t.TrfCod) as QtdTarefas
            FROM T_Rel r
            LEFT JOIN T_Trf t ON r.RelCod = t.TrfRelCod
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE r.RelAudDlt IS NULL
            GROUP BY r.RelCod
            ORDER BY r.RelDat DESC
        """
        return self.db.select(sql)