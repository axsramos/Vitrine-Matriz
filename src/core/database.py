import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "data/database.db")

def get_connection():
    """Retorna uma conexão ativa com o SQLite."""
    # Garante que a pasta data/ existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)