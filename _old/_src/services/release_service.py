import pandas as pd
from src.models import ReleaseModel

class ReleaseService:
    def get_all_releases(self):
        # Ordena por Data de Publicação (desc)
        # Nota: O Mixin simples não tem ORDER BY, então ordenamos no Pandas
        data = ReleaseModel.read_all()
        df = pd.DataFrame(data)
        
        if df.empty:
            return pd.DataFrame(columns=ReleaseModel.FIELDS)
            
        # Ordenação via Pandas
        if 'RelDtaPub' in df.columns:
            df['RelDtaPub'] = pd.to_datetime(df['RelDtaPub'])
            df = df.sort_values(by='RelDtaPub', ascending=False)
            
        return df

    def create_release(self, version: str, title: str):
        try:
            # Verifica duplicidade
            existing = ReleaseModel.read_all(where="RelVrs = ?", params=(version,))
            if existing:
                return False, f"A versão {version} já existe."

            # Cria nova release
            rel = ReleaseModel()
            rel.RelVrs = version
            rel.RelTtlCmm = title
            # RelDtaPub é automático no banco ou podemos setar aqui
            
            if rel.save():
                return True, rel.RelCod # Retorna ID para vincular tarefas
            return False, "Erro ao salvar release."
            
        except Exception as e:
            return False, f"Erro: {str(e)}"