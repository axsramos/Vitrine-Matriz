import sqlite3
import os
from src.core.config import Config

class Database:
    _connection = None

    @staticmethod
    def get_connection():
        """
        Retorna uma conexão Singleton com o banco de dados.
        """
        if Database._connection is None:
            if Config.DB_DRIVER == "sqlite":
                # check_same_thread=False é crucial para o Streamlit
                Database._connection = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
                # Define a factory para retornar dicionários
                Database._connection.row_factory = Database.dict_factory
        
        return Database._connection

    @staticmethod
    def dict_factory(cursor, row):
        """
        Converte as linhas do banco (tuplas) em dicionários Python reais.
        Permite acesso via row['NomeColuna'].
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def close_connection():
        if Database._connection:
            Database._connection.close()
            Database._connection = None

# Função auxiliar para manter compatibilidade com códigos antigos se necessário
def get_connection():
    return Database.get_connection()