import sqlite3
import os

DB_PATH = "database/vitrine.db"

def create_task_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🚀 [PASSO 4] Migração de Releases e Tarefas...")

    try:
        # --- 1. Tabela T_Rel (Releases) ---
        cursor.execute("DROP TABLE IF EXISTS T_Rel")
        cursor.execute("""
        CREATE TABLE T_Rel (
            RelCod INTEGER PRIMARY KEY AUTOINCREMENT,
            RelVrs VARCHAR(50) NOT NULL,    -- Versão (ex: 1.0.0)
            RelTtlCmm VARCHAR(255),         -- Título/Comentário
            RelDat DATE,                    -- Data da Publicação
            
            -- Auditoria
            RelAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            RelAudUpd DATETIME,
            RelAudDlt DATETIME,
            RelAudUsr VARCHAR(255)
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_REL_01 ON T_Rel (RelVrs);")
        print("✅ Tabela T_Rel criada.")

        # --- 2. Tabela T_Trf (Tarefas - Antiga T_Tsk) ---
        cursor.execute("DROP TABLE IF EXISTS T_Trf")
        cursor.execute("""
        CREATE TABLE T_Trf (
            TrfCod INTEGER PRIMARY KEY AUTOINCREMENT,
            TrfTtl VARCHAR(150) NOT NULL,
            TrfDesc VARCHAR(4000),
            TrfPrio VARCHAR(20) DEFAULT 'Média',
            TrfImp VARCHAR(20) DEFAULT 'Médio',  -- Campo Impacto
            TrfStt VARCHAR(50) DEFAULT 'A Fazer',
            TrfDatEnt DATE,
            
            -- FKs
            TrfDevCod INTEGER,
            TrfRelCod INTEGER,
            
            -- Auditoria
            TrfAudIns DATETIME DEFAULT CURRENT_TIMESTAMP,
            TrfAudUpd DATETIME,
            TrfAudDlt DATETIME,
            TrfAudUsr VARCHAR(255),
            
            FOREIGN KEY(TrfDevCod) REFERENCES T_Dev(DevCod) ON DELETE SET NULL,
            FOREIGN KEY(TrfRelCod) REFERENCES T_Rel(RelCod) ON DELETE SET NULL
        );
        """)
        
        # Índices de Performance
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_TRF_01 ON T_Trf (TrfDevCod);") -- Filtro por Dev
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_TRF_02 ON T_Trf (TrfRelCod);") -- Filtro por Release
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_TRF_03 ON T_Trf (TrfStt);")    -- Filtro por Status
        cursor.execute("CREATE INDEX IF NOT EXISTS IDX_TRF_04 ON T_Trf (TrfAudDlt);") -- Filtro de Exclusão Lógica
        
        print("✅ Tabela T_Trf criada.")

        conn.commit()
        print("\n🏁 Migração do Passo 4 concluída!")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_task_tables()