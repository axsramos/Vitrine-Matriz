from src.models.md.AudMD import AudMD

class RelMD:
    TABLE_NAME = "T_Rel"
    FIELDS_PK = ["RelCod"]
    FIELDS_FK = {}
    
    FIELDS_AUDIT = ["RelAudIns", "RelAudUpd", "RelAudDlt", "RelAudUsr"]

    FIELDS = [
        "RelCod", "RelVrs", "RelTtlCmm", "RelDat",
        "RelAudIns", "RelAudUpd", "RelAudDlt", "RelAudUsr"
    ]
    
    FIELDS_MD = {
        "RelCod": {"Type": "INTEGER", "Label": "ID"},
        "RelVrs": {"Type": "VARCHAR", "Label": "Versão", "Required": True},
        "RelTtlCmm": {"Type": "VARCHAR", "Label": "Título/Comentário"},
        "RelDat": {"Type": "DATE", "Label": "Data Publicação"},
        
        "RelAudIns": AudMD.FIELDS_MD["AudIns"],
        "RelAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "RelAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "RelAudUsr": AudMD.FIELDS_MD["AudUsr"]
    }