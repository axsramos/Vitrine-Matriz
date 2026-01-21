import streamlit as st
import plotly.express as px
import pandas as pd
from src.services.dashboard_service import DashboardService
from src.services.release_service import ReleaseService
from src.core.config import Config
from src.core.auth_middleware import require_auth

# Proteção de acesso
require_auth()

# Inicialização de Serviços
dash_service = DashboardService()
rel_service = ReleaseService()

# --- HEADER ---
st.title(f"📊 {Config.APP_TITLE}")
st.caption(Config.APP_SUBTITLE)

# --- 1. INDICADORES DE TOPO (KPIs) ---
# Buscamos dados para os indicadores
df_status = dash_service.get_task_status_distribution()
df_releases = rel_service.get_all_releases()

# Lógica para Versão Atual e Última Pub
v_atual = df_releases.iloc[0]['RelVrs'] if not df_releases.empty else "N/A"
u_pub = df_releases.iloc[0]['RelDat'] if not df_releases.empty else "N/A"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Versão Atual", v_atual, delta="Estável", delta_color="normal")
with col2:
    total_tasks = df_status['Quantidade'].sum() if not df_status.empty else 0
    st.metric("Total de Tasks", total_tasks, delta="Backlog", delta_color="off")
with col3:
    concluidas = df_status[df_status['Status'] == 'Concluído']['Quantidade'].sum() if not df_status.empty else 0
    # Cálculo simples de performance (apenas ilustrativo para o layout)
    st.metric("Concluídas", concluidas, delta="↑ 12%", delta_color="normal")
with col4:
    st.metric("Última Publicação", str(u_pub), delta="📅")

st.divider()

# --- 2. VISÃO ESTRATÉGICA (GRÁFICOS) ---
row1_col1, row1_col2 = st.columns([1.2, 0.8])

with row1_col1:
    st.subheader("📈 Produtividade por Desenvolvedor")
    df_dev = dash_service.get_dev_workload()
    if not df_dev.empty:
        fig_dev = px.bar(
            df_dev, 
            x='Desenvolvedor', 
            y='Tarefas', 
            color='Tarefas',
            color_continuous_scale='Viridis',
            text_auto=True
        )
        fig_dev.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350)
        st.plotly_chart(fig_dev, use_container_width=True)
    else:
        st.info("Aguardando vínculo de tarefas a desenvolvedores.")

with row1_col2:
    st.subheader("🎯 Status Geral")
    if not df_status.empty:
        fig_pie = px.pie(
            df_status, 
            values='Quantidade', 
            names='Status', 
            hole=.5,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=350, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- 3. TENDÊNCIAS E ENTREGAS ---
st.subheader("📅 Totalização de Entregas por Mês")
# Exemplo de consulta que você pode adicionar ao seu DashboardService
# sql = "SELECT strftime('%Y-%m', TrfAudIns) as Mes, COUNT(*) as Total FROM T_Trf GROUP BY Mes"
# Aqui simulamos o DataFrame para visualização do layout:
df_mensal = pd.DataFrame({
    "Mês": ["Jan/26", "Fev/26", "Mar/26", "Abr/26"],
    "Entregas": [12, 18, 15, 25] # Exemplo
})

fig_line = px.area(
    df_mensal, 
    x="Mês", 
    y="Entregas", 
    markers=True,
    line_shape="spline",
    color_discrete_sequence=['#00CC96']
)
fig_line.update_layout(height=300)
st.plotly_chart(fig_line, use_container_width=True)

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"© 2026 Vitrine Matriz - Versão do Sistema: {v_atual} | Ambiente: {Config.ENV.upper()}")