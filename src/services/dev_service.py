from typing import List, Dict, Tuple, Optional
from src.models.DevModel import DevModel
from src.core.database import Database
from src.services.user_service import UserService
from src.models.UserRole import UserRole

class DevService:
    
    def get_all_devs(self) -> List[Dict]:
        """
        Retorna a lista completa de desenvolvedores com todos os campos (incluindo DevUsrCod).
        Usado para identificar se o usuário logado é um Dev.
        """
        return DevModel.find_all(fields=['DevCod', 'DevNom', 'DevUsrCod'])

    def get_dev_options(self) -> Dict[str, int]:
        """
        Retorna dicionário {Nome: ID} para popular selectboxes.
        """
        # Busca apenas campos necessários via Mixin
        devs = DevModel.find_all(fields=["DevCod", "DevNom"])
        return {d["DevNom"]: d["DevCod"] for d in devs}
    
    def get_portfolio_data(self) -> List[Dict]:
        """
        Retorna dados consolidados de Desenvolvedores + Perfil.
        Substitui o antigo 'get_all_devs_dataframe' e 'get_all_developers'.
        Usado para os Cards de Equipe e Detalhes.
        """
        db = Database()
        # Query otimizada trazendo dados do Dev e do Perfil
        sql = """
            SELECT 
                d.DevCod, d.DevNom, d.DevUsrCod,
                p.UsrPrfCgo, p.UsrPrfBio, p.UsrPrfFto, p.UsrPrfUrl
            FROM T_Dev d
            LEFT JOIN T_UsrPrf p ON d.DevUsrCod = p.UsrPrfUsrCod
            ORDER BY d.DevNom ASC
        """
        # O Soft Delete (d.DevAudDlt IS NULL) deve ser tratado se a tabela suportar.
        # Como é SQL direto, adicionamos a cláusula se existir o campo.
        # Assumindo que T_Dev tem DevAudDlt:
        sql = sql.replace("ORDER BY", "WHERE d.DevAudDlt IS NULL ORDER BY")
        
        return db.select(sql)
    
    def check_if_user_is_dev(self, user_id: int) -> bool:
        """Verifica se um Usuário do sistema já é um Desenvolvedor."""
        # Filtra pelo campo da FK de usuário (DevUsrCod)
        results = DevModel.find_all("DevUsrCod = ?", (user_id,))
        return len(results) > 0

    def create_dev_from_user(self, user_id: int, nome: str) -> Tuple[bool, str]:
        """
        Promove um usuário a desenvolvedor.
        1. Cria registro em T_Dev.
        2. Atualiza permissão do usuário para 'manager' (se configurado).
        """
        # 1. Validação
        if self.check_if_user_is_dev(user_id):
            return False, "Este usuário já é um desenvolvedor."

        # 2. Criação (Auditoria automática via Mixin)
        try:
            new_dev = DevModel(
                DevNom=nome,
                DevUsrCod=user_id,
                DevSit="Ativo"
            )
            
            if new_dev.create():
                # 3. Atualização de Permissão (Opcional - Regra de Negócio)
                try:
                    u_service = UserService()
                    # Promove para Manager para ter acesso a telas de gestão
                    u_service.update_permission(user_id, UserRole.MANAGER)
                except Exception as e:
                    print(f"Aviso: Não foi possível atualizar a role do usuário: {e}")

                return True, f"{nome} promovido a desenvolvedor com sucesso!"
            
            return False, "Erro ao gravar registro de desenvolvedor."
            
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"

    def update_dev(self, dev_id: int, nome: str) -> Tuple[bool, str]:
        """Atualiza dados básicos do desenvolvedor."""
        dev = DevModel(DevCod=dev_id, DevNom=nome)
        if dev.update():
            return True, "Desenvolvedor atualizado."
        return False, "Erro ao atualizar."