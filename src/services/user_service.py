import hashlib
from src.models.UserModel import UserModel
from src.models.UserProfileModel import UserProfileModel

class UserService:
    def _hash_password(self, password):
        """Gera hash SHA256 para comparar com o banco."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password):
        model = UserModel()
        password_hash = self._hash_password(password)
        
        # Busca usuário ativo (UsrAudDlt IS NULL)
        # Atenção: Usando UsrPrm se precisar validar permissão depois
        users = model.read_all(
            where="UsrLgn = ? AND UsrPwd = ? AND UsrAudDlt IS NULL", 
            params=(username, password_hash)
        )
        
        return users[0] if users else None

    def get_user_profile(self, user_id):
        model = UserProfileModel()
        profiles = model.read_all(where="UsrPrfUsrCod = ?", params=(user_id,))
        return profiles[0] if profiles else {}
    
    def update_profile(self, user_id, profile_data: dict):
        """Cria ou Atualiza o perfil."""
        model = UserProfileModel()
        
        # Verifica se já existe
        existing = model.read_all(where="UsrPrfUsrCod = ?", params=(user_id,))
        
        if existing:
            # Atualiza objeto existente
            current_data = existing[0]
            model = UserProfileModel(**current_data)
            
            # Atualiza campos recebidos
            for k, v in profile_data.items():
                if hasattr(model, k):
                    setattr(model, k, v)
        else:
            # Cria novo
            model = UserProfileModel(**profile_data)
            model.UsrPrfUsrCod = user_id
            
        return model.save()