from src.core.database import get_connection
from src.models.AudMD import AudMD

class UsrPrfMD:
    TABLE_NAME = "T_UsrPrf"
    
    FIELDS_PK = ["UsrPrfCod"]
    FIELDS_FK = {
        "Fields": ["UsrPrfUsrCod"],
        "FKUsrPrf01": { "FieldsKey": ["UsrPrfUsrCod"], "References": "T_USR", "Fields":["UsrCod"]}
    }
    TABLE_IDX = {
        "IDXUsrPrf01": ["UsrPrfAudIns"],
        "IDXUsrPrf02": ["UsrPrfCgo"]
    }
    FIELDS_REQUIRED = []
    FIELDS_AUDIT = [
        "UsrPrfAudIns",
        "UsrPrfAudUpd",
        "UsrPrfAudDlt",
        "UsrPrfAudUsr",
    ]
    FIELDS = FIELDS_PK + FIELDS_FK["Fields"]
    FIELDS += [
        "UsrPrfCgo",
        "UsrPrfBio",
        "UsrPrfUrl",
        "UsrPrfFto",
    ]
    FIELDS += FIELDS_AUDIT.copy()
    FIELDS_MD = {
        "UsrPrfCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Perfil do Usuário',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPrfUsrCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Usuário',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPrfCgo": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "Default": '',
            "LongLabel": 'Cargo do Usuário',
            "ShortLabel": 'Cargo',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPrfBio": {
            "Type": 'TEXT',
            "Length": '4000',
            "Required": False,
            "Default": '',
            "LongLabel": 'Biografia do Usuário',
            "ShortLabel": 'Biografia',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPrfUrl": {
            "Type": 'VARCHAR',
            "Length": '999',
            "Required": False,
            "Default": '',
            "LongLabel": 'URL do Portfólio do Usuário',
            "ShortLabel": 'URL',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPrfFto": {
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