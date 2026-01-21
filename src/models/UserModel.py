from src.core.crud_mixin import CrudMixin
from src.models.md.UsrMD import UsrMD

class UserModel(CrudMixin, UsrMD):
    def __init__(self, **kwargs):
        super().__init__()
        # Inicializa campos com None
        for field in self.FIELDS:
            setattr(self, field, None)
            
        if kwargs:
            for k, v in kwargs.items():
                if hasattr(self, k):
                    setattr(self, k, v)