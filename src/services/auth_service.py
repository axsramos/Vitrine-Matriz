import hashlib
from src.core.database import get_connection

class AuthService:
    @staticmethod
    def make_hash(password: str) -> str:
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_login(self, username, password):
        hash_tentativa = self.make_hash(password)
        # DEBUG: Copie o valor que sair no terminal e compare com o banco
        print(f"DEBUG - Hash Gerado: {hash_tentativa}")
    
        query = "SELECT id, nome, role FROM usuarios WHERE username = ? AND password_hash = ?"
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, hash_tentativa))
            user = cursor.fetchone()
            
            if user:
                return {"id": user[0], "nome": user[1], "role": user[2]}
            return None