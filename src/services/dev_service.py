import pandas as pd
from src.models import DevModel

class DevService:
    def get_all_developers(self):
        data = DevModel.read_all()
        
        df = pd.DataFrame(data)
        if df.empty:
            return pd.DataFrame(columns=DevModel.FIELDS)
        return df
    
    def get_dev_by_user_id(self, user_id):
        model = DevModel()
        # Busca pelo novo campo de ligação que criamos
        if model.read_by_field('DevUsrCod', user_id):
            return model
        return None

    def get_dev_by_login(self, login: str):
        """Busca um desenvolvedor pelo login (DevLgnExt)"""
        # Assumindo que você tem um campo para vincular ao login do usuário.
        # Se não tiver 'DevLgnExt' no seu DevMD, usaremos o 'DevNme' ou criaremos o campo.
        # Para v0.4.0, vamos assumir que o DevNme deve ser único ou usaremos o filtro simples.
        
        # Vamos tentar filtrar onde o nome ou login bate
        # Nota: O ideal é ter DevLgnExt na T_DEV. Se não tiver, usaremos o Nome para vincular.
        devs = DevModel.read_all()
        for dev in devs:
            # Verifica se existe algum campo de login ou se o nome bate
            if dev.get('DevPgeUrl') == login: # Improviso: Usando PgeUrl para guardar login se não houver campo específico
                return DevModel(**dev)
            # Ou verificação por nome exato
            if dev.get('DevNme') == login:
                return DevModel(**dev)
        return None
    
    def save_developer(self, dev_data: dict):
        try:
            # Padrão: Data Transfer Object (via dict) -> Entity (Model)
            dev = DevModel(**dev_data)
            
            if dev.save():
                return True, "Desenvolvedor salvo com sucesso!"
            return False, "Erro ao salvar dados."
            
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"
    
    def create_dev_from_user(self, user_name: str, user_login: str):
        """
        Cria um perfil de desenvolvedor baseado nos dados do usuário (T_USR).
        """
        try:
            # 1. Verifica duplicidade (Regra de Negócio)
            # Aqui verificamos se já existe um Dev com esse Nome
            existing = DevModel.read_all(where="DevNme = ?", params=(user_name,))
            if existing:
                return False, f"Já existe um desenvolvedor com o nome '{user_name}'."

            # 2. Cria o objeto Model
            new_dev = DevModel()
            new_dev.DevNme = user_name
            new_dev.DevCgo = "Full Stack" # Cargo Padrão
            new_dev.DevBio = f"Perfil gerado automaticamente a partir do usuário {user_login}."
            new_dev.DevPgeUrl = ""   # Pode ser link do GitHub
            new_dev.DevFto = ""      # Pode ser URL da foto
            
            # DICA: Se quiser vincular estritamente, idealmente T_DEV teria uma coluna DevUsrLgn
            # Como não temos certeza se alterou T_DEV para ter Login, salvamos o básico.
            
            if new_dev.save():
                return True, f"Perfil de desenvolvedor criado para: {user_name}"
            return False, "Erro ao salvar no banco de dados."
            
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"