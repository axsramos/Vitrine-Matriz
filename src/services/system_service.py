import os
import shutil
from datetime import datetime
from typing import Tuple, Dict
from src.core.config import Config

class SystemService:
    """
    Serviço responsável por operações de infraestrutura e sistema.
    Ex: Backups, Logs, Informações de Ambiente.
    """

    def create_database_backup(self) -> Tuple[bool, str]:
        """Gera uma cópia física do arquivo SQLite com timestamp."""
        try:
            # 1. Definição de Caminhos
            db_path = os.path.join(Config.BASE_DIR, Config.DB_NAME)
            backup_dir = os.path.join(Config.BASE_DIR, "backups")
            
            # 2. Garante que pasta de backup existe
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # 3. Verifica se o banco original existe
            if not os.path.exists(db_path):
                return False, "Arquivo de banco de dados original não encontrado."

            # 4. Gera nome do arquivo: vitrine_20231025_120000.db
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            db_name_clean = os.path.basename(Config.DB_NAME).split('.')[0]
            backup_filename = f"{db_name_clean}_{timestamp}.db"
            destination = os.path.join(backup_dir, backup_filename)
            
            # 5. Executa a cópia
            shutil.copy2(db_path, destination)
            
            return True, f"Backup salvo com sucesso em: {backup_filename}"

        except PermissionError:
            return False, "Permissão negada ao tentar gravar na pasta de backups."
        except Exception as e:
            return False, f"Erro inesperado no backup: {str(e)}"

    def get_system_info(self) -> Dict[str, str]:
        """Retorna dados do ambiente para exibição."""
        return {
            "Diretório Raiz": Config.BASE_DIR,
            "Banco de Dados": Config.DB_NAME,
            "Ambiente": os.getenv("ENV", "Development"),
            "Encoding": "UTF-8"
        }