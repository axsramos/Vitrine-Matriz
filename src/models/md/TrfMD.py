from src.models.md.AudMD import AudMD

class TrfMD:
    TABLE_NAME = "T_Trf"
    FIELDS_PK = ["TrfCod"]
    
    FIELDS_FK = {
        "Fields": ["TrfDevCod", "TrfRelCod"],
        "FKTrf01": { "FieldsKey": ["TrfDevCod"], "References": "T_Dev", "Fields":["DevCod"]},
        "FKTrf02": { "FieldsKey": ["TrfRelCod"], "References": "T_Rel", "Fields":["RelCod"]},
    }

    FIELDS_AUDIT = ["TrfAudIns", "TrfAudUpd", "TrfAudDlt", "TrfAudUsr"]

    FIELDS = [
        "TrfCod", "TrfTit", "TrfDsc", "TrfTip", "TrfPri", "TrfImp", "TrfSit", "TrfDatEnt",
        "TrfDevCod", "TrfRelCod",
        "TrfAudIns", "TrfAudUpd", "TrfAudDlt", "TrfAudUsr"
    ]
    
    FIELDS_MD = {
        "TrfCod": {"Type": "INTEGER", "Label": "Código"},
        "TrfTit": {"Type": "VARCHAR", "Label": "Título", "Required": True},
        "TrfDsc": {"Type": "TEXTAREA", "Label": "Descrição"},
        "TrfTip": {"Type": "VARCHAR", "Label": "Tipo de Tarefa"},
        "TrfPri": {"Type": "VARCHAR", "Label": "Prioridade"},
        "TrfImp": {"Type": "VARCHAR", "Label": "Impacto"},
        "TrfSit": {"Type": "VARCHAR", "Label": "Status"},
        "TrfDatEnt": {"Type": "DATE", "Label": "Entrega"},
        
        "TrfDevCod": {"Type": "INTEGER", "Label": "Desenvolvedor"},
        "TrfRelCod": {"Type": "INTEGER", "Label": "Release"},
        
        "TrfAudIns": AudMD.FIELDS_MD["AudIns"],
        "TrfAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "TrfAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "TrfAudUsr": AudMD.FIELDS_MD["AudUsr"]
    }