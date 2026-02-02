import os
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
from fpdf import FPDF

from src.models.ReleaseModel import ReleaseModel
from src.core.database import Database

class ReleaseService:

    # --- CRUD BÁSICO (Padronizado com Mixin) ---

    def get_all_releases(self) -> List[Dict]:
        """Retorna todas as releases cadastradas."""
        return ReleaseModel.find_all()

    def get_active_releases(self) -> Dict[str, int]:
        """
        Retorna releases ABERTAS para preencher comboboxes.
        Retorna: {'Titulo da Release': ID}
        """
        releases = ReleaseModel.find_all(
            where="RelSit = ?", 
            params=("Aberto",),
            fields=["RelCod", "RelTit"]
        )
        return {r["RelTit"]: r["RelCod"] for r in releases}

    def get_release_by_version(self, version: str) -> Optional[Dict]:
        """Busca release específica pelo número da versão."""
        res = ReleaseModel.find_all("RelVrs = ?", (version,))
        return res[0] if res else None

    def create_release(self, titulo: str, versao: str, data_publicacao: str, desc: str) -> Tuple[bool, str]:
        """
        Cria nova release.
        Valida unicidade da versão e delega persistência ao Modelo.
        """
        # 1. Validação
        if self.get_release_by_version(versao):
            return False, f"A versão {versao} já existe."

        # 2. Criação (Auditoria automática via Mixin)
        try:
            new_rel = ReleaseModel(
                RelTit=titulo,
                RelVrs=versao,
                RelDat=data_publicacao,
                RelDsc=desc,
                RelSit="Aberto"
            )

            if new_rel.create():
                return True, "Release criada com sucesso!"
            return False, "Erro ao gravar release."
            
        except Exception as e:
            return False, f"Erro técnico: {str(e)}"

    def close_release(self, rel_id: int) -> bool:
        """Encerra uma release (Status = Fechado)."""
        rel = ReleaseModel(RelCod=rel_id, RelSit="Fechado")
        return rel.update()
        
    def delete_release(self, rel_id: int) -> bool:
        """Exclusão da release."""
        rel = ReleaseModel(RelCod=rel_id)
        return rel.delete()

    # --- FUNCIONALIDADES DE RELATÓRIOS (Refatoradas para Python Nativo) ---

    def get_release_details_for_report(self) -> List[Dict]:
        """
        Busca dados enriquecidos para relatórios.
        Nota: Mantemos SQL direto aqui pois envolve JOINs complexos que o CRUD padrão não cobre.
        """
        db = Database()
        # Traz dados da release e contagem de tarefas associadas
        sql = """
            SELECT 
                r.RelCod, r.RelVrs, r.RelDat, r.RelTit, r.RelDsc, r.RelSit,
                (SELECT COUNT(*) FROM T_Trf t WHERE t.TrfRelCod = r.RelCod) as QtdTarefas
            FROM T_Rel r
            WHERE r.RelSit != 'Cancelado'
            ORDER BY r.RelDat DESC
        """
        return db.select(sql)

    def generate_monthly_pdf(self, releases_data: List[Dict]) -> bytes:
        """
        Gera PDF agrupado por mês.
        Refatorado para não depender de Pandas (DataFrame).
        """
        if not releases_data:
            return None
        
        pdf = FPDF()
        pdf.add_page()
        
        # 1. Agrupamento Manual (Substitui pandas groupby)
        grouped = defaultdict(list)
        for r in releases_data:
            try:
                # Converte string 'YYYY-MM-DD' para objeto data
                dt = datetime.strptime(str(r['RelDat']), '%Y-%m-%d')
                key = (dt.year, dt.month)
                grouped[key].append(r)
            except (ValueError, TypeError):
                continue # Ignora datas inválidas

        # Ordena chaves (Ano, Mes) do mais recente para o mais antigo
        sorted_keys = sorted(grouped.keys(), key=lambda x: (x[0], x[1]), reverse=True)

        meses_pt = {1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho',
                   7:'Julho', 8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}

        # 2. Geração do Documento
        for ano, mes in sorted_keys:
            subset = grouped[(ano, mes)]
            
            # Cabeçalho do Mês
            pdf.set_font("Arial", "B", 14)
            pdf.set_fill_color(240, 240, 240)
            nome_mes = meses_pt.get(mes, '').upper()
            pdf.cell(0, 10, f"{nome_mes} / {ano}", ln=True, fill=True)
            
            # Lista de Releases do Mês
            for item in subset:
                pdf.set_font("Arial", "B", 11)
                titulo_sanitizado = self._sanitize_text(f"v{item['RelVrs']} - {item.get('RelTit', '')}")
                pdf.cell(0, 8, titulo_sanitizado, ln=True)
                
                pdf.set_font("Arial", "", 9)
                desc_sanitizada = self._sanitize_text(item.get('RelDsc', ''))
                pdf.multi_cell(0, 5, desc_sanitizada)
                pdf.ln(2)

        try:
            return bytes(pdf.output(dest='S'))
        except Exception as e:
            print(f"Erro na geração do binário PDF: {e}")
            return None

    def _sanitize_text(self, text: str) -> str:
        """
        Trata caracteres para o FPDF (que usa encoding latin-1 por padrão).
        Substitui caracteres não suportados para evitar erros de geração.
        """
        if not text: return ""
        try:
            # Tenta converter para latin-1, substituindo o que não for compatível
            return text.encode('latin-1', 'replace').decode('latin-1')
        except:
            return text