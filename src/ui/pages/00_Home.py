import streamlit as st
from src.services.dashboard_service import DashboardService
from src.core.ui_utils import show_info_message

# Não precisamos de init_page aqui, pois o app.py já fará isso
st.markdown("# 📊 Painel de Controle")

# --- Navegação Rápida (Tiles) ---
# Agora que as páginas serão registradas no app.py, estes links funcionarão!
cols = st.columns(3)
with cols[0]:
    st.page_link("src/ui/pages/01_Gerar_Release.py", label="Gerar Release", icon="📦")
    st.page_link("src/ui/pages/02_Notas_de_Versao.py", label="Notas de Versão", icon="📜")
    st.page_link("src/ui/pages/03_Portfolio_Equipe.py", label="Portfólio", icon="👥")

with cols[1]:
    st.page_link("src/ui/pages/04_Detalhes_Dev.py", label="Detalhes Dev", icon="🕵️")
    st.page_link("src/ui/pages/05_Gerenciar_Perfil.py", label="Meu Perfil", icon="👤")
    st.page_link("src/ui/pages/06_Cadastrar_Tarefa.py", label="Nova Tarefa", icon="📝")

with cols[2]:
    st.page_link("src/ui/pages/07_Relatorios.py", label="Relatórios", icon="📈")
    st.page_link("src/ui/pages/08_Gerenciar_Usuarios.py", label="Usuários", icon="🔐")
    st.page_link("src/ui/pages/09_Alterar_Senha.py", label="Segurança", icon="🛡️")

st.markdown("---")

# --- Lógica do Dashboard ---
dash_service = DashboardService()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Evolução de Entregas (30 dias)")
    df_evolucao = dash_service.get_tasks_evolution(30)
    
    if not df_evolucao.empty:
        st.line_chart(df_evolucao.set_index('Data'))
    else:
        show_info_message("Sem dados de evolução recentes.")

with col2:
    st.subheader("Distribuição por Impacto")
    df_impacto = dash_service.get_impact_distribution()
    
    if not df_impacto.empty:
        st.dataframe(
            df_impacto, 
            column_config={
                "Impacto": "Nível",
                "Total": st.column_config.ProgressColumn("Qtd", format="%d", min_value=0, max_value=int(df_impacto['Total'].max()))
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Nenhuma tarefa registrada.")

# --- Últimas Releases ---
st.subheader("Últimas Releases Publicadas")
df_releases = dash_service.get_latest_releases()

if not df_releases.empty:
    for _, row in df_releases.iterrows():
        # Tratamento seguro de Data
        data_val = row['Data']
        data_fmt = data_val
        if hasattr(data_val, 'strftime'):
            data_fmt = data_val.strftime('%d/%m/%Y')
        else:
            data_fmt = str(data_val)[:10]
            
        st.markdown(f"**v{row['Versao']}** - {row['Titulo']} _({data_fmt})_")
else:
    st.caption("Nenhuma release encontrada.")