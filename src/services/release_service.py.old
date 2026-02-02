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
    
    def get_latest_version_label(self):
        """Retorna a etiqueta da última versão lançada para sugestão na UI."""
        sql = "SELECT RelVrs FROM T_Rel ORDER BY RelDat DESC, RelCod DESC LIMIT 1"
        result = self.db.select(sql)
        if result:
            return result[0]['RelVrs']
        return "0.0.0"
    
    def _sanitizar_para_pdf(self, texto):
        if not texto: return ""
        subs = {'—': '-', '–': '-', '“': '"', '”': '"', '‘': "'", '’': "'", '📅': ''}
        for k, v in subs.items():
            texto = texto.replace(k, v)
        return re.sub(r'[^\x00-\xff]', '', str(texto))

    # def _get_template(self, nome):
    #     # Caminho absoluto para evitar erro de 'Template não encontrado' no Laragon
    #     base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #     path = os.path.join(base_dir, 'src', 'reports', 'templates', f'{nome}.html')
        
    #     if not os.path.exists(path):
    #         return f""
            
    #     with open(path, 'r', encoding='utf-8') as f:
    #         return f.read()

    # def _render_html(self, template_name, data_dict):
    #     template = self._get_template(template_name)
    #     for key, value in data_dict.items():
    #         template = template.replace(f'{{{{ {key} }}}}', str(value))
    #     return template

    # def _formatar_lista_tarefas_pdf(self, tarefas_str):
    #     if not tarefas_str:
    #         return "Nenhum item registrado."
        
    #     itens = tarefas_str.split('||')
    #     # Use apenas texto puro e <br> para máxima compatibilidade com FPDF2
    #     lista_formatada = ""
    #     for i in itens:
    #         item_limpo = self._sanitizar_para_pdf(i)
    #         lista_formatada += f" - {item_limpo}<br>"
        
    #     return lista_formatada.strip()

    # def export_pdf_geral(self, df):
    #     try:
    #         if df.empty:
    #             return None

    #         pdf = FPDF()
    #         pdf.add_page()
            
    #         # Ordenamos por data para garantir a cronologia no relatório
    #         df = df.sort_values('RelDat', ascending=False)
            
    #         html_acumulado = ""
    #         for _, row in df.iterrows():
    #             # Tratamento da data de referência para exibição no PDF
    #             data_str = row['RelDat'].strftime('%d/%m/%Y') if pd.notnull(row['RelDat']) else "Sem data"
                
    #             dados = {
    #                 'RelVrs': row['RelVrs'],
    #                 'RelTtlCmm': self._sanitizar_para_pdf(row['RelTtlCmm']),
    #                 'RelDat': data_str,
    #                 'Desenvolvedores': self._sanitizar_para_pdf(row.get('Desenvolvedores', 'Equipe')),
    #                 'ItensLista': self._formatar_lista_tarefas_pdf(row.get('ListaTarefas', ''))
    #             }
    #             html_acumulado += self._render_html('release_detalhada', dados)

    #         # Injeção no Layout Base
    #         html_final = self._render_html('layout_base', {
    #             'Conteudo': html_acumulado,
    #             'DataHoje': datetime.now().strftime('%d/%m/%Y %H:%M')
    #         })

    #         pdf.write_html(html_final)
    #         return bytes(pdf.output(dest='S'))
    #     except Exception as e:
    #         print(f"Erro no PDF Geral: {e}")
    #         return None

    # def export_pdf_mensal(self, df, meses_pt):
    #     try:
    #         pdf = FPDF()
    #         pdf.add_page()
    #         df['Ano'] = df['RelDat'].dt.year
    #         df['MesNum'] = df['RelDat'].dt.month
    #         grupos = df.sort_values(['Ano', 'MesNum'], ascending=False).groupby(['Ano', 'MesNum'], sort=False)
            
    #         html_acumulado = ""
    #         for (ano, mes_num), subset in grupos:
    #             mes_ano = f"{meses_pt.get(mes_num).upper()} / {ano}"
    #             html_acumulado += f'<h2 style="color: #0D0D2B; border-bottom: 2px solid #00FF01;">{mes_ano}</h2>'
    #             for _, row in subset.iterrows():
    #                 dados = {
    #                     'RelVrs': row['RelVrs'],
    #                     'RelTtlCmm': self._sanitizar_para_pdf(row['RelTtlCmm']),
    #                     'RelDat': row['RelDat'].strftime('%d/%m/%Y'),
    #                     'Desenvolvedores': self._sanitizar_para_pdf(row.get('Desenvolvedores', 'Equipe')),
    #                     'ItensLista': self._formatar_lista_tarefas_pdf(row.get('ListaTarefas', ''))
    #                 }
    #                 html_acumulado += self._render_html('release_mensal', dados)
    #
    #         html_final = self._render_html('layout_base', {
    #             'Conteudo': html_acumulado,
    #             'DataHoje': datetime.now().strftime('%d/%m/%Y %H:%M')
    #         })
    #         pdf.write_html(html_final)
    #         return bytes(pdf.output(dest='S'))
    #     except Exception as e:
    #         return None

    def export_pdf_simples(self, df, titulo_relatorio="Relatorio de Versao"):
        try:
            if df.empty: return None
            
            pdf = FPDF()
            pdf.add_page()
            
            html_acumulado = ""
            for _, row in df.iterrows():
                # Limpeza rápida de strings para evitar erros de caractere
                itens = str(row.get('ListaTarefas', '')).replace('||', '<br> - ')
                
                dados = {
                    'RelVrs': row['RelVrs'],
                    'RelTtlCmm': self._sanitizar_para_pdf(row['RelTtlCmm']),
                    'RelDat': row['RelDat'].strftime('%d/%m/%Y') if pd.notnull(row['RelDat']) else "N/A",
                    'Desenvolvedores': self._sanitizar_para_pdf(row.get('Desenvolvedores', 'Equipe')),
                    'ItensLista': self._sanitizar_para_pdf(itens)
                }
                html_acumulado += self._render_html('release_detalhada', dados)

            html_final = self._render_html('layout_base', {
                'Conteudo': html_acumulado,
                'DataHoje': datetime.now().strftime('%d/%m/%Y %H:%M')
            })
            
            pdf.write_html(html_final)
            return bytes(pdf.output(dest='S'))
        except Exception as e:
            print(f"ERRO CRITICO PDF: {e}")
            return None
    
    def export_pdf_direto(self, df):
        try:
            if df.empty:
                return None
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "VITRINE MATRIZ - Notas de Versao", ln=True, align='C')
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
            pdf.ln(10)

            for _, row in df.iterrows():
                # Cabeçalho da Versão
                pdf.set_font("Arial", "B", 12)
                titulo = self._sanitizar_para_pdf(f"Versao: {row['RelVrs']} - {row['RelTtlCmm']}")
                pdf.cell(0, 10, titulo, ln=True)
                
                # Detalhes
                pdf.set_font("Arial", "I", 9)
                data_rel = row['RelDat'].strftime('%d/%m/%Y') if pd.notnull(row['RelDat']) else "N/A"
                pdf.cell(0, 5, f"Data: {data_rel} | Devs: {row.get('Desenvolvedores', 'Equipe')}", ln=True)
                
                # Itens
                pdf.set_font("Arial", "", 10)
                pdf.multi_cell(0, 5, f"Itens:\n{str(row.get('ListaTarefas', '')).replace('||', '\n- ')}")
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)

            return bytes(pdf.output(dest='S'))
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            return None
    
    def export_pdf_geral_direto(self, df):
        """Gera o PDF do Histórico Geral sem depender de HTML externo."""
        try:
            if df.empty: return None
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "NOTAS DE VERSAO - HISTORICO GERAL", ln=True, align='C')
            pdf.ln(10)

            for _, row in df.iterrows():
                # Título da Versão
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, self._sanitizar_para_pdf(f"v{row['RelVrs']} - {row['RelTtlCmm']}"), ln=True)
                # Metadados
                pdf.set_font("Arial", "I", 9)
                data_v = row['RelDat'].strftime('%d/%m/%Y') if pd.notnull(row['RelDat']) else "N/A"
                pdf.cell(0, 5, f"Data: {data_v} | Equipe: {row.get('Desenvolvedores', 'N/A')}", ln=True)
                # Tarefas
                pdf.set_font("Arial", "", 10)
                tarefas = str(row.get('ListaTarefas', '')).replace('||', '\n- ')
                pdf.multi_cell(0, 5, f"Itens:\n- {self._sanitizar_para_pdf(tarefas)}")
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            
            return bytes(pdf.output(dest='S'))
        except Exception as e:
            print(f"Erro PDF Geral: {e}")
            return None

    def export_pdf_mensal_direto(self, df, meses_pt):
        """Gera o PDF Agrupado por Mês sem depender de HTML externo."""
        try:
            if df.empty: return None
            pdf = FPDF()
            pdf.add_page()
            
            df['Ano'] = df['RelDat'].dt.year
            df['MesNum'] = df['RelDat'].dt.month
            grupos = df.sort_values(['Ano', 'MesNum'], ascending=False).groupby(['Ano', 'MesNum'], sort=False)

            for (ano, mes_num), subset in grupos:
                pdf.set_font("Arial", "B", 14)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 10, f"{meses_pt.get(mes_num).upper()} / {ano}", ln=True, fill=True)
                
                for _, row in subset.iterrows():
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 8, self._sanitizar_para_pdf(f"v{row['RelVrs']} - {row['RelTtlCmm']}"), ln=True)
                    pdf.set_font("Arial", "", 9)
                    tarefas = str(row.get('ListaTarefas', '')).replace('||', ', ')
                    pdf.multi_cell(0, 5, f"Resumo: {self._sanitizar_para_pdf(tarefas)}")
                    pdf.ln(2)
                pdf.ln(5)

            return bytes(pdf.output(dest='S'))
        except Exception as e:
            print(f"Erro PDF Mensal: {e}")
            return None