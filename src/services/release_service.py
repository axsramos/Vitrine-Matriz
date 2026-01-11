from src.core.database import get_connection

class ReleaseService:
    def get_all_releases_with_tasks(self):
        """Versão corrigida: Adicionado JOIN com desenvolvedores para o campo 'desenvolvedor'."""
        query = """
            SELECT 
                COALESCE(r.versao, 'Sem Versão') as versao, 
                r.titulo_comunicado, 
                r.data_publicacao,
                t.titulo as tarefa_titulo, 
                t.descricao_tecnica,
                t.impacto_negocio,
                d.nome as desenvolvedor  -- Campo que estava faltando
            FROM tarefas t
            LEFT JOIN releases r ON t.id_release = r.id
            LEFT JOIN desenvolvedores d ON t.id_desenvolvedor = d.id -- Join necessário
            WHERE t.AudDlt IS NULL
            ORDER BY r.data_publicacao DESC, t.id DESC
        """
        with get_connection() as conn:
            import pandas as pd
            return pd.read_sql_query(query, conn)
    
    def get_all_releases(self):
        """Versão corrigida: Incluindo o título do comunicado para o relatório."""
        query = """
            SELECT id, versao, titulo_comunicado 
            FROM releases 
            ORDER BY data_publicacao DESC
        """
        with get_connection() as conn:
            import pandas as pd
            return pd.read_sql_query(query, conn)