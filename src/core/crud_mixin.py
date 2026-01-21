import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from src.core.database import Database

class CrudMixin:
    """
    Mixin que implementa CRUD dinâmico baseado nos metadados (MD) da classe.
    Padronizado para suportar Auditoria e Soft Delete.
    """

    def __init__(self, **kwargs):
        self._attributes = {}
        if hasattr(self, 'FIELDS'):
            for field in self.FIELDS:
                self._attributes[field] = kwargs.get(field, None)

    def __setattr__(self, name, value):
        if name != '_attributes' and hasattr(self, 'FIELDS') and name in self.FIELDS:
            self._attributes[name] = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "_attributes":
            return super().__getattribute__(name)
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def save(self) -> bool:
        """Decide entre INSERT ou UPDATE e gerencia campos de auditoria."""
        pk_field = self.FIELDS_PK[0]
        pk_val = self._attributes.get(pk_field)
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Identifica campos de auditoria baseados no prefixo da tabela (ex: TrfAud...)
        # ou usa o mapeamento do FIELDS_AUDIT definido no MD
        audit_ins = next((f for f in self.FIELDS_AUDIT if "AudIns" in f), None)
        audit_upd = next((f for f in self.FIELDS_AUDIT if "AudUpd" in f), None)

        if pk_val is None or pk_val == 0:
            # Lógica de INSERT
            if audit_ins: self._attributes[audit_ins] = now
            
            fields = [f for f in self.FIELDS if f != pk_field]
            columns = ", ".join(fields)
            placeholders = ", ".join(["?" for _ in fields])
            values = tuple(self._attributes.get(f) for f in fields)
            
            sql = f"INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({placeholders})"
            db = Database()
            last_id = db.execute(sql, values)
            if last_id:
                self._attributes[pk_field] = last_id
                return True
        else:
            # Lógica de UPDATE
            if audit_upd: self._attributes[audit_upd] = now
            
            fields = [f for f in self.FIELDS if f != pk_field and f not in self.FIELDS_AUDIT or f == audit_upd]
            set_clause = ", ".join([f"{f} = ?" for f in fields])
            values = tuple(self._attributes.get(f) for f in fields) + (pk_val,)
            
            sql = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {pk_field} = ?"
            db = Database()
            db.execute(sql, values)
            return True
        
        return False

    def read_all(self, where: str = None, params: tuple = (), include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Lê registros, filtrando por padrão os excluídos logicamente."""
        db = Database()
        sql = f"SELECT * FROM {self.TABLE_NAME}"
        
        filters = []
        # Regra de Soft Delete
        audit_dlt = next((f for f in self.FIELDS_AUDIT if "AudDlt" in f), None)
        if audit_dlt and not include_deleted:
            filters.append(f"{audit_dlt} IS NULL")
            
        if where:
            filters.append(where)
            
        if filters:
            sql += " WHERE " + " AND ".join(filters)
            
        return db.select(sql, params)

    def delete(self, hard_delete: bool = False) -> bool:
        """Realiza exclusão lógica (padrão) ou física."""
        pk_field = self.FIELDS_PK[0]
        pk_val = self._attributes.get(pk_field)
        if not pk_val: return False
        
        db = Database()
        audit_dlt = next((f for f in self.FIELDS_AUDIT if "AudDlt" in f), None)
        
        if audit_dlt and not hard_delete:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = f"UPDATE {self.TABLE_NAME} SET {audit_dlt} = ? WHERE {pk_field} = ?"
            db.execute(sql, (now, pk_val))
        else:
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE {pk_field} = ?"
            db.execute(sql, (pk_val,))
        return True

    def read_by_field(self, field_name: str, value: Any):
        """Busca um único registro por um campo específico."""
        results = self.read_all(where=f"{field_name} = ?", params=(value,))
        if results:
            for key, val in results[0].items():
                setattr(self, key, val)
            return True
        return False