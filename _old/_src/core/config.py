import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega as variáveis do arquivo .env
load_dotenv()

APP_TITLE = 'APP_TITLE'
APP_SUBTITLE = 'APP_SUBTITLE'
    
class Config:
    # Ambiente
    ENV = os.getenv("APP_ENV", "local")

    # Configurações de UI
    APP_TITLE = os.getenv("APP_TITLE", "Vitrine Matriz")
    APP_SUBTITLE = os.getenv("APP_SUBTITLE", "Portal de Transparência e Performance")

    DB_DRIVER = os.getenv("DB_DRIVER", "sqlite")
    
    # 1. Localiza a raiz do projeto
    current_file = Path(__file__).resolve()
    BASE_DIR = current_file.parent.parent.parent
    
    # 2. Define explicitamente a pasta de dados
    DATA_DIR = BASE_DIR / "data"
    
    # 3. Garante que a pasta existe (importante para evitar erros de I/O)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Configurações do Banco vindas do .env ou valores default
    DB_NAME = os.getenv("DB_NAME", "database.db") 

    # 5. Monta o caminho FINAL absoluto dentro da pasta data
    DB_PATH = DATA_DIR / DB_NAME
    

