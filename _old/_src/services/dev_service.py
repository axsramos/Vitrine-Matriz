import pandas as pd
from src.models.DevModel import DevModel
from src.models.UserProfileModel import UserProfileModel

class DevService:
    def get_all_devs_dataframe(self):
        """
        Retorna um DataFrame consolidado (Join T_Dev + T_UsrPrf).
        Utilizado nas telas de Portfólio, Detalhes e Tarefas.
        """
        dev_model = DevModel()
        profile_model = UserProfileModel()
        
        devs_data = dev_model.read_all()
        profiles_data = profile_model.read_all()

        if not devs_data:
            return pd.DataFrame(columns=['DevNme', 'UsrPrfCgo', 'UsrPrfBio', 'UsrPrfFto', 'UsrPrfUrl'])

        df_devs = pd.DataFrame(devs_data)
        df_profiles = pd.DataFrame(profiles_data)

        if not df_devs.empty:
            df_devs['DevUsrCod'] = pd.to_numeric(df_devs['DevUsrCod'], errors='coerce')
            df_devs['DevUsrCod'] = df_devs['DevUsrCod'].fillna(0).astype(int)
            
        if not df_profiles.empty:
            df_profiles['UsrPrfUsrCod'] = pd.to_numeric(df_profiles['UsrPrfUsrCod'], errors='coerce')
            df_profiles['UsrPrfUsrCod'] = df_profiles['UsrPrfUsrCod'].fillna(0).astype(int)
            
            df_merged = pd.merge(
                df_devs, 
                df_profiles, 
                left_on='DevUsrCod', 
                right_on='UsrPrfUsrCod', 
                how='left'
            )
        else:
            df_merged = df_devs
            cols_perfil = ['UsrPrfCgo', 'UsrPrfBio', 'UsrPrfFto', 'UsrPrfUrl']
            for col in cols_perfil:
                df_merged[col] = None

        return df_merged.fillna({
            'UsrPrfCgo': 'Colaborador',
            'UsrPrfBio': '',
            'UsrPrfFto': '',
            'UsrPrfUrl': ''
        })

    def create_dev_from_user(self, user_id, user_name, user_login=None):
        """
        Cria um registro na tabela T_Dev vinculado ao usuário.
        
        Args:
            user_id (int): ID do usuário.
            user_name (str): Nome do usuário.
            user_login (str, optional): Recebido para compatibilidade legado, mas IGNORADO
                                      pois T_Dev não armazena mais login externo.
        """
        try:
            model = DevModel()
            
            # 1. Verifica se já existe vínculo
            existing_dev = model.read_by_field('DevUsrCod', user_id)
            if existing_dev:
                return True, "Usuário já vinculado como desenvolvedor."

            # 2. Cria o novo registro
            model.DevUsrCod = user_id
            model.DevNme = user_name
            # Note que não salvamos user_login, pois o campo DevLgnExt foi removido.
            
            if model.save():
                return True, "Desenvolvedor cadastrado com sucesso."
            else:
                return False, "Erro ao salvar registro na tabela T_Dev."
                
        except Exception as e:
            return False, f"Erro interno no serviço: {str(e)}"