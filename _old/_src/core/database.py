import sqlite3
import os

class Database:
    def __init__(self):
        # Garante o caminho absoluto para a pasta 'database' na raiz do projeto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.db_path = os.path.join(project_root, "database", "vitrine.db")

    def get_connection(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)

    def select(self, query, params=()):
        """Executa SELECT e retorna lista de tuplas."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro SQL (Select): {e}\nQuery: {query}")
            return []
        finally:
            conn.close()

    def execute(self, query, params=()):
        """Executa INSERT/UPDATE/DELETE e retorna sucesso (Bool)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Erro SQL (Execute): {e}\nQuery: {query}")
            return False
        finally:
            conn.close()