import sqlite3
import os
from src.core.config import Config

def fix_database():
    print("🕵️ INICIANDO DIAGNÓSTICO DO BANCO DE DADOS...")
    
    # 1. Verifica o Caminho do Banco
    db_path = Config.DB_PATH
    print(f"📂 Caminho do Banco definido no Config: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ ARQUIVO DE BANCO NÃO ENCONTRADO! Um novo será criado, mas estará vazio.")
    else:
        print("✅ Arquivo de banco encontrado.")

    # 2. Conecta e Verifica Tabelas
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lista todas as tabelas atuais
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tabelas existentes: {tables}")

        # 3. Verifica se a tabela nova T_Tsk existe
        if 'T_Tsk' in tables or 'T_TSK' in tables:
            print("✅ A tabela T_Tsk JÁ EXISTE. O problema pode ser outro (permissão ou cache).")
            # Tenta um select simples para validar
            try:
                cursor.execute("SELECT COUNT(*) FROM T_TSK")
                count = cursor.fetchone()[0]
                print(f"📊 Total de tarefas na tabela nova: {count}")
            except Exception as e:
                print(f"❌ Erro ao ler T_TSK: {e}")
        else:
            print("⚠️ A tabela T_Tsk NÃO EXISTE. Iniciando migração forçada...")
            
            # 4. Executa os Scripts de Refatoração (Força Bruta)
            migrations = [
                'migrations/004_refactory_schemas.sql',
                'migrations/005_copy_data.sql'
            ]
            
            for migration_file in migrations:
                if os.path.exists(migration_file):
                    print(f"🚀 Executando {migration_file}...")
                    with open(migration_file, 'r', encoding='utf-8') as f:
                        sql_script = f.read()
                        cursor.executescript(sql_script)
                    print(f"✅ {migration_file} aplicado com sucesso.")
                else:
                    print(f"❌ ARQUIVO DE MIGRAÇÃO NÃO ENCONTRADO: {migration_file}")
            
            conn.commit()
            print("💾 Alterações salvas (COMMIT realizado).")
            
            # Validação Final
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            new_tables = [row[0] for row in cursor.fetchall()]
            if 'T_TSK' in new_tables or 'T_Tsk' in new_tables:
                print("🎉 SUCESSO! A tabela T_Tsk foi criada.")
            else:
                print("❌ FALHA CRÍTICA: A tabela ainda não aparece após a migração.")

    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
    finally:
        if conn:
            conn.close()
        print("🏁 FIM DO DIAGNÓSTICO.")

if __name__ == "__main__":
    fix_database()