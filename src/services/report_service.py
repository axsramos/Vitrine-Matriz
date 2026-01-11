from fpdf import FPDF
from datetime import datetime

class ReportService:
    def generate_release_pdf(self, release_info, tasks_df):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Margens e Largura Útil (Effective Page Width)
        largura_util = pdf.epw 

        # Cabeçalho
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(30, 61, 89)
        pdf.cell(largura_util, 10, "Notas de Versão - Vitrine Matriz", ln=True, align="C")
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(100)
        pdf.cell(largura_util, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="R")
        pdf.ln(10)

        # Informações da Release
        pdf.set_fill_color(230, 233, 239)
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0)
        # Usamos largura_util em vez de 0 para evitar erros de cálculo de margem
        pdf.cell(largura_util, 10, f" Release: {release_info['versao']}", ln=True, fill=True)
        pdf.set_font("Arial", "I", 12)
        pdf.cell(largura_util, 10, f" Título: {release_info['titulo_comunicado']}", ln=True)
        pdf.ln(5)

        # Detalhamento das Tarefas
        pdf.set_font("Arial", "B", 12)
        pdf.cell(largura_util, 10, "Tarefas e Impacto de Negócio:", ln=True)
        pdf.ln(2)

        for _, row in tasks_df.iterrows():
            # Resetamos o X para a margem esquerda antes de cada multi_cell
            pdf.set_x(pdf.l_margin) 
            
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(75, 139, 190)
            texto_titulo = f"- {row['tarefa_titulo']} (Responsável: {row['desenvolvedor']})"
            pdf.multi_cell(largura_util, 7, texto_titulo)
            
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50)
            texto_impacto = f"Impacto: {row['impacto_negocio'] or 'N/A'}"
            pdf.multi_cell(largura_util, 6, texto_impacto)
            pdf.ln(4)
        
        # Convertemos o bytearray retornado pelo fpdf2 para bytes (formato aceito pelo Streamlit)
        return bytes(pdf.output())
    
    def generate_full_team_report(self, team_data, service_dev):
        """
        Gera um relatório completo com todos os desenvolvedores.
        team_data: DataFrame com a lista básica de devs.
        service_dev: Instância do DevService para buscar detalhes de cada um.
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        largura_util = pdf.epw

        for _, dev_row in team_data.iterrows():
            pdf.add_page() # Quebra de página para cada profissional
            
            # Busca detalhes completos (tarefas + impacto) de cada dev
            df_profile = service_dev.get_dev_full_profile(dev_row['id'])
            
            # Cabeçalho do Profissional
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(30, 61, 89)
            pdf.cell(largura_util, 12, dev_row['nome'], ln=True)
            
            pdf.set_font("Arial", "I", 12)
            pdf.set_text_color(100)
            pdf.cell(largura_util, 8, f"Cargo: {dev_row['cargo']}", ln=True)
            pdf.ln(5)

            # Bio / Resumo
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50)
            pdf.multi_cell(largura_util, 6, f"Resumo: {dev_row['bio'] or 'N/A'}")
            pdf.ln(10)

            # Histórico de Entregas
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0)
            pdf.cell(largura_util, 10, "Histórico de Entregas e Impacto:", ln=True)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + largura_util, pdf.get_y())
            pdf.ln(5)

            if df_profile.empty or df_profile['tarefa_titulo'].isnull().all():
                pdf.set_font("Arial", "I", 10)
                pdf.cell(largura_util, 10, "Nenhuma tarefa vinculada até o momento.", ln=True)
            else:
                # Filtra apenas linhas com tarefas
                df_tasks = df_profile[df_profile['tarefa_titulo'].notnull()]
                for _, tarefa in df_tasks.iterrows():
                    pdf.set_x(pdf.l_margin)
                    pdf.set_font("Arial", "B", 11)
                    pdf.set_text_color(75, 139, 190)
                    pdf.multi_cell(largura_util, 7, f"Versão {tarefa['versao']}: {tarefa['tarefa_titulo']}")
                    
                    pdf.set_x(pdf.l_margin)
                    pdf.set_font("Arial", "", 10)
                    pdf.set_text_color(50)
                    pdf.multi_cell(largura_util, 6, f"Impacto: {tarefa['impacto_negocio'] or 'Em análise.'}")
                    pdf.ln(4)

        return bytes(pdf.output())
    