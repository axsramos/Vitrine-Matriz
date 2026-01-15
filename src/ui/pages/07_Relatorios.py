import streamlit as st
from datetime import datetime, timedelta
from src.services.release_service import ReleaseService
from src.services.dev_service import DevService
from src.services.report_service import ReportService
from src.services.task_service import TaskService
from src.core.auth_middleware import require_auth
from src.core.ui_utils import init_page

require_auth()

init_page("Relatórios em PDF", "centered")
    
st.title("📄 Exportação de Relatórios")
report_service = ReportService() # Instância única para toda a página

# --- SEÇÃO 1: RELATÓRIO DE RELEASE ---
st.subheader("📦 Notas de Versão (Release)")
rel_service = ReleaseService()
df_releases = rel_service.get_all_releases()

if not df_releases.empty:
    opcoes_rel = {row['versao']: row['id'] for _, row in df_releases.iterrows()}
    versao_sel = st.selectbox("Selecione a versão para exportar:", options=list(opcoes_rel.keys()))
    
    if st.button("Gerar PDF da Release", use_container_width=True):
        all_tasks = rel_service.get_all_releases_with_tasks()
        tasks_release = all_tasks[all_tasks['versao'] == versao_sel]
        info_release = df_releases[df_releases['versao'] == versao_sel].iloc[0]
        
        pdf_bytes = report_service.generate_release_pdf(info_release, tasks_release)
        st.download_button("💾 Baixar PDF da Release", pdf_bytes, f"Release_{versao_sel}.pdf", "application/pdf")

st.divider()

# --- SEÇÃO 2: RELATÓRIO DE EQUIPE ---
st.subheader("👥 Performance da Equipe")
if st.button("🛠️ Gerar Relatório Consolidado da Equipe", use_container_width=True):
    dev_service = DevService()
    df_team = dev_service.get_team_stats()
    
    if df_team.empty:
        st.warning("Não há desenvolvedores cadastrados.")
    else:
        with st.spinner("Compilando dados..."):
            pdf_equipe = report_service.generate_full_team_report(df_team, dev_service)
            st.success("Relatório da equipe pronto!")
            st.download_button(
                label="💾 Baixar Relatório da Equipe (PDF)",
                data=pdf_equipe,
                file_name=f"Performance_Equipe_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

st.divider()

# --- SEÇÃO 3: RELATÓRIO POR PERÍODO ---
st.subheader("📅 Atividades por Período")
col1, col2 = st.columns(2)
with col1:
    data_ini = st.date_input("Início:", datetime.now() - timedelta(days=30))
with col2:
    data_fim = st.date_input("Fim:", datetime.now())

task_service = TaskService()
# Agora passando os parâmetros de data corretamente
df_tasks = task_service.get_all_with_details(data_ini, data_fim) 

if not df_tasks.empty:
    st.write(f"Encontradas **{len(df_tasks)}** tarefas no período.")
    st.dataframe(df_tasks, use_container_width=True)
    
    if st.button("🛠️ Gerar Relatório de Atividades (PDF)", use_container_width=True):
        # Usando a instância report_service definida no topo
        pdf_bytes = report_service.generate_release_report(df_tasks)
        
        st.download_button(
            label="💾 Baixar Relatório de Atividades",
            data=pdf_bytes,
            file_name=f"Relatorio_Periodo_{data_ini}_{data_fim}.pdf",
            mime="application/pdf"
        )
else:
    st.info("Nenhuma tarefa encontrada para este intervalo de datas.")