from src.models.AudMD import AudMD

class TskMD:
    TABLE_NAME = "T_TSK"
    FIELDS_PK = ["TskCod"]
    
    FIELDS_FK = {
        "Fields": ["DevCod", "RelCod"],
        "FKTsk01": { "FieldsKey": ["DevCod"], "References": "T_DEV", "Fields":["DevCod"]},
        "FKTsk02": { "FieldsKey": ["RelCod"], "References": "T_REL", "Fields":["RelCod"]},
    }
    
    TABLE_IDX = {
        "IXTsk01": ["TskAudIns"],
        "IXTsk02": ["TskTtl"],
        "IXTsk03": ["TskImp"],
    }
    
    FIELDS_REQUIRED = ["TskExtCod", "TskTtl"]
    
    FIELDS_AUDIT = [
        "TskAudIns",
        "TskAudUpd",
        "TskAudDlt",
        "TskAudUsr",
    ]
    
    FIELDS = FIELDS_PK + FIELDS_REQUIRED + ["TskDsc", "TskImp", "DevCod", "RelCod"] + FIELDS_AUDIT
    
    FIELDS_MD = {
        "TskCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "LongLabel": 'Código',
            "Default": None
        },
        "TskExtCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "LongLabel": 'Código Externo (Bitrix)',
            "Default": None
        },
        "TskTtl": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "LongLabel": 'Título da Tarefa',
            "Default": ''
        },
        "TskDsc": {
            "Type": 'VARCHAR',
            "Length": '4000',
            "Required": False,
            "LongLabel": 'Descrição Técnica',
            "Default": ''
        },
        "TskImp": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": False,
            "LongLabel": 'Impacto no Negócio',
            "Default": 'Baixo'
        },
        "DevCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": False,
            "LongLabel": 'Desenvolvedor Responsável',
            "Default": None
        },
        "RelCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": False,
            "LongLabel": 'Versão / Release',
            "Default": None
        },
        "TskAudIns": AudMD.FIELDS_MD["AudIns"],
        "TskAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "TskAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "TskAudUsr": AudMD.FIELDS_MD["AudUsr"],
    }