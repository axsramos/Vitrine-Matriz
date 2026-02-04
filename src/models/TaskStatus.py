from enum import StrEnum

class TaskStatus(StrEnum):
    ABERTO = "Aberto"       # Aberto / Em desenvolvimento
    CONCLUIDO = "Concluído" # Concluído / Finalizado
    CANCELADO = "Cancelado" # Cancelado / Abortado

    @classmethod
    def list(cls):
        """Retorna lista para selectbox"""
        return list(map(str, cls))