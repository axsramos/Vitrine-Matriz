import sqlite3
import os
from src.core.config import Config

class Database:
    """
    Gerenciador de conexão com o banco de dados.
    Utiliza as configurações centralizadas de caminhos do Config.
    """
    
    def __init__(self):
        # Consome o caminho absoluto definido no config.py
        self.db_path = Config.DB_STR_PATH
        
        # Log de diagnóstico (Verifique isso no console!)
        if not os.path.exists(self.db_path):
            print(f"⚠️ AVISO: Banco de dados NÃO encontrado em: {self.db_path}")
            print(f"CWD atual: {os.getcwd()}")
        else:
            print(f"✅ Conectado ao banco em: {self.db_path}")

    def get_connection(self):
        """Retorna uma conexão ativa com suporte a dicionários."""
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"❌ Erro ao conectar ao SQLite ({self.db_path}): {e}")
            return None

    def execute(self, sql: str, params: tuple = ()) -> any:
        """Executa comandos de escrita (INSERT, UPDATE, DELETE)."""
        conn = self.get_connection()
        if not conn: return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            # Retorna o ID gerado em caso de INSERT
            return cursor.lastrowid if "INSERT" in sql.upper() else True
        except sqlite3.Error as e:
            print(f"❌ Erro na execução SQL: {e}\nQuery: {sql}")
            return None
        finally:
            conn.close()

    def select(self, sql: str, params: tuple = ()) -> list:
        """Executa consultas e retorna uma lista de dicionários."""
        conn = self.get_connection()
        if not conn: return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            # Converte sqlite3.Row para dict para compatibilidade total
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"❌ Erro na consulta SQL: {e}")
            return []
        finally:
            conn.close()