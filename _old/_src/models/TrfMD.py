from src.core.database import get_connection
from src.models.AudMD import AudMD

class TrfMD:
    TABLE_NAME = 'T_Trf'
    
    FIELDS_PK = ['TrfCod']
    
    # FKs definidas aqui entram automaticamente na lista FIELDS
    FIELDS_FK = {
        "Fields": ["TrfDevCod", "TrfRelCod"],
        "FKTrf01": { "FieldsKey": ["TrfDevCod"], "References": "T_Dev", "Fields":["DevCod"]},
        "FKTrf02": { "FieldsKey": ["TrfRelCod"], "References": "T_Rel", "Fields":["RelCod"]},
    }
    
    TABLE_IDX = {
        "IDXTrf01": ["TrfAudIns"],
        "IDXTrf02": ["TrfTtl"],
        "IDXTrf03": ["TrfStt"],
    }
    
    FIELDS_REQUIRED = ["TrfTtl"]
    
    FIELDS_AUDIT = [
        "TrfAudIns",
        "TrfAudUpd",
        "TrfAudDlt",
        "TrfAudUsr",
    ]

    # Construção da Lista de Campos (Sem duplicidade)
    # PK + FKs + Obrigatórios
    FIELDS  = FIELDS_PK + FIELDS_FK["Fields"] + FIELDS_REQUIRED
    
    # Adiciona os demais campos que NÃO estão nas listas acima
    FIELDS += [
        'TrfDesc',    # Descrição
        'TrfPrio',    # Prioridade
        'TrfImp',     # Impacto
        'TrfStt',     # Status
        'TrfDatEnt',  # Data Entrega
    ]
    
    FIELDS += FIELDS_AUDIT.copy()

    FIELDS_MD = {
         "TrfCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": True,
            "LongLabel": 'Código da Tarefa',
            "ShortLabel": 'Código',
        },
        "TrfDevCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": False,
            "LongLabel": 'Desenvolvedor Responsável',
            "ShortLabel": 'Desenvolvedor',
        },
        "TrfRelCod": {
            "Type": 'INTEGER',
            "Length": '8',
            "Required": False,
            "LongLabel": 'Release/Versão',
            "ShortLabel": 'Release',
        },
        "TrfTtl": {
            "Type": 'VARCHAR',
            "Length": '150', # Ajustado conforme SQL
            "Required": True,
            "LongLabel": 'Título da Tarefa',
            "ShortLabel": 'Título',
        },
        "TrfDesc": {
            "Type": 'VARCHAR',
            "Length": '4000',
            "Required": False,
            "LongLabel": 'Descrição Detalhada',
            "ShortLabel": 'Descrição',
        },
        "TrfPrio": {
            "Type": 'VARCHAR',
            "Length": '20',
            "Required": False,
            "LongLabel": 'Prioridade',
            "ShortLabel": 'Prioridade',
        },
        "TrfImp": {
            "Type": 'VARCHAR', 
            "Length": '20', 
            "Required": False,
            "Default": 'Médio',
            "LongLabel": 'Impacto do Negócio', 
            "ShortLabel": 'Impacto',
        },
        "TrfStt": {
            "Type": 'VARCHAR',
            "Length": '50',
            "Required": False,
            "LongLabel": 'Status',
            "ShortLabel": 'Status',
        },
        "TrfDatEnt": {
            "Type": 'DATE',
            "Length": '10',
            "Required": False,
            "LongLabel": 'Data de Entrega',
            "ShortLabel": 'Entrega',
        },
        "TrfAudIns": AudMD.FIELDS_MD["AudIns"],
        "TrfAudUpd": AudMD.FIELDS_MD["AudUpd"],
        "TrfAudDlt": AudMD.FIELDS_MD["AudDlt"],
        "TrfAudUsr": AudMD.FIELDS_MD["AudUsr"],
    }

    def __init__(self, data=None):
        self.att = data or {}

    def get_db_connection(self):
        return get_connection()