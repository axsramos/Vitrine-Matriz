import pandas as pd
from src.models.DevModel import DevModel
from src.models.UserProfileModel import UserProfileModel
from src.core.database import Database

class DevService:
    def __init__(self):
        self.db = Database()
        
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
    
    def get_all_developers(self):
        """
        Busca desenvolvedores cruzando com a tabela de perfil redesenhada.
        """
        sql = """
            SELECT 
                d.DevCod, 
                d.DevNom, 
                p.UsrPrfBio as DevBio, 
                p.UsrPrfFto as DevFto, 
                p.UsrPrfUrl as DevLnk
            FROM T_Dev d
            LEFT JOIN T_UsrPrf p ON d.DevCod = p.UsrPrfCod
            WHERE d.DevAudDlt IS NULL
            ORDER BY d.DevNom;
        """
        try:
            return self.db.select(sql)
        except Exception as e:
            print(f"Erro ao buscar portfólios da equipe: {e}")
            return []

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
    
    def check_if_exists(self, usr_cod):
        """
        Verifica a existência do Dev mantendo a integridade da sua estrutura.
        """
        # Garantimos que o usr_cod seja tratado como o tipo correto do banco (int)
        try:
            sql = "SELECT DevCod FROM T_Dev WHERE DevCod = ?"
            # Usando o método select original da sua estrutura
            result = self.db.select(sql, (int(usr_cod),))
            
            # Se a sua estrutura retorna uma lista de dicionários ou Rows:
            return len(result) > 0
        except (ValueError, TypeError):
            # Caso o usr_cod chegue vazio ou em formato inválido
            return False
        except Exception as e:
            # Log apenas para debug interno
            print(f"Erro na verificação de Dev: {e}")
            return False

    def promote_to_developer(self, dev_data):
        """
        Insere em T_Dev e eleva permissão para manager caso não seja admin.
        """
        from src.services.user_service import UserService
        u_service = UserService()
        
        # Query manual como você prefere para esta ação específica
        sql = "INSERT INTO T_Dev (DevCod, DevNom, DevAudUsr) VALUES (?, ?, ?)"
        params = (dev_data['DevCod'], dev_data['DevNom'], dev_data['DevAudUsr'])
        
        try:
            if self.db.execute(sql, params):
                # Busca o usuário para validar a regra de negócio
                user = u_service.get_user_by_id(dev_data['DevCod'])
                
                # Regra: Promover a manager se não for administrador
                if user and user.get('UsrPrm') != 'admin':
                    u_service.update_user_permission(dev_data['DevCod'], 'manager')
                    
                return True
            return False
        except Exception as e:
            print(f"Erro na promoção: {e}")
            return False