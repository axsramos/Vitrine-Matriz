import sys
import os

# Adiciona o diretório atual ao path para garantir que o Python encontre o módulo 'src'
sys.path.append(os.getcwd())

from src.services.user_service import UserService
from src.models.UserProfileModel import UserProfileModel
from src.models.UserRole import UserRole
from src.core.database import Database

def seed_admin():
    print("🌱 Iniciando semeadura do banco de dados...")

    u_service = UserService()
    
    # Dados do Admin
    LOGIN = "admin"
    SENHA = "123"
    NOME = "Administrador do Sistema"
    ROLE = UserRole.ADMIN

    # 1. Verifica se já existe para evitar duplicação
    # Usamos find_all do mixin para verificar existência
    existing = u_service.get_all_users()
    admin_exists = any(u['UsrLgn'] == LOGIN for u in existing)

    if admin_exists:
        print(f"⚠️  O usuário '{LOGIN}' já existe. Ignorando criação.")
    else:
        # 2. Cria o Usuário (A senha será hashada automaticamente pelo Service)
        success, msg = u_service.create_user(LOGIN, NOME, SENHA, ROLE)
        
        if success:
            print(f"✅ Usuário '{LOGIN}' criado com sucesso.")
            
            # 3. Cria o Perfil (Necessário para evitar erros na UI ao carregar avatar/bio)
            # Precisamos recuperar o ID do usuário recém-criado
            # O create_user não retorna o ID, então buscamos pelo login
            users = u_service.login(LOGIN, SENHA) # Ou busca direta
            if users and isinstance(users, tuple): 
                 # Ajuste: se o seu login retorna (bool, user_dict), pegamos o dict
                 user_data = users[1]
            else:
                # Fallback caso o login falhe ou retorne diferente, buscamos na base
                # Nota: O login retorna (bool, dict) na versão refatorada
                res = u_service.get_all_users()
                user_data = next((u for u in res if u['UsrLgn'] == LOGIN), None)

            if user_data:
                user_id = user_data['UsrCod']
                
                # Cria perfil padrão
                profile = UserProfileModel(
                    UsrPrfUsrCod=user_id,
                    UsrPrfCgo="Super Admin",
                    UsrPrfBio="Conta de administração gerada via Seed.",
                    UsrPrfUrl="http://localhost"
                )
                
                if profile.create():
                    print("✅ Perfil do Admin vinculado com sucesso.")
                else:
                    print("❌ Erro ao criar perfil do Admin.")
            else:
                print("❌ Erro ao recuperar ID do Admin recém-criado.")
        else:
            print(f"❌ Falha ao criar usuário: {msg}")

    print("🏁 Semeadura concluída.")

if __name__ == "__main__":
    # Garante que as tabelas existem antes de inserir
    # Se você tiver um método db.init_db(), pode chamá-lo aqui, 
    # ou assumimos que você já rodou as migrações SQL limpas.
    db = Database()
    # db.init_db() # Descomente se quiser forçar a criação das tabelas aqui
    
    seed_admin()