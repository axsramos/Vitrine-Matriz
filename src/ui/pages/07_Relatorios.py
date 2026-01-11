import streamlit as st
from datetime import datetime
from src.services.release_service import ReleaseService
from src.services.dev_service import DevService
from src.services.report_service import ReportService

st.set_page_config(page_title="Relatórios - Vitrine Matriz", layout="centered")

st.title("📄 Exportação de Relatórios")
report_service = ReportService()

# --- SEÇÃO 1: RELATÓRIO DE RELEASE ---
st.subheader("📦 Notas de Versão (Release)")
rel_service = ReleaseService()
df_releases = rel_service.get_all_releases()

if not df_releases.empty:
    opcoes_rel = {row['versao']: row['id'] for _, row in df_releases.iterrows()}
    versao_sel = st.selectbox("Selecione a versão:", options=list(opcoes_rel.keys()))
    
    if st.button("Gerar PDF da Release"):
        all_tasks = rel_service.get_all_releases_with_tasks()
        tasks_release = all_tasks[all_tasks['versao'] == versao_sel]
        info_release = df_releases[df_releases['versao'] == versao_sel].iloc[0]
        
        pdf_bytes = report_service.generate_release_pdf(info_release, tasks_release)
        st.download_button("💾 Baixar PDF da Release", pdf_bytes, f"Release_{versao_sel}.pdf", "application/pdf")

st.divider()

# --- SEÇÃO 2: RELATÓRIO DE EQUIPE (NOVO) ---
st.subheader("👥 Performance da Equipe (Consolidado)")
st.write("Gera um documento com o perfil e histórico de todos os profissionais cadastrados.")

if st.button("🛠️ Preparar Relatório da Equipe"):
    dev_service = DevService()
    df_team = dev_service.get_team_stats()
    
    if df_team.empty:
        st.warning("Não há desenvolvedores cadastrados.")
    else:
        with st.spinner("Compilando dados de todos os profissionais..."):
            pdf_equipe = report_service.generate_full_team_report(df_team, dev_service)
            
            st.success("Relatório consolidado pronto!")
            st.download_button(
                label="💾 Baixar Relatório da Equipe (PDF)",
                data=pdf_equipe,
                file_name=f"Performance_Equipe_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )