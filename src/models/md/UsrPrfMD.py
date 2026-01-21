from src.models.md.AudMD import AudMD

class UsrPrfMD:
    TABLE_NAME = "T_UsrPrf"
    
    FIELDS_PK = ["UsrPrfCod"]
    
    FIELDS_AUDIT = [
        "UsrPrfAudIns",
        "UsrPrfAudUpd",
        "UsrPrfAudDlt",
        "UsrPrfAudUsr",
    ]
    
    FIELDS_FK = {
        "Fields": ["UsrPrfUsrCod"],
        "Details": { "UsrPrfUsrCod": {"Table": "T_Usr", "Field": "UsrCod"} }
    }
    
    FIELDS = [
        "UsrPrfCod", "UsrPrfBio", "UsrPrfFto", "UsrPrfUrl", "UsrPrfCgo",
        "UsrPrfUsrCod",
        "UsrPrfAudIns", "UsrPrfAudUpd", "UsrPrfAudDlt", "UsrPrfAudUsr"
    ]
    
    FIELDS_MD = {
        "UsrPrfBio": {"Type": "TEXTAREA", "Label": "Biografia"},
        "UsrPrfFto": {"Type": "IMAGE", "Label": "Foto"},
        "UsrPrfUrl": {"Type": "URL", "Label": "LinkedIn/Portfólio"},
        "UsrPrfCgo": {"Type": "VARCHAR", "Label": "Cargo"},
        "UsrPrfUsrCod": {"Type": "INTEGER", "Label": "Usuário"},
        "UsrPrfAudIns": AudMD.FIELDS_MD["AudIns"],
        "UsrPrfAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "UsrPrfAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "UsrPrfAudUsr": AudMD.FIELDS_MD["AudUsr"]
    }