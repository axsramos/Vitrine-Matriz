import streamlit as st
import pandas as pd
from src.services.report_service import ReportService
from src.core.auth_middleware import require_auth

st.set_page_config(page_title="Relatórios Gerenciais")
require_auth()

st.title("📊 Relatórios e Métricas")
st.markdown("---")

service = ReportService()

# Layout de Dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tarefas por Impacto")
    df_impact = service.get_tasks_by_impact()
    if not df_impact.empty:
        st.bar_chart(df_impact)
    else:
        st.info("Sem dados de impacto.")

with col2:
    st.subheader("Produtividade por Dev")
    df_dev = service.get_tasks_by_developer()
    if not df_dev.empty:
        st.bar_chart(df_dev)
    else:
        st.info("Sem dados de desenvolvedores.")

st.markdown("---")

st.subheader("Distribuição por Release")
df_rel = service.get_tasks_by_release()
if not df_rel.empty:
    st.bar_chart(df_rel, horizontal=True) # Gráfico horizontal fica melhor aqui
else:
    st.info("Sem dados de releases.")