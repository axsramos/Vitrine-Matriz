import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega as variáveis do arquivo .env
load_dotenv()

class Config:
    # --- AMBIENTE E UI ---
    ENV = os.getenv("APP_ENV", "local")
    APP_TITLE = os.getenv("APP_TITLE", "Vitrine Matriz")
    APP_SUBTITLE = os.getenv("APP_SUBTITLE", "Portal de Transparência e Performance")

    # --- CAMINHOS DE DIRETÓRIO (DINÂMICO) ---
    # Localiza a raiz do projeto a partir deste arquivo (src/core/config.py)
    # Sobe dois níveis: core -> src -> raiz
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    # Padronização conforme o PASSO 1 da revisão
    DB_DIR = BASE_DIR / "database"
    UPLOAD_DIR = DB_DIR / "uploads" / "avatars"
    
    # Garante que a pasta database existe
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Garante que as pastas de upload existam
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # --- IMAGENS PADRÃO (ASSETS) ---
    # Caminhos relativos à raiz do projeto
    ASSETS_DIR = BASE_DIR / "src" / "ui" / "assets"
    
    # Garante que a pasta de assets exista
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Parametrizado via .env ou assume o padrão
    DEFAULT_USER_IMG = os.getenv("DEFAULT_USER_IMG", str(ASSETS_DIR / "default_user.png"))
    LOGO_IMG = os.getenv("LOGO_IMG", str(ASSETS_DIR / "logo.png"))

    # --- BANCO DE DADOS ---
    DB_DRIVER = os.getenv("DB_DRIVER", "sqlite")
    DB_NAME = os.getenv("DB_NAME", "vitrine.db") 

    # Caminho FINAL absoluto
    DB_PATH = DB_DIR / DB_NAME
    
    # Para facilitar o uso no SQLite nativo (string)
    DB_STR_PATH = str(DB_PATH)
    
    # --- UPLOAD CONFIG ---
    # Caminho absoluto para salvar as fotos
    AVATAR_PATH = str(UPLOAD_DIR)

    # --- SEGURANÇA E SESSÃO ---
    SECRET_KEY = os.getenv("SECRET_KEY", "vitrine_secret_123")