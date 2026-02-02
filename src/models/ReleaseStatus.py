from enum import StrEnum

class ReleaseStatus(StrEnum):
    ABERTO = "Aberto"       # Em planejamento / Desenvolvimento
    FECHADO = "Fechado"     # Publicado / Lançado oficialmente
    CANCELADO = "Cancelado" # Versão abortada

    @classmethod
    def list(cls):
        """Retorna lista para selectbox"""
        return list(map(str, cls))