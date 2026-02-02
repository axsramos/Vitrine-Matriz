import bcrypt
from typing import List, Optional, Tuple, Dict
from src.models.UserModel import UserModel

class UserService:
    
    def get_all_users(self) -> List[Dict]:
        """
        Retorna todos os utilizadores ativos.
        O Mixin (find_all) já filtra automaticamente os excluídos (Soft Delete).
        """
        return UserModel.find_all()

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Busca um usuário pelo ID."""
        return UserModel.get_by_id(user_id)

    def create_user(self, login: str, nome: str, senha: str, perfil: str) -> Tuple[bool, str]:
        """
        Cria novo usuário.
        Auditoria (Data/Autor) é injetada automaticamente pelo Mixin.
        """
        # 1. Validação de Duplicidade
        if UserModel.exists(login): # Se tiveres implementado verificação por login, ou:
             existing = UserModel.find_all("UsrLgn = ?", (login,))
             if existing:
                 return False, f"O login '{login}' já está em uso."

        # 2. Criptografia segura
        hashed_pwd = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 3. Criação
        user = UserModel(
            UsrNom=nome,
            UsrLgn=login,
            UsrPwd=hashed_pwd,
            UsrPrm=perfil
        )

        try:
            if user.create():
                return True, "Usuário criado com sucesso!"
            return False, "Erro ao criar registro."
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"

    def login(self, login: str, senha: str) -> Tuple[bool, Optional[Dict]]:
        """Autenticação de usuário."""
        # Busca pelo login (o Mixin já ignora os deletados logicamente)
        users = UserModel.find_all("UsrLgn = ?", (login,))
        
        if not users:
            return False, None
            
        user = users[0]
        stored_pwd = user['UsrPwd']
        
        # Verifica a senha (compatível com bcrypt)
        # Se as senhas antigas estiverem em SHA256, terás de migrar ou manter suporte duplo temporário
        try:
            if bcrypt.checkpw(senha.encode('utf-8'), stored_pwd.encode('utf-8')):
                return True, user
        except ValueError:
            # Fallback caso tenhas senhas antigas sem hash bcrypt (opcional)
            return False, None
            
        return False, None

    def reset_password(self, user_id: int) -> bool:
        """Reseta a senha para '123'."""
        # Gera hash da senha padrão
        default_pwd = bcrypt.hashpw('123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Instancia apenas com a PK e o campo a alterar
        user = UserModel(UsrCod=user_id, UsrPwd=default_pwd)
        
        # O update só altera o campo UsrPwd e a auditoria de update
        return user.update()

    def update_permission(self, user_id: int, new_role: str) -> bool:
        """Altera o perfil de acesso do usuário."""
        user = UserModel(UsrCod=user_id, UsrPrm=new_role)
        return user.update()

    def delete_user(self, user_id: int) -> bool:
        """Exclusão lógica do usuário."""
        user = UserModel(UsrCod=user_id)
        return user.delete()
    
    def get_profile(self, user_id: int) -> Dict:
        """Busca o perfil do usuário (T_UsrPrf)."""
        from src.models.UserProfileModel import UserProfileModel
        # Busca por FK (UsrPrfUsrCod)
        res = UserProfileModel.find_all("UsrPrfUsrCod = ?", (user_id,))
        return res[0] if res else {}

    def update_profile(self, user_id: int, data: Dict, file_obj=None) -> Tuple[bool, str]:
        """
        Atualiza ou Cria o perfil do usuário.
        Gerencia o upload da imagem se fornecido.
        """
        import os
        from src.core.config import Config
        from src.models.UserProfileModel import UserProfileModel
        
        # 1. Tratamento de Upload de Imagem
        if file_obj:
            try:
                # Garante diretório
                os.makedirs(Config.AVATAR_PATH, exist_ok=True)
                
                # Gera nome único: avatar_{user_id}.ext
                file_ext = os.path.splitext(file_obj.name)[1]
                file_name = f"avatar_{user_id}{file_ext}"
                save_path = os.path.join(Config.AVATAR_PATH, file_name)
                
                # Salva no disco
                with open(save_path, "wb") as f:
                    f.write(file_obj.getbuffer())
                
                # Adiciona caminho ao dict de dados
                data["UsrPrfFto"] = save_path
            except Exception as e:
                return False, f"Erro ao salvar imagem: {str(e)}"

        # 2. Persistência (Insert ou Update)
        try:
            # Verifica se já existe perfil para este usuário
            existing = self.get_profile(user_id)
            
            if existing:
                # Update (usando a PK do perfil encontrada)
                profile = UserProfileModel(UsrPrfCod=existing['UsrPrfCod'], **data)
                if profile.update():
                    return True, "Perfil atualizado com sucesso!"
            else:
                # Insert (Novo perfil)
                profile = UserProfileModel(UsrPrfUsrCod=user_id, **data)
                if profile.create():
                    return True, "Perfil criado com sucesso!"
            
            return False, "Erro ao gravar dados."
            
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"
    