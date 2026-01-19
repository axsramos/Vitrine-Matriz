from src.core.crud_mixin import CrudMixin
from src.models.RelMD import RelMD

class ReleaseModel(CrudMixin, RelMD):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)