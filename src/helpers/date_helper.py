from datetime import datetime

class DateHelper:
    @staticmethod
    def get_db_timestamp() -> str:
        """Retorna o timestamp atual no formato padrão do SQLite (YYYY-MM-DD HH:MM:SS)."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')