import pandas as pd
from src.models.DevModel import DevModel
from src.models.UserProfileModel import UserProfileModel
from src.core.database import Database

class DevService:
    def get_all_devs_dataframe(self):
        """
        Retorna DataFrame consolidado (T_Dev + T_UsrPrf).
        Essencial para as telas de Tarefas (Dropdown) e Equipe (Cards).
        """
        db = Database()
        
        # Fazemos o JOIN diretamente via SQL para performance e simplicidade
        sql = """
            SELECT 
                d.DevCod, d.DevNom, d.DevUsrCod,
                p.UsrPrfCgo, p.UsrPrfBio, p.UsrPrfFto, p.UsrPrfUrl
            FROM T_Dev d
            LEFT JOIN T_UsrPrf p ON d.DevUsrCod = p.UsrPrfUsrCod
            WHERE d.DevAudDlt IS NULL
        """
        
        rows = db.select(sql)
        
        # Colunas esperadas no DataFrame
        cols = ['DevCod', 'DevNom', 'DevUsrCod', 'UsrPrfCgo', 'UsrPrfBio', 'UsrPrfFto', 'UsrPrfUrl']
        
        if not rows:
            return pd.DataFrame(columns=cols)
            
        return pd.DataFrame(rows, columns=cols)

    def create_dev_from_user(self, user_id, user_name):
        """
        Promove um usuário a desenvolvedor (Cria registro em T_Dev).
        """
        try:
            model = DevModel()
            
            # 1. Verifica se já existe (Inclusive deletados, se quiser reativar lógica futura)
            # Por enquanto, verifica apenas ativos
            exists = model.read_all(where="DevUsrCod = ?", params=(user_id,))
            
            if exists:
                return True, "Este usuário já é um desenvolvedor."

            # 2. Cria novo
            model.DevUsrCod = user_id
            model.DevNom = user_name
            model.DevAudUsr = "system_admin" # Ou pegar da sessão se possível
            
            if model.save():
                return True, f"{user_name} promovido a desenvolvedor com sucesso!"
            return False, "Falha ao salvar registro em T_Dev."
            
        except Exception as e:
            return False, f"Erro no serviço de desenvolvedores: {str(e)}"