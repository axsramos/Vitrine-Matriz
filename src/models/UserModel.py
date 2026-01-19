from src.core.crud_mixin import CrudMixin
from src.models.UsrMD import UsrMD

class UserModel(CrudMixin, UsrMD):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)