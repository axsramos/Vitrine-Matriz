from fpdf import FPDF
from datetime import datetime

class ReportService(FPDF):
    def header(self):
        """Cabeçalho padrão para todos os documentos."""
        self.set_font('Arial', 'B', 15)
        self.set_text_color(30, 61, 89)
        self.cell(0, 10, 'Relatório de Entregas - Portal Matriz', border=False, ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.set_text_color(100)
        self.cell(0, 10, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True, align='C')
        self.ln(10)

    def footer(self):
        """Rodapé padrão com numeração."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
    
    def generate_release_report(self, df_tasks):
        """Relatório de Atividades por Período (Tabela)."""
        self.add_page()
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Atividades por Período', ln=True)
        
        # Cabeçalho da Tabela
        self.set_fill_color(200, 220, 255)
        self.set_font('Arial', 'B', 10)
        self.cell(100, 10, 'Tarefa', 1, 0, 'C', 1)
        self.cell(40, 10, 'Desenvolvedor', 1, 0, 'C', 1)
        self.cell(50, 10, 'Impacto', 1, 1, 'C', 1)
        
        self.set_font('Arial', '', 9)
        for _, row in df_tasks.iterrows():
            # multi_cell não é usado aqui para manter a estrutura de tabela simples
            self.cell(100, 10, str(row['titulo'])[:50], 1)
            self.cell(40, 10, str(row['dev']), 1)
            self.cell(50, 10, str(row['impacto']), 1, 1)
        
        return bytes(self.output())

    def generate_release_pdf(self, release_info, tasks_df):
        """Notas de Versão (Release) com detalhamento de impacto."""
        self.add_page()
        largura_util = self.epw 

        # Título da Release
        self.set_fill_color(230, 233, 239)
        self.set_font("Arial", "B", 14)
        self.set_text_color(0)
        self.cell(largura_util, 10, f" Release: {release_info['versao']}", ln=True, fill=True)
        self.set_font("Arial", "I", 12)
        self.cell(largura_util, 10, f" Título: {release_info['titulo_comunicado']}", ln=True)
        self.ln(5)

        self.set_font("Arial", "B", 12)
        self.cell(largura_util, 10, "Tarefas e Impacto de Negócio:", ln=True)
        self.ln(2)

        for _, row in tasks_df.iterrows():
            self.set_x(self.l_margin) 
            self.set_font("Arial", "B", 11)
            self.set_text_color(75, 139, 190)
            # Nota: use os nomes de colunas corretos do seu DataFrame (tarefa_titulo ou titulo)
            pdf_titulo = f"- {row.get('tarefa_titulo', row.get('titulo', 'N/A'))}"
            self.multi_cell(largura_util, 7, pdf_titulo)
            
            self.set_x(self.l_margin)
            self.set_font("Arial", "", 10)
            self.set_text_color(50)
            # Busca o impacto de negócio
            texto_impacto = f"Impacto: {row.get('impacto_negocio', 'N/A')}"
            self.multi_cell(largura_util, 6, texto_impacto)
            self.ln(4)
        
        return bytes(self.output())
    
    def generate_full_team_report(self, team_data, service_dev):
        """Relatório completo de performance da equipe."""
        largura_util = self.epw

        for _, dev_row in team_data.iterrows():
            self.add_page() 
            df_profile = service_dev.get_dev_full_profile(dev_row['id'])
            
            # Cabeçalho do Dev
            self.set_font("Arial", "B", 18)
            self.set_text_color(30, 61, 89)
            self.cell(largura_util, 12, dev_row['nome'], ln=True)
            self.set_font("Arial", "I", 12)
            self.cell(largura_util, 8, f"Cargo: {dev_row['cargo']}", ln=True)
            self.ln(10)

            # Histórico
            self.set_font("Arial", "B", 12)
            self.set_text_color(0)
            self.cell(largura_util, 10, "Histórico de Entregas:", ln=True)
            self.line(self.l_margin, self.get_y(), self.l_margin + largura_util, self.get_y())
            self.ln(5)

            if df_profile.empty:
                self.cell(largura_util, 10, "Nenhuma tarefa vinculada.", ln=True)
            else:
                for _, tarefa in df_profile.iterrows():
                    self.set_font("Arial", "B", 11)
                    self.set_text_color(75, 139, 190)
                    titulo = f"V{tarefa['versao']}: {tarefa['tarefa_titulo']}"
                    self.multi_cell(largura_util, 7, titulo)
                    self.ln(2)

        return bytes(self.output())