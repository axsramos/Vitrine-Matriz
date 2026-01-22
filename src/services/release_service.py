import pandas as pd
from src.models.ReleaseModel import ReleaseModel
from src.core.database import Database

class ReleaseService:
    def __init__(self):
        # Inicializa o banco de dados para permitir o uso de self.db.select
        self.db = Database()
        # Inicializa o modelo para persistência via CrudMixin (save/read)
        self.model = ReleaseModel()

    def create_release(self, version, title, user_audit="system"):
        try:
            model = ReleaseModel()
            # Verifica duplicidade
            exists = model.read_all(where="RelVrs = ?", params=(version,))
            if exists:
                return False, f"A versão {version} já existe."

            model.RelVrs = version
            model.RelTtlCmm = title
            model.RelAudUsr = user_audit
            
            if model.save():
                # Retorna ID recém criado para vincular tarefas
                # Como o SQLite não devolve ID no INSERT direto do Mixin simples, 
                # fazemos uma busca rápida para pegar o ID.
                new_rel = model.read_all(where="RelVrs = ?", params=(version,))
                return True, new_rel[0]['RelCod']
            return False, "Erro ao salvar release."
        except Exception as e:
            return False, f"Erro técnico: {e}"

    def get_all_releases(self):
        model = ReleaseModel()
        data = model.read_all(where="RelAudDlt IS NULL ORDER BY RelCod DESC")
        if not data: return pd.DataFrame(columns=model.FIELDS)
        return pd.DataFrame(data)
    
    def get_latest_version_label(self):
        releases = self.get_all_releases()
        v_atual = releases.iloc[0]['RelVrs'] if not releases.empty else "N/A"
        return v_atual
    
    def get_release_details(self):
        """
        Retorna as releases com o total de tarefas e a lista de desenvolvedores.
        """
        sql = """
            SELECT 
                r.RelCod,
                r.RelVrs, 
                r.RelDat, 
                r.RelTtlCmm,
                COUNT(t.TrfCod) as QtdTarefas,
                GROUP_CONCAT(DISTINCT d.DevNom) as Desenvolvedores
            FROM T_Rel r
            LEFT JOIN T_Trf t ON r.RelCod = t.TrfRelCod
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE r.RelAudDlt IS NULL
            GROUP BY r.RelCod
            ORDER BY r.RelDat DESC, r.RelCod DESC
        """
        return self.db.select(sql)