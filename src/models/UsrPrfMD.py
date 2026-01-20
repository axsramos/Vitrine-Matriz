from src.core.database import get_connection
from src.models.AudMD import AudMD

class UsrPrfMD:
    TABLE_NAME = 'T_Usr_Prf'
    
    FIELDS_PK = ['PrfCod']
    FIELDS_FK = []
    TABLE_IDX = {
        "IDXUsrPrf01": ["DevAudIns"],
        "IDXUsrPrf02": ["PrfCgo"]
    }
    FIELDS_REQUIRED = []
    FIELDS_AUDIT = [
        "UsrPrfAudIns",
        "UsrPrfAudUpd",
        "UsrPrfAudDlt",
        "UsrPrfAudUsr",
    ]
    FIELDS = [
        "PrfCod",     # PK
        "PrfUsrCod",  # FK para T_Usr
        "PrfCgo",     # Cargo
        "PrfBio",     # Biografia
        "PrfUrl",     # URL (LinkedIn/Portfólio)
        "PrfFto",     # Caminho da Foto (Nova localização)
    ]
    FIELDS += FIELDS_AUDIT.copy()
    FIELDS_MD = {
        "PrfCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Perfil',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "PrfUsrCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Usuário',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "PrfCgo": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "Default": '',
            "LongLabel": 'Cargo do Usuário',
            "ShortLabel": 'Cargo',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "PrfBio": {
            "Type": 'TEXT',
            "Length": '4000',
            "Required": False,
            "Default": '',
            "LongLabel": 'Biografia do Usuário',
            "ShortLabel": 'Biografia',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "PrfUrl": {
            "Type": 'VARCHAR',
            "Length": '999',
            "Required": False,
            "Default": '',
            "LongLabel": 'URL do Portfólio do Usuário',
            "ShortLabel": 'URL',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "PrfFto": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "Default": '',
            "LongLabel": 'Foto do Usuário',
            "ShortLabel": 'Foto',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPrfAudIns": AudMD.FIELDS_MD["AudIns"],
        "UsrPrfAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "UsrPrfAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "UsrPrfAudUsr": AudMD.FIELDS_MD["AudUsr"],
    }
    
    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
            return get_connection()