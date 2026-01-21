from src.core.database import get_connection
from src.models.AudMD import AudMD

class RelMD:
    TABLE_NAME = "T_Rel"
    FIELDS_PK = ["RelCod"]
    FIELDS_FK = []
    TABLE_IDX = {
        "IXRel01": ["RelAudIns"],
        "IXRel02": ["RelDtaPub"],
    }
    FIELDS_REQUIRED = ["RelVrs"]
    FIELDS_AUDIT = [
        "RelAudIns",
        "RelAudUpd",
        "RelAudDlt",
        "RelAudUsr",
    ]
    FIELDS = FIELDS_PK + FIELDS_REQUIRED
    FIELDS += [
        "RelTtlCmm",
        "RelDtaPub",
    ]
    FIELDS += FIELDS_AUDIT.copy()
    FIELDS_MD = {
        "RelCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "Default": '',
            "LongLabel": 'Código do Relatório',
            "ShortLabel": 'Código',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "RelVrs": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Versão',
            "ShortLabel": 'Versão',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "RelTtlCmm": {
            "Type": 'VARCHAR',
            "Length": '4000',
            "Required": False,
            "Default": '',
            "LongLabel": 'Título do Commit',
            "ShortLabel": 'Título',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "RelDtaPub": {
            "Type": 'DATETIME',
            "Length": '25',
            "Required": False,
            "Default": '',
            "LongLabel": 'Publicação',
            "ShortLabel": 'Publicação',
            "TextPlaceholder": '',
            "TextHelp": '',
        },
        "RelAudIns": AudMD.FIELDS_MD["AudIns"],
        "RelAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "RelAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "RelAudUsr": AudMD.FIELDS_MD["AudUsr"],
    }
    
    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
            return get_connection()