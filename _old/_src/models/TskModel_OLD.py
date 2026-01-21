from src.models.DevModel import DevModel
import pandas as pd

class DevService:
    def get_all_developers(self):
        """
        Retorna DataFrame com todos os desenvolvedores.
        """
        # Usa o método read_all do Mixin
        data = DevModel.read_all()
        
        # Converte lista de dicts para DataFrame
        df = pd.DataFrame(data)
        
        if df.empty:
            return pd.DataFrame(columns=DevModel.FIELDS)
            
        return df

    def get_dev_by_login(self, login_bitrix):
        """Busca desenvolvedor pelo login externo (Bitrix)"""
        results = DevModel.read_all(
            where="DevLgnExt = ?", 
            params=(login_bitrix,)
        )
        return results[0] if results else None

    def save_developer(self, dev_data: dict):
        """
        Salva ou Atualiza um desenvolvedor.
        Recebe um dict com chaves iguais ao banco (DevNme, DevCgo...)
        """
        dev = DevModel(**dev_data) # Popula o Model
        return dev.save() # O Mixin decide Insert ou Update