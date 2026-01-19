import os
from typing import List, Optional, Dict, Any
from src.core.database import Database

class CrudMixin:
    """
    Mixin que implementa CRUD dinâmico baseado nos metadados (MD) da classe.
    Similar ao CrudOperationsTrait.php.
    """

    def __init__(self, **kwargs):
        self._attributes = {}
        # Inicializa atributos baseado no FIELDS do Metadata
        if hasattr(self, 'FIELDS'):
            for field in self.FIELDS:
                self._attributes[field] = kwargs.get(field, None)

    # --- Magic Methods para acesso tipo obj.Campo = Valor ---
    def __setattr__(self, name, value):
        if hasattr(self, 'FIELDS') and name in self.FIELDS:
            self._attributes[name] = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "_attributes":
            return super().__getattribute__(name)
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    # --- MÉTODOS DE ESCRITA (Active Record) ---
    
    def save(self):
        """Decide entre INSERT ou UPDATE baseado na PK."""
        pk_field = self.FIELDS_PK[0]
        pk_val = self._attributes.get(pk_field)

        if pk_val and self._record_exists(pk_val):
            return self._update()
        else:
            return self._insert()
        
        self.connection.commit()

    def _insert(self):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        # Filtra campos preenchidos
        fields_to_save = [f for f in self.FIELDS if self._attributes.get(f) is not None]
        placeholders = ["?" for _ in fields_to_save]
        values = [self._attributes[f] for f in fields_to_save]
        
        sql = f"INSERT INTO {self.TABLE_NAME} ({', '.join(fields_to_save)}) VALUES ({', '.join(placeholders)})"
        
        try:
            cursor.execute(sql, values)
            conn.commit()
            if cursor.lastrowid:
                self._attributes[self.FIELDS_PK[0]] = cursor.lastrowid
            return True
        except Exception as e:
            print(f"Erro no INSERT: {e}")
            return False

    def _update(self):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        pk_field = self.FIELDS_PK[0]
        pk_val = self._attributes.get(pk_field)
        
        fields_to_update = [f for f in self.FIELDS if f != pk_field and self._attributes.get(f) is not None]
        set_clause = [f"{f} = ?" for f in fields_to_update]
        values = [self._attributes[f] for f in fields_to_update]
        values.append(pk_val)
        
        sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clause)} WHERE {pk_field} = ?"
        
        try:
            cursor.execute(sql, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro no UPDATE: {e}")
            return False

    def _record_exists(self, pk_val):
        conn = Database.get_connection()
        cursor = conn.cursor()
        pk_field = self.FIELDS_PK[0]
        sql = f"SELECT 1 FROM {self.TABLE_NAME} WHERE {pk_field} = ?"
        cursor.execute(sql, (pk_val,))
        return cursor.fetchone() is not None

    # --- MÉTODOS DE LEITURA (Static/Class Methods) ---

    @classmethod
    def read_all(cls, fields: Optional[List[str]] = None, where: str = None, params: tuple = ()) -> List[dict]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        target_fields = fields if fields else cls.FIELDS
        cols_str = ", ".join(target_fields)
        
        sql = f"SELECT {cols_str} FROM {cls.TABLE_NAME}"
        if where:
            sql += f" WHERE {where}"
            
        cursor.execute(sql, params)
        return cursor.fetchall()

    @classmethod
    def read_join(cls, where: str = None, params: tuple = ()) -> List[dict]:
        """
        Realiza SELECT com LEFT JOIN baseado em FIELDS_FK.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        # 1. Campos da tabela principal
        select_parts = [f"{cls.TABLE_NAME}.{f}" for f in cls.FIELDS]
        join_clauses = []
        
        # 2. Processa FKs
        if hasattr(cls, 'FIELDS_FK'):
            for key, fk_data in cls.FIELDS_FK.items():
                if key == "Fields": continue 
                
                ref_table = fk_data['References']
                local_key = fk_data['FieldsKey'][0] # Ex: DevCod
                remote_key = fk_data['Fields'][0]   # Ex: DevCod (na T_Dev)
                
                # Monta JOIN
                join_clauses.append(
                    f"LEFT JOIN {ref_table} ON {cls.TABLE_NAME}.{local_key} = {ref_table}.{remote_key}"
                )
                
                # Adiciona campos da tabela referenciada (Simples: Select *)
                # Em refatoração futura, podemos pegar os campos do MD da tabela referenciada
                select_parts.append(f"{ref_table}.*")

        cols_sql = ", ".join(select_parts)
        joins_sql = " ".join(join_clauses)
        
        sql = f"SELECT {cols_sql} FROM {cls.TABLE_NAME} {joins_sql}"
        
        if where:
            sql += f" WHERE {where}"
            
        cursor.execute(sql, params)
        # Remove duplicatas de chaves no dicionário se houver colunas com mesmo nome
        # (O driver SQLite sobrescreve chaves iguais, o que é aceitável aqui)
        return cursor.fetchall()

    # def read_by_id(self, id_value, pk_column='id'):
    #     """
    #     Busca um registro específico pela chave primária.
    #     """
    #     try:
    #         # Se você usa SQLAlchemy puro:
    #         # return self.session.query(self.__class__).filter(getattr(self.__class__, pk_column) == id_value).first()
            
    #         # Se você usa uma estrutura de dicionário/JSON (comum em protótipos):
    #         # registros = self.read_all()
    #         # return next((item for item in registros if item.get(pk_column) == id_value), None)

    #         # Sugestão genérica baseada no seu erro anterior (usando a instância):
    #         query = f"SELECT * FROM {self.__class__.__name__} WHERE {pk_column} = ?"
    #         # Aqui entraria sua lógica de execução de SQL (self.execute, etc)
            
    #         # Para resolver seu erro imediato e manter a compatibilidade com o que a UI espera:
    #         dados = self.find_one(id_value) # Ou o nome do seu método de busca
    #         if dados:
    #             for key, value in dados.items():
    #                 setattr(self, key, value)
    #             return True
    #         return False
    #     except Exception as e:
    #         print(f"Erro ao ler por ID: {e}")
    #         return False
    
    # def load(self, id_value):
    #     # Lógica para buscar no banco (exemplo genérico)
    #     res = self.session.query(self.__class__).get(id_value)
    #     if res:
    #         self.__dict__.update(res.__dict__)
    #         return True
    #     return False
    
    def read_by_field(self, field_name, value):
        """
        Busca um registro onde field_name == value usando a estrutura existente.
        """
        # Usamos o 'where' e 'params' que sua read_all já aceita
        where_clause = f"{field_name} = ?"
        registros = self.read_all(where=where_clause, params=(value,)) 
        
        if registros:
            dados = registros[0]
            for key, val in dados.items():
                setattr(self, key, val)
            return True
        return False