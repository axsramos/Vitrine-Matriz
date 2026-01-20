from src.core.crud_mixin import CrudMixin
from src.models.UsrPrfMD import UsrPrfMD

class UserProfileModel(CrudMixin, UsrPrfMD):
    def __init__(self):
        # Inicializa o Mixin, que vai ler os FIELDS do UsrPrfMD
        # e criar os atributos dinamicamente (self._attributes)
        super().__init__()
        
    def load_by_user(self, user_id):
        """
        Carrega o perfil utilizando a chave estrangeira PrfUsrCod.
        """
        return self.read_by_field('PrfUsrCod', user_id)

    # Se precisar de regras de negócio específicas (ex: validação de URL), adicione aqui.