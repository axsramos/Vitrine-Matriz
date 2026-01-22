import streamlit as st
import altair as alt
import pandas as pd
from src.services.dashboard_service import DashboardService
from src.core.auth_middleware import require_auth

st.set_page_config(page_title="Dashboard | Vitrine", layout="wide")
# require_auth()

st.title("📊 Painel de Controle")

dash = DashboardService()

# --- 1. INFO DA VERSÃO (HEADER CORRIGIDO) ---
# O serviço agora retorna chaves baseadas no banco: RelVrs e RelDat
last_rel = dash.get_ultima_release()

# Tratamento para evitar erro se vier nulo
versao_txt = last_rel.get('RelVrs', 'N/A')
data_txt = last_rel.get('RelDat', 'N/A')

st.markdown(f"""
<div style='background-color: #ccc; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
    🚀 <b>Versão em Produção:</b> {versao_txt} 
    <span style='float:right; color: #666;'>📅 Publicado em: {data_txt}</span>
</div>
""", unsafe_allow_html=True)

# --- 2. INDICADORES MACRO ---
kpis = dash.get_kpis_gerais()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Tarefas", kpis['total'])
col2.metric("Conclusão", f"{kpis['percentual']}%")
col3.metric("Entregues", kpis['concluidas'])
col4.metric("🚨 Em Atraso", kpis['atrasadas'], delta=-kpis['atrasadas'], delta_color="inverse")

st.divider()

# --- 3. GRÁFICOS ---
c_chart1, c_chart2 = st.columns(2)

with c_chart1:
    st.subheader("📌 Status das Atividades")
    df_status = dash.get_tarefas_por_status()
    
    if not df_status.empty:
        base = alt.Chart(df_status).encode(theta=alt.Theta("Quantidade", stack=True))
        pie = base.mark_arc(outerRadius=100, innerRadius=60).encode(
            color=alt.Color("Status", scale=alt.Scale(scheme='category20b')),
            order=alt.Order("Quantidade", sort="descending"),
            tooltip=["Status", "Quantidade"]
        )
        text = base.mark_text(radius=130).encode(
            text=alt.Text("Quantidade"),
            order=alt.Order("Quantidade", sort="descending"),
            color=alt.value("black")  
        )
        st.altair_chart(pie + text, use_container_width=True)
    else:
        st.info("Sem dados para exibir.")

with c_chart2:
    st.subheader("⚖️ Carga de Trabalho (Pendentes)")
    df_workload = dash.get_carga_trabalho_devs()
    
    if not df_workload.empty:
        bar = alt.Chart(df_workload).mark_bar().encode(
            x=alt.X('Tarefas', title='Qtd Pendente'),
            y=alt.Y('Desenvolvedor', sort='-x'),
            color=alt.value('#4c78a8'),
            tooltip=['Desenvolvedor', 'Tarefas']
        ).properties(height=300)
        st.altair_chart(bar, use_container_width=True)
    else:
        st.caption("Nenhum desenvolvedor com tarefas pendentes.")

# --- 4. TABELA DE RISCO ---
if kpis['atrasadas'] > 0:
    st.divider()
    st.error(f"🔥 Atenção: Existem {kpis['atrasadas']} tarefas com prazo estourado!")
    
    lista_atrasos = dash.get_tarefas_atrasadas_detalhe()
    df_atrasos = pd.DataFrame(lista_atrasos)
    
    st.dataframe(
        df_atrasos,
        column_config={
            "TrfTtl": "Tarefa",
            "TrfDatEnt": st.column_config.DateColumn("Prazo Original", format="DD/MM/YYYY"),
            "DevNom": "Responsável",
            "TrfPrio": "Prioridade"
        },
        hide_index=True,
        use_container_width=True
    )