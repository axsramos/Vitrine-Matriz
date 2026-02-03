from enum import StrEnum

# Definição dos tipos de tarefa disponíveis no sistema
class TaskTip(StrEnum):
    FEATURE = "Feature"
    BUGFIX = "Bugfix"
    REFACTOR = "Refactor"
    DOCUMENTATION = "Documentation"
    SUPPORT = "Support"
    

    @classmethod
    def list(cls):
        """Retorna uma lista simples com os valores para usar no selectbox"""
        return list(map(str, cls))
