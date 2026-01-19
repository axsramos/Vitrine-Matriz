import hashlib
import streamlit as st
from src.models import UserModel

class AuthService:
    def hash_password(self, password):
        return hashlib.sha256(str(password).encode()).hexdigest()

    def check_credentials(self, username, password):
        """
        Verifica credenciais consultando T_USR via UserModel
        """
        pwd_hash = self.hash_password(password)
        
        # Busca usuário pelo Login (UsrLgn)
        # O Mixin monta: SELECT * FROM T_USR WHERE UsrLgn = ?
        users = UserModel.read_all(where="UsrLgn = ?", params=(username,))
        
        if not users:
            return False, None
            
        user = users[0] # Dicionário com os dados
        
        # Valida Senha
        if user['UsrPwdHash'] == pwd_hash:
            # Retorna dados normalizados para a sessão
            return True, {
                'username': user['UsrLgn'],
                'name': user['UsrNme'],
                'role': user['UsrRle'],
                'id': user['UsrCod'] # Importante guardar o ID para updates
            }
            
        return False, None

    def change_password(self, username, new_password):
        """Atualiza a senha do usuário"""
        try:
            # 1. Recupera o usuário
            users = UserModel.read_all(where="UsrLgn = ?", params=(username,))
            if not users:
                return False, "Usuário não encontrado."
            
            # 2. Instancia o Model com os dados existentes
            user_model = UserModel(**users[0])
            
            # 3. Atualiza hash
            user_model.UsrPwdHash = self.hash_password(new_password)
            
            # 4. Salva (Mixin identifica Update pela PK)
            if user_model.save():
                return True, "Senha alterada com sucesso!"
            else:
                return False, "Erro ao atualizar senha no banco."
                
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"
        

    # Antigo método de autenticação comentado para futura referência
    # @staticmethod
    # def make_hash(password: str) -> str:
    #     return hashlib.sha256(str.encode(password)).hexdigest()

    # def check_login(self, username, password):
    #     hash_tentativa = self.make_hash(password)
    #     # DEBUG: Copie o valor que sair no terminal e compare com o banco
    #     print(f"DEBUG - Hash Gerado: {hash_tentativa}")
    
    #     query = "SELECT id, nome, role FROM usuarios WHERE username = ? AND password_hash = ?"
        
    #     with get_connection() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(query, (username, hash_tentativa))
    #         user = cursor.fetchone()
            
    #         if user:
    #             return {"id": user[0], "nome": user[1], "role": user[2]}
    #         return None