class AudMD:
    FIELDS = [
        "AudIns",  # Insertion Date
        "AudUpd",  # Update Date
        "AudDlt",  # Deletion Date
        "AudUsr"   # User ID responsible for the action
    ]
    FIELDS_MD = {
        "AudIns": {
            "Type": 'DATETIME',
            "Length": '25',
            "Required": True,
            "Default": '',
            "LongLabel": 'Auditoria - Data de Inserção',
            "ShortLabel": 'Inserção',
            "TextPlaceholder": 'Data de criação do registro',
            "TextHelp": '',
        },
        "AudUpd": {
            "Type": 'DATETIME',
            "Length": '25',
            "Required": False,
            "Default": '',
            "LongLabel": 'Auditoria - Data de Atualização',
            "ShortLabel": 'Atualização',
            "TextPlaceholder": 'Data da última atualização do registro',
            "TextHelp": '',
        },
        "AudDlt": {
            "Type": 'DATETIME',
            "Length": '25',
            "Required": False,
            "Default": '',
            "LongLabel": 'Auditoria - Data de Exclusão',
            "ShortLabel": 'Exclusão',
            "TextPlaceholder": 'Data da exclusão do registro',
            "TextHelp": '',
        },
        "AudUsr": {
            "Type": 'VARCHAR',
            "Length": '255',
            "Required": True,
            "Default": '',
            "LongLabel": 'Auditoria - Usuário Responsável',
            "ShortLabel": 'Usuário',
            "TextPlaceholder": 'Usuário que realizou a ação',
            "TextHelp": '',
        }
    }