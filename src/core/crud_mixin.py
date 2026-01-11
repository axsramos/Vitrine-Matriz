import sqlite3
from datetime import datetime
from src.core.database import get_connection

class CrudMixin:
    """Implementação Python da lógica contida no CrudOperationsTrait.php"""

    def _get_audit_user(self):
        # Placeholder para o seu sistema de sessão/usuário
        return "SISTEMA"

    def create(self):
        """Versão corrigida para lidar com IDs autoincrementais."""
        dt_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.att['AudIns'] = dt_now
        self.att['AudUpd'] = dt_now
        self.att['AudUsr'] = self._get_audit_user()
        
        # Filtra campos: só inclui campos que estão em self.att
        # Isso permite que o 'id' seja omitido e o SQLite gere o autoincrement
        insert_fields = [f for f in self.FIELDS if f in self.att]
        
        fields_str = ", ".join(insert_fields)
        placeholders = ", ".join([f":{f}" for f in insert_fields])
        
        query = f"INSERT INTO {self.TABLE_NAME} ({fields_str}) VALUES ({placeholders})"
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, self.att)
            conn.commit()
            return cursor.lastrowid

    def read(self, pk_values: dict):
        """Equivalente ao readRegister() utilizando chaves primárias"""
        where_clause = " AND ".join([f"{pk} = :{pk}" for pk in self.FIELDS_PK])
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {where_clause} LIMIT 1"
        
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, pk_values)
            row = cursor.fetchone()
            if row:
                self.att = dict(row)
                return True
            return False

    def update(self):
        """Versão dinâmica: atualiza apenas os campos presentes em self.att."""
        dt_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.att['AudUpd'] = dt_now
        self.att['AudUsr'] = self._get_audit_user()

        # 1. Identifica quais campos devem ser atualizados (excluindo as chaves primárias)
        # Apenas campos que existem em self.FIELDS e foram passados em self.att
        update_fields = [f for f in self.FIELDS if f in self.att and f not in self.FIELDS_PK]
        
        if not update_fields:
            return False # Nada para atualizar

        set_clause = ", ".join([f"{f} = :{f}" for f in update_fields])
        
        # 2. Monta a cláusula WHERE com as chaves primárias
        where_clause = " AND ".join([f"{f} = :{f}" for f in self.FIELDS_PK])
        
        # 3. Verifica se os valores das PKs estão presentes
        for pk in self.FIELDS_PK:
            if pk not in self.att:
                raise ValueError(f"Chave primária '{pk}' não fornecida para atualização.")

        query = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {where_clause}"

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, self.att)
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, logical=True):
        """Suporta exclusão lógica (LOGICAL_EXCLUSION) ou física"""
        where_clause = " AND ".join([f"{pk} = :{pk}" for pk in self.FIELDS_PK])
        
        if logical:
            # Exclusão lógica
            dt_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = f"UPDATE {self.TABLE_NAME} SET AudDlt = '{dt_now}', AudUsr = '{self._get_audit_user()}' WHERE {where_clause}"
        else:
            query = f"DELETE FROM {self.TABLE_NAME} WHERE {where_clause}"
            
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, self.att)
            conn.commit()
            return cursor.rowcount > 0