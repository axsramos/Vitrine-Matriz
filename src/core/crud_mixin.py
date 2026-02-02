from typing import List, Optional, Dict, Any
from src.core.database import Database
from src.helpers.date_helper import DateHelper
from src.helpers.session_helper import SessionHelper

class CrudMixin:
    """
    Mixin aprimorado com:
    - Auditoria Automática (Helpers).
    - Seleção Explícita de Campos (Performance e Segurança).
    """

    def __init__(self, **kwargs):
        self._attributes = {}
        if hasattr(self, 'FIELDS'):
            for field in self.FIELDS:
                if field in kwargs:
                    self._attributes[field] = kwargs[field]

    # --- MÉTODOS MÁGICOS (Mantidos) ---
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

    # --- MÉTODOS DE ESCRITA (COMMANDS - Mantidos iguais) ---
    def create(self) -> bool:
        fields_to_insert = {k: v for k, v in self._attributes.items() if v is not None}
        
        aud_ins = self._get_audit_field("AudIns")
        if aud_ins: fields_to_insert[aud_ins] = DateHelper.get_db_timestamp()
            
        aud_usr = self._get_audit_field("AudUsr")
        if aud_usr: fields_to_insert[aud_usr] = SessionHelper.get_current_user_login()

        if not fields_to_insert: return False

        cols = ", ".join(fields_to_insert.keys())
        placeholders = ", ".join(["?"] * len(fields_to_insert))
        values = list(fields_to_insert.values())
        
        sql = f"INSERT INTO {self.TABLE_NAME} ({cols}) VALUES ({placeholders})"
        db = Database()
        db.execute(sql, tuple(values))
        return True

    def update(self) -> bool:
        pk_field = self.FIELDS_PK[0]
        pk_val = self._attributes.get(pk_field)
        
        if not pk_val: raise ValueError(f"Update falhou: PK {pk_field} não definida.")

        fields_to_update = {k: v for k, v in self._attributes.items() if k != pk_field}
        
        aud_upd = self._get_audit_field("AudUpd")
        if aud_upd: fields_to_update[aud_upd] = DateHelper.get_db_timestamp()
            
        aud_usr = self._get_audit_field("AudUsr")
        if aud_usr: fields_to_update[aud_usr] = SessionHelper.get_current_user_login()

        if not fields_to_update: return False

        set_clause = ", ".join([f"{k} = ?" for k in fields_to_update.keys()])
        values = list(fields_to_update.values())
        values.append(pk_val)

        sql = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {pk_field} = ?"
        db = Database()
        db.execute(sql, tuple(values))
        return True

    def delete(self, hard_delete: bool = False) -> bool:
        pk_field = self.FIELDS_PK[0]
        pk_val = self._attributes.get(pk_field)
        if not pk_val: return False
        
        db = Database()
        audit_dlt = self._get_audit_field("AudDlt")
        
        if audit_dlt and not hard_delete:
            aud_usr = self._get_audit_field("AudUsr")
            set_clauses = [f"{audit_dlt} = ?"]
            params = [DateHelper.get_db_timestamp()]
            
            if aud_usr:
                set_clauses.append(f"{aud_usr} = ?")
                params.append(SessionHelper.get_current_user_login())
            
            params.append(pk_val)
            sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clauses)} WHERE {pk_field} = ?"
            db.execute(sql, tuple(params))
        else:
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE {pk_field} = ?"
            db.execute(sql, (pk_val,))
        return True

    # --- MÉTODOS DE LEITURA (QUERIES - Refatorados) ---

    @classmethod
    def get_by_id(cls, pk_value: Any, fields: List[str] = None) -> Optional[Dict]:
        """
        Busca registro pelo ID.
        :param pk_value: Valor da chave primária.
        :param fields: (Opcional) Lista de campos específicos para retornar.
        """
        db = Database()
        pk_field = cls.FIELDS_PK[0]
        
        # Define quais colunas buscar (SELECT col1, col2...)
        selected_cols = cls._get_valid_fields(fields)
        cols_sql = ", ".join(selected_cols)
        
        sql = f"SELECT {cols_sql} FROM {cls.TABLE_NAME} WHERE {pk_field} = ?"
        result = db.select(sql, (pk_value,))
        return result[0] if result else None

    @classmethod
    def find_all(cls, where: str = None, params: tuple = None, fields: List[str] = None) -> List[Dict]:
        """
        Busca lista de registros.
        :param fields: (Opcional) Lista de campos específicos para retornar.
        """
        db = Database()
        
        # Define quais colunas buscar
        selected_cols = cls._get_valid_fields(fields)
        cols_sql = ", ".join(selected_cols)
        
        sql = f"SELECT {cols_sql} FROM {cls.TABLE_NAME}"
        
        # Tratamento de Soft Delete
        if hasattr(cls, 'FIELDS_AUDIT'):
            audit_dlt = next((f for f in cls.FIELDS_AUDIT if "AudDlt" in f), None)
            if audit_dlt:
                clause = f"{audit_dlt} IS NULL"
                if where:
                    where = f"({where}) AND {clause}"
                else:
                    where = clause

        if where:
            sql += f" WHERE {where}"
            
        return db.select(sql, params or ())
    
    @classmethod
    def paginate(cls, page: int = 1, page_size: int = 10, where: str = None, params: tuple = None, fields: List[str] = None) -> Dict[str, Any]:
        """
        Busca registros de forma paginada.
        Retorna um dicionário contendo os dados e metadados de paginação.
        
        :param page: Número da página atual (inicia em 1).
        :param page_size: Quantidade de registros por página.
        :param where: Filtros SQL (ex: "UsrNom LIKE ?").
        :param params: Tupla de parâmetros para o filtro.
        :param fields: Lista de campos específicos para retornar.
        """
        db = Database()
        params = params or ()
        
        # 1. Construção da Cláusula WHERE (Reaproveitando lógica de Soft Delete)
        filters = []
        
        # Filtro de Soft Delete (apenas ativos)
        if hasattr(cls, 'FIELDS_AUDIT'):
            audit_dlt = next((f for f in cls.FIELDS_AUDIT if "AudDlt" in f), None)
            if audit_dlt:
                filters.append(f"{audit_dlt} IS NULL")
        
        # Filtro personalizado (argumento where)
        if where:
            filters.append(f"({where})")
            
        where_clause = " WHERE " + " AND ".join(filters) if filters else ""

        # 2. Query de Contagem (Total de itens correspondentes ao filtro)
        # Necessário para calcular o total de páginas
        sql_count = f"SELECT COUNT(*) FROM {cls.TABLE_NAME}{where_clause}"
        res_count = db.select(sql_count, params)
        
        total_items = 0
        if res_count:
            row = res_count[0]
            # Tratamento para garantir leitura correta (dict ou tupla)
            if isinstance(row, dict):
                total_items = list(row.values())[0]
            elif isinstance(row, (list, tuple)):
                total_items = row[0]

        # 3. Cálculos de Paginação
        if page < 1: page = 1
        total_pages = (total_items + page_size - 1) // page_size
        offset = (page - 1) * page_size

        # 4. Query de Dados (SELECT com LIMIT e OFFSET)
        selected_cols = cls._get_valid_fields(fields) # Usa o validador que criamos
        cols_sql = ", ".join(selected_cols)
        
        # Adiciona LIMIT e OFFSET à query
        sql_data = f"SELECT {cols_sql} FROM {cls.TABLE_NAME}{where_clause} LIMIT ? OFFSET ?"
        
        # Os parâmetros finais são: params do where + limit + offset
        data_params = params + (page_size, offset)
        
        items = db.select(sql_data, data_params)

        # 5. Retorno Estruturado
        return {
            "data": items,          # A lista de registros desta página
            "meta": {               # Metadados para montar a UI de paginação
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
    @classmethod
    def exists(cls, pk_value: Any) -> bool:
        db = Database()
        pk_field = cls.FIELDS_PK[0]
        sql = f"SELECT 1 FROM {cls.TABLE_NAME} WHERE {pk_field} = ? LIMIT 1"
        res = db.select(sql, (pk_value,))
        return len(res) > 0
    
    @classmethod
    def count(cls, include_deleted: bool = False) -> int:
        """
        Retorna a quantidade total de registros.
        :param include_deleted: Se False (padrão), ignora os registros excluídos logicamente.
        """
        db = Database()
        sql = f"SELECT COUNT(*) FROM {cls.TABLE_NAME}"
        
        # Lógica de Filtro para Soft Delete (apenas Ativos)
        if not include_deleted and hasattr(cls, 'FIELDS_AUDIT'):
            # Procura o campo de auditoria de deleção (ex: UsrAudDlt)
            audit_dlt = next((f for f in cls.FIELDS_AUDIT if "AudDlt" in f), None)
            if audit_dlt:
                sql += f" WHERE {audit_dlt} IS NULL"

        result = db.select(sql)
        
        # Tratamento do retorno (SQLite pode retornar dict ou tuple dependendo da config)
        if result:
            row = result[0]
            if isinstance(row, dict):
                # Pega o primeiro valor do dicionário (ex: {'COUNT(*)': 10})
                return list(row.values())[0]
            elif isinstance(row, (list, tuple)):
                # Pega o primeiro índice da tupla (ex: (10,))
                return row[0]
            
        return 0

    # --- HELPERS INTERNOS ---

    def _get_audit_field(self, suffix: str):
        if hasattr(self, 'FIELDS_AUDIT'):
            return next((f for f in self.FIELDS_AUDIT if suffix in f), None)
        return None

    @classmethod
    def _get_valid_fields(cls, requested_fields: List[str] = None) -> List[str]:
        """
        Valida se os campos solicitados existem no MD da classe.
        Se nenhum for válido ou informado, retorna TODOS os campos (cls.FIELDS).
        """
        if not requested_fields:
            return cls.FIELDS
            
        # Filtra apenas campos que realmente existem no modelo (Segurança)
        valid_fields = [f for f in requested_fields if f in cls.FIELDS]
        
        # Se o filtro resultou em lista vazia (ex: campos errados), assume todos
        return valid_fields if valid_fields else cls.FIELDS