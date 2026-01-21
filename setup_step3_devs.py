import sqlite3
import os

DB_PATH = "database/vitrine.db"

def create_dev_table():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🚀 [PASSO 3] Iniciando migração de Desenvolvedores (T_Dev)...")

    try:
        cursor.execute("DROP TABLE IF EXISTS T_Dev")
        
        # Tabela T_Dev
        # DevNom é redundante com UsrNom, mas útil para performance em Dropdowns de tarefas
        cursor.execute("""
        CREATE TABLE T_Dev (
            DevCod INTEGER PRIMARY KEY AUTOINCREMENT,
            DevNom VARCHAR(255) NOT NULL,
            DevUsrCod INTEGER UNIQUE,
            
            -- Auditoria Completa (Padrão AudMD)
            DevAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            DevAudUpd DATETIME,
            DevAudDlt DATETIME,
            DevAudUsr VARCHAR(255),
            
            FOREIGN KEY(DevUsrCod) REFERENCES T_Usr(UsrCod) ON DELETE CASCADE
        );
        """)
        
        # Índices
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_DEV_01 ON T_Dev (DevUsrCod);")
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_DEV_02 ON T_Dev (DevNom);")
        
        print("✅ Tabela T_Dev recriada com sucesso.")

        # Opcional: Promover o Admin a Desenvolvedor para testes iniciais
        cursor.execute("""
        INSERT INTO T_Dev (DevNom, DevUsrCod, DevAudUsr)
        VALUES ('Administrador', 1, 'system_setup');
        """)
        print("👤 Admin promovido a Desenvolvedor para testes.")

        conn.commit()
        print("\n🏁 Migração de Desenvolvedores concluída!")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_dev_table()