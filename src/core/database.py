import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# DB_PATH_DEFAULT = os.path.join(BASE_DIR, "data", "database.db")
DB_PATH = os.getenv("DB_PATH", "data/database.db")

def get_connection():
    """Retorna uma conexão ativa com o SQLite."""
    # Garante que a pasta data/ existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)