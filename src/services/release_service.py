import os
import re
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from src.models.ReleaseModel import ReleaseModel
from src.core.database import Database

class ReleaseService:
    def __init__(self):
        self.db = Database()
        self.model = ReleaseModel()

    def create_release(self, version, title, user_audit="system"):
        try:
            model = ReleaseModel()
            exists = model.read_all(where="RelVrs = ?", params=(version,))
            if exists:
                return False, f"A versão {version} já existe."

            model.RelVrs = version
            model.RelTtlCmm = title
            model.RelAudUsr = user_audit
            model.RelDat = datetime.now().strftime('%Y-%m-%d')
            
            if model.save():
                new_rel = model.read_all(where="RelVrs = ?", params=(version,))
                return True, new_rel[0]['RelCod']
            return False, "Erro ao salvar release."
        except Exception as e:
            return False, str(e)

    def get_release_details(self):
        """Busca releases com agregados de desenvolvedores e tarefas para a UI."""
        sql = """
            SELECT 
                r.RelCod, r.RelVrs, r.RelDat, r.RelTtlCmm,
                GROUP_CONCAT(DISTINCT d.DevNom) as Desenvolvedores,
                GROUP_CONCAT(t.TrfTtl, '||') as ListaTarefas,
                COUNT(t.TrfCod) as QtdTarefas
            FROM T_Rel r
            LEFT JOIN T_Trf t ON r.RelCod = t.TrfRelCod
            LEFT JOIN T_Dev d ON t.TrfDevCod = d.DevCod
            WHERE r.RelAudDlt IS NULL
            GROUP BY r.RelCod
            ORDER BY r.RelDat DESC
        """
        return self.db.select(sql)
    
    def _sanitizar_para_pdf(self, texto):
        if not texto: return ""
        subs = {'—': '-', '–': '-', '“': '"', '”': '"', '‘': "'", '’': "'", '📅': ''}
        for k, v in subs.items():
            texto = texto.replace(k, v)
        return re.sub(r'[^\x00-\xff]', '', str(texto))

    def _get_template(self, nome):
        path = os.path.join('src', 'reports', 'templates', f'{nome}.html')
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _render_html(self, template_name, data_dict):
        template = self._get_template(template_name)
        for key, value in data_dict.items():
            template = template.replace(f'{{{{ {key} }}}}', str(value))
        return template

    def _formatar_lista_tarefas_pdf(self, tarefas_str):
        if not tarefas_str: return "Nenhum item registrado."
        itens = tarefas_str.split('||')
        return "<br>".join([f"&bull; {self._sanitizar_para_pdf(i)}" for i in itens])

    def export_pdf_geral(self, df):
        try:
            pdf = FPDF()
            pdf.add_page()
            html_acumulado = ""
            for _, row in df.iterrows():
                dados = {
                    'RelVrs': row['RelVrs'],
                    'RelTtlCmm': self._sanitizar_para_pdf(row['RelTtlCmm']),
                    'RelDat': row['RelDat'].strftime('%d/%m/%Y'),
                    'Desenvolvedores': self._sanitizar_para_pdf(row.get('Desenvolvedores', 'Equipe')),
                    'ItensLista': self._formatar_lista_tarefas_pdf(row.get('ListaTarefas', ''))
                }
                html_acumulado += self._render_html('release_detalhada', dados)

            html_final = self._render_html('layout_base', {
                'Conteudo': html_acumulado,
                'DataHoje': datetime.now().strftime('%d/%m/%Y %H:%M')
            })
            pdf.write_html(html_final)
            return bytes(pdf.output(dest='S'))
        except Exception as e:
            return None

    def export_pdf_mensal(self, df, meses_pt):
        try:
            pdf = FPDF()
            pdf.add_page()
            df['Ano'] = df['RelDat'].dt.year
            df['MesNum'] = df['RelDat'].dt.month
            grupos = df.sort_values(['Ano', 'MesNum'], ascending=False).groupby(['Ano', 'MesNum'], sort=False)
            
            html_acumulado = ""
            for (ano, mes_num), subset in grupos:
                mes_ano = f"{meses_pt.get(mes_num).upper()} / {ano}"
                html_acumulado += f'<h2 style="color: #0D0D2B; border-bottom: 2px solid #00FF01;">{mes_ano}</h2>'
                for _, row in subset.iterrows():
                    dados = {
                        'RelVrs': row['RelVrs'],
                        'RelTtlCmm': self._sanitizar_para_pdf(row['RelTtlCmm']),
                        'RelDat': row['RelDat'].strftime('%d/%m/%Y'),
                        'Desenvolvedores': self._sanitizar_para_pdf(row.get('Desenvolvedores', 'Equipe')),
                        'ItensLista': self._formatar_lista_tarefas_pdf(row.get('ListaTarefas', ''))
                    }
                    html_acumulado += self._render_html('release_mensal', dados)

            html_final = self._render_html('layout_base', {
                'Conteudo': html_acumulado,
                'DataHoje': datetime.now().strftime('%d/%m/%Y %H:%M')
            })
            pdf.write_html(html_final)
            return bytes(pdf.output(dest='S'))
        except Exception as e:
            return None
