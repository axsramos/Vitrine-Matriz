import hashlib
import pandas as pd
from src.core.database import get_connection

class UserService:
    def get_all(self):
        """Retorna todos os usuários (sem o hash da senha por segurança)."""
        query = "SELECT id, nome, username, role FROM usuarios"
        with get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def create(self, nome, username, password, role="Admin"):
        """Cria um novo usuário com senha criptografada."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = "INSERT INTO usuarios (nome, username, password_hash, role) VALUES (?, ?, ?, ?)"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nome, username, password_hash, role))
            conn.commit()

    def delete(self, user_id):
        """Remove um usuário pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conn.commit()
    
    def update_password(self, user_id, new_password):
        """Atualiza a senha de um usuário específico."""
        import hashlib
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        query = "UPDATE usuarios SET password_hash = ?, AudUpd = CURRENT_TIMESTAMP WHERE id = ?"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (password_hash, user_id))
            conn.commit()