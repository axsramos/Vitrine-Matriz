import streamlit as st
import csv
from io import StringIO
from datetime import datetime

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth

# --- SERVIÇOS ---
from src.services.release_service import ReleaseService

# --- METADADOS ---
from src.models.md.RelMD import RelMD

# Configuração da Página
st.set_page_config(
    page_title=f"Relatórios | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth()

st.title("📊 Central de Relatórios")
st.write("Exporte o histórico de versões e métricas do sistema.")

# Instância do Serviço
rel_service = ReleaseService()

# --- CARREGAMENTO DE DADOS ---
# Busca dados enriquecidos (com contagem de tarefas) através do serviço
report_data = rel_service.get_release_details_for_report()

if not report_data:
    st.warning("Não há dados suficientes para gerar relatórios no momento.")
    st.stop()

st.divider()

# --- ÁREA DE DOWNLOADS ---
# Layout em duas colunas para os tipos de relatório
c1, c2 = st.columns(2)

# --- 1. RELATÓRIO PDF (DOCUMENTAÇÃO) ---
with c1:
    with st.container(border=True):
        st.subheader("📄 Documentação Oficial")
        st.write("Arquivo PDF agrupado por mês, ideal para impressão ou arquivamento de notas de versão.")
        
        # Gerar PDF em memória
        pdf_bytes = rel_service.generate_monthly_pdf(report_data)
        
        if pdf_bytes:
            filename = f"relatorio_versoes_{datetime.now().strftime('%Y%m%d')}.pdf"
            st.download_button(
                label="⬇️ Baixar PDF Mensal",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        else:
            st.error("Erro ao processar PDF.")

# --- 2. EXPORTAÇÃO DE DADOS (CSV/EXCEL) ---
with c2:
    with st.container(border=True):
        st.subheader("📊 Dados Analíticos")
        st.write("Exportação em formato CSV (compatível com Excel) contendo os dados brutos para análise.")
        
        # Gerar CSV em memória usando Python Nativo (sem Pandas)
        def convert_to_csv(data_list):
            if not data_list: return ""
            output = StringIO()
            # Define as colunas baseado nas chaves do primeiro dicionário
            # Ou forçamos ordem específica para ficar bonito
            fieldnames = ['RelCod', 'RelVrs', 'RelTit', 'RelDat', 'RelSit', 'QtdTarefas']
            
            writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for row in data_list:
                writer.writerow(row)
            return output.getvalue()

        csv_data = convert_to_csv(report_data)
        
        filename_csv = f"dados_versoes_{datetime.now().strftime('%Y%m%d')}.csv"
        st.download_button(
            label="⬇️ Baixar CSV (Excel)",
            data=csv_data,
            file_name=filename_csv,
            mime="text/csv",
            use_container_width=True
        )

# --- PRÉ-VISUALIZAÇÃO ---
st.divider()
st.subheader("🔍 Pré-visualização dos Dados")

# Formatação simples para tabela na tela
display_data = []
for item in report_data:
    display_data.append({
        RelMD.FIELDS_MD['RelVrs']['Label']: item.get('RelVrs'),
        RelMD.FIELDS_MD['RelTit']['Label']: item.get('RelTit'),
        RelMD.FIELDS_MD['RelDat']['Label']: item.get('RelDat'),
        "Tarefas": item.get('QtdTarefas', 0),
        RelMD.FIELDS_MD['RelSit']['Label']: item.get('RelSit')
    })

st.dataframe(display_data, use_container_width=True)