from src.core.crud_mixin import CrudMixin
from src.models.DevMD import DevMD

class DevModel(CrudMixin, DevMD):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def presentation(self):
        """Helper para exibição em combos/selects"""
        return f"{self.DevNme} - {self.DevCgo}"
    
    def load(self, id):
        """
        Carrega os dados do desenvolvedor pelo ID (DevCod).
        """
        # Em vez de read_by_id, usamos o método genérico do Mixin
        return self.read_by_field('DevCod', id)

    # def load(self, id):
    #     """
    #     Carrega os dados do desenvolvedor pelo ID.
    #     Retorna True se encontrar, False caso contrário.
    #     """
    #     # Se o seu CRUDMixin usa 'read' ou 'get_by_id', chame-o aqui:
    #     dados = self.read_by_id(id)
        
    #     if dados:
    #         # Opcional: Popula os atributos do objeto com os dados retornados
    #         for key, value in dados.items():
    #             setattr(self, key, value)
    #         return True
    #     return False