from src.core.database import get_connection
from src.models.AudMD import AudMD

class UsrMD:
    TABLE_NAME = "T_USR"
    FIELDS_PK = ["UsrCod"]
    FIELDS_FK = []
    TABLE_IDX = {
        "IDX_Usr01": ["UsrAudIns"],
        "IDX_Usr02": ["UsrNme"],
        "IDX_Usr03": ["UsrRle", "UsrNme"]
    }
    FIELDS_REQUIRED = ["UsrNme","UsrLgn","UsrPwdHash","UsrRle"]
    FIELDS_AUDIT = [
        "UsrAudIns",
        "UsrAudUpd",
        "UsrAudDlt",
        "UsrAudUsr",
    ]
    FIELDS = FIELDS_PK + FIELDS_REQUIRED + FIELDS_AUDIT
    FIELDS_MD = {
        "UsrCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Usuário',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrNme": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Nome do Usuário',
            "ShortLabel": 'Nome',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrLgn": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Login do Usuário',
            "ShortLabel": 'Login',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrPwdHash": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Hash da Senha do Usuário',
            "ShortLabel": 'Hash',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrRle": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Perfil do Usuário',
            "ShortLabel": 'Perfil',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "UsrAudIns": AudMD.FIELDS_MD["AudIns"],
        "UsrAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "UsrAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "UsrAudUsr": AudMD.FIELDS_MD["AudUsr"],
    }
    
    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
            return get_connection()