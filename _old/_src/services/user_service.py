import pandas as pd
from src.models import UserModel
from src.services.auth_service import AuthService

class UserService:
    def get_all_users(self):
        # Usa o Mixin para buscar dados
        data = UserModel.read_all()
        df = pd.DataFrame(data)
        if df.empty:
            return pd.DataFrame(columns=UserModel.FIELDS)
        return df

    def create_user(self, name, username, password, role='User'):
        try:
            # Verifica se já existe
            if UserModel.read_all(where="UsrLgn = ?", params=(username,)):
                return False, f"O login '{username}' já está em uso."

            # Hash da senha via AuthService
            auth = AuthService()
            pwd_hash = auth.hash_password(password)

            # Cria Model
            new_user = UserModel()
            new_user.UsrNme = name
            new_user.UsrLgn = username
            new_user.UsrPwdHash = pwd_hash
            new_user.UsrRle = role
            
            if new_user.save():
                return True, "Usuário criado com sucesso!"
            return False, "Erro ao salvar no banco."
            
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"

    def delete_user(self, usr_cod):
        # Implementação simples de exclusão física para este exemplo
        # Em produção, idealmente seria Logic Delete (UsrAudDlt)
        from src.core.database import Database
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {UserModel.TABLE_NAME} WHERE UsrCod = ?", (usr_cod,))
            conn.commit()
            return True, "Usuário excluído."
        except Exception as e:
            return False, str(e)