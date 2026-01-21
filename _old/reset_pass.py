from src.services.auth_service import AuthService
from src.core.database import get_connection

auth = AuthService()
hash_admin = auth.make_hash("admin123")

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = 'admin'") # Limpa anterior
    cursor.execute(
        "INSERT INTO usuarios (nome, username, password_hash, role) VALUES (?, ?, ?, ?)",
        ('Administrador', 'admin', hash_admin, 'Admin')
    )
    conn.commit()
print("Usuário admin resetado com sucesso usando o hash do sistema!")