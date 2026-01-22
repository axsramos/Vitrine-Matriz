import pandas as pd
from src.models.ReleaseModel import ReleaseModel

class ReleaseService:
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