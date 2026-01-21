from src.core.crud_mixin import CrudMixin
from src.models.UsrPrfMD import UsrPrfMD

class UserProfileModel(CrudMixin, UsrPrfMD):
    def __init__(self):
        super().__init__()
        
    def load_by_user(self, user_id):
        """
        Carrega o perfil buscando pelo campo de vínculo CORRETO: UsrPrfUsrCod.
        """
        # AQUI ESTAVA O ERRO: 'UsrCod' -> 'UsrPrfUsrCod'
        return self.read_by_field('UsrPrfUsrCod', user_id)

    def prepare_for_save(self, user_id):
        """
        Garante que o vínculo com o usuário esteja preenchido antes de salvar.
        """
        # AQUI TAMBÉM: self.UsrCod -> self.UsrPrfUsrCod
        self.UsrPrfUsrCod = user_id