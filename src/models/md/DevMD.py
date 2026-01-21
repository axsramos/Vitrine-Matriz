from src.models.md.AudMD import AudMD

class DevMD:
    TABLE_NAME = "T_Dev"
    
    FIELDS_PK = ["DevCod"]
    
    FIELDS_FK = {
        "Fields": ["DevUsrCod"],
        "Details": { "DevUsrCod": {"Table": "T_Usr", "Field": "UsrCod"} }
    }

    FIELDS_AUDIT = [
        "DevAudIns", "DevAudUpd", "DevAudDlt", "DevAudUsr"
    ]

    FIELDS = [
        "DevCod", "DevNom", "DevUsrCod",
        "DevAudIns", "DevAudUpd", "DevAudDlt", "DevAudUsr"
    ]
    
    FIELDS_MD = {
        "DevCod": {"Type": "INTEGER", "Label": "ID Dev"},
        "DevNom": {"Type": "VARCHAR", "Label": "Nome", "Required": True},
        "DevUsrCod": {"Type": "INTEGER", "Label": "ID Usuário"},
        
        # Auditoria
        "DevAudIns": AudMD.FIELDS_MD["AudIns"],
        "DevAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "DevAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "DevAudUsr": AudMD.FIELDS_MD["AudUsr"]
    }