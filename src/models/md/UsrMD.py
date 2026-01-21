from src.models.md.AudMD import AudMD

class UsrMD:
    TABLE_NAME = "T_Usr"
    
    FIELDS_PK = ["UsrCod"]

    FIELDS_FK = {}

    FIELDS_AUDIT = [
        "UsrAudIns",
        "UsrAudUpd",
        "UsrAudDlt",
        "UsrAudUsr",
    ]

    FIELDS = [
        "UsrCod", "UsrNom", "UsrLgn", "UsrPwd", "UsrPrm",
        "UsrAudIns", "UsrAudUpd", "UsrAudUsr"
    ]
    
    FIELDS_MD = {
        "UsrCod": {"Type": "INTEGER", "Label": "ID"},
        "UsrNom": {"Type": "VARCHAR", "Label": "Nome Completo", "Required": True},
        "UsrLgn": {"Type": "VARCHAR", "Label": "Login", "Required": True},
        "UsrPwd": {"Type": "PASSWORD", "Label": "Senha", "Required": True},
        "UsrPrm": {"Type": "VARCHAR", "Label": "Permissão"},
        "UsrAudIns": AudMD.FIELDS_MD["AudIns"],
        "UsrAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "UsrAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "UsrAudUsr": AudMD.FIELDS_MD["AudUsr"]
    }