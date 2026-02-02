from enum import StrEnum

# Definição das roles (permissões) disponíveis no sistema
class UserRole(StrEnum):
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"
    DEVELOPMENT = "development"

    @classmethod
    def list(cls):
        """Retorna uma lista simples com os valores para usar no selectbox"""
        return list(map(str, cls))
