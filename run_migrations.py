import sqlite3
import os
from src.core.database import Database

def run_migrations():
    conn = Database().get_connection()
    cursor = conn.cursor()

    # Cria tabela de controlo de versões
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            migration_name TEXT UNIQUE NOT NULL,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    migration_path = 'migrations'
    if not os.path.exists(migration_path):
        os.makedirs(migration_path)
        
    # Lista e ordena os ficheiros SQL
    files = sorted([f for f in os.listdir(migration_path) if f.endswith('.sql')])

    for file in files:
        cursor.execute("SELECT id FROM schema_migrations WHERE migration_name = ?", (file,))
        if cursor.fetchone() is None:
            print(f"⚙️ A aplicar migração: {file}...")
            try:
                with open(os.path.join(migration_path, file), 'r', encoding='utf-8') as f:
                    sql = f.read()
                    cursor.executescript(sql)
                
                cursor.execute("INSERT INTO schema_migrations (migration_name) VALUES (?)", (file,))
                conn.commit()
                print(f"✅ {file} aplicada com sucesso.")
            except Exception as e:
                conn.rollback()
                print(f"❌ Erro em {file}: {e}")
                break
        else:
            print(f"⏭️ Ignorada (já aplicada): {file}")

    conn.close()

if __name__ == "__main__":
    run_migrations()