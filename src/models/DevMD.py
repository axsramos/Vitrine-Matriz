from src.core.database import get_connection
from src.models.AudMD import AudMD

class DevMD:
    TABLE_NAME = "T_Dev"
    FIELDS_PK = ["DevCod"]
    FIELDS_FK = []
    TABLE_IDX = {
        "IXDev01": ["DevAudIns"],
        "IXDev02": ["DevNme"],
        "IXDev03": ["DevCgo", "DevNme"]
    }
    FIELDS_REQUIRED = ["DevNme"]
    FIELDS_AUDIT = [
        "DevAudIns",
        "DevAudUpd",
        "DevAudDlt",
        "DevAudUsr",
    ]
    FIELDS = FIELDS_PK + FIELDS_REQUIRED
    FIELDS += [
        "DevLgnExt",
        "DevCgo",
        "DevBio",
        "DevPgeUrl",
        "DevFto",
        "DevUsrCod",
    ]
    FIELDS += FIELDS_AUDIT.copy()
    FIELDS_MD = {
        "DevCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Desenvolvedor',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevNme": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Nome do Desenvolvedor',
            "ShortLabel": 'Nome',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevLgnExt": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "Default": '',
            "LongLabel": 'Login do Desenvolvedor',
            "ShortLabel": 'Login',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevCgo": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "Default": '',
            "LongLabel": 'Cargo Desenvolvedor',
            "ShortLabel": 'Cargo',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevBio": {
            "Type": 'VARCHAR',
            "Length": '4000',
            "Required": False,
            "Default": '',
            "LongLabel": 'Biografia do Desenvolvedor',
            "ShortLabel": 'Bio',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevPgeUrl": {
            "Type": 'VARCHAR',
            "Length": '999',
            "Required": False,
            "Default": '',
            "LongLabel": 'Portfólio do Desenvolvedor',
            "ShortLabel": 'Portfólio',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevFto": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "Default": '',
            "LongLabel": 'Foto do Desenvolvedor',
            "ShortLabel": 'Foto',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevUsrCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": False,
            "Default": '',
            "LongLabel": 'Código do Usuário',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "DevAudIns": AudMD.FIELDS_MD["AudIns"],
        "DevAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "DevAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "DevAudUsr": AudMD.FIELDS_MD["AudUsr"],
    }
    
    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
            return get_connection()