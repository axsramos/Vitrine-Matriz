import pandas as pd
from src.models.DevModel import DevModel
from src.models.UserProfileModel import UserProfileModel

class DevService:
    def get_all_devs_dataframe(self):
        """
        Retorna um DataFrame consolidado utilizando apenas os Models (CrudMixin).
        Realiza o 'Join' em memória usando Pandas.
        """
        # 1. Busca dados brutos usando o padrão CrudMixin
        dev_model = DevModel()
        profile_model = UserProfileModel()
        
        devs_data = dev_model.read_all()
        profiles_data = profile_model.read_all()

        # Se não houver devs, retorna DF vazio com as colunas esperadas
        if not devs_data:
            return pd.DataFrame(columns=['DevNme', 'UsrPrfCgo', 'UsrPrfBio', 'UsrPrfFto', 'UsrPrfUrl'])

        # 2. Converte para DataFrames
        df_devs = pd.DataFrame(devs_data)
        df_profiles = pd.DataFrame(profiles_data)

        # 3. Tratamento de Tipos para o Join (CORREÇÃO DO ERRO)
        if not df_devs.empty:
            # Garante que é numérico, coage erros para NaN
            df_devs['DevUsrCod'] = pd.to_numeric(df_devs['DevUsrCod'], errors='coerce')
            # Preenche Nulos com 0 para permitir a conversão para Int sem erro
            df_devs['DevUsrCod'] = df_devs['DevUsrCod'].fillna(0).astype(int)
            
        if not df_profiles.empty:
            # Mesma proteção para o lado do Perfil
            df_profiles['UsrPrfUsrCod'] = pd.to_numeric(df_profiles['UsrPrfUsrCod'], errors='coerce')
            df_profiles['UsrPrfUsrCod'] = df_profiles['UsrPrfUsrCod'].fillna(0).astype(int)
            
            # MERGE: Devs + Perfil
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

        # 4. Seleciona e Trata colunas finais
        df_final = df_merged.fillna({
            'UsrPrfCgo': 'Colaborador', # Ajuste no default
            'UsrPrfBio': '',
            'UsrPrfFto': '',
            'UsrPrfUrl': ''
        })

        return df_final