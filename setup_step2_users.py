import sqlite3
import os

DB_PATH = "database/vitrine.db"

def create_user_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🚀 [PASSO 2] Iniciando migração de Usuários (Com Auditoria e Índices)...")

    try:
        # --- 1. Tabela T_Usr ---
        cursor.execute("DROP TABLE IF EXISTS T_Usr")
        cursor.execute("""
        CREATE TABLE T_Usr (
            UsrCod INTEGER PRIMARY KEY AUTOINCREMENT,
            UsrNom VARCHAR(255) NOT NULL,
            UsrLgn VARCHAR(255) NOT NULL UNIQUE,
            UsrPwd VARCHAR(255) NOT NULL,
            UsrPrm VARCHAR(255) DEFAULT 'user',
            
            -- Auditoria Completa
            UsrAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            UsrAudUpd DATETIME,
            UsrAudDlt DATETIME, -- Soft Delete
            UsrAudUsr VARCHAR(255)
        );
        """)
        # Índices de Performance
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_USR_01 ON T_Usr (UsrAudIns);")
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_USR_02 ON T_Usr (UsrNom);")
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_USR_03 ON T_Usr (UsrPrm, UsrNom);")
        print("✅ Tabela T_Usr recriada com sucesso.")

        # --- 2. Tabela T_UsrPrf ---
        cursor.execute("DROP TABLE IF EXISTS T_UsrPrf")
        cursor.execute("""
        CREATE TABLE T_UsrPrf (
            UsrPrfCod INTEGER PRIMARY KEY AUTOINCREMENT,
            UsrPrfBio VARCHAR(4000),
            UsrPrfFto VARCHAR(255),
            UsrPrfUrl VARCHAR(255),
            UsrPrfCgo VARCHAR(255),
            
            -- FK (1:1)
            UsrPrfUsrCod INTEGER UNIQUE,
            
            -- Auditoria Completa
            UsrPrfAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            UsrPrfAudUpd DATETIME,
            UsrPrfAudDlt DATETIME,
            UsrPrfAudUsr VARCHAR(255),
            
            FOREIGN KEY(UsrPrfUsrCod) REFERENCES T_Usr(UsrCod) ON DELETE CASCADE
        );
        """)
        print("✅ Tabela T_UsrPrf recriada com sucesso.")

        # --- 3. Dados Iniciais (Admin) ---
        # Inserindo com o Hash SHA256 que você forneceu
        cursor.execute("""
        INSERT INTO T_Usr (UsrNom, UsrLgn, UsrPwd, UsrPrm) 
        VALUES ('Administrador', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');
        """)
        
        cursor.execute("""
        INSERT INTO T_UsrPrf (UsrPrfBio, UsrPrfFto, UsrPrfUrl, UsrPrfCgo, UsrPrfUsrCod)
        VALUES ('Administrador do sistema', 'admin.png', 'admin.com', 'Administrador', 1);
        """)
        print("👤 Usuário Admin inserido.")

        conn.commit()
        print("\n🏁 Migração concluída!")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_user_tables()