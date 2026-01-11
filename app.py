import streamlit as st
from pathlib import Path
from src.core.config import get_page
from src.services.dashboard_service import DashboardService
from src.services.release_service import ReleaseService

def home():
    st.title("🚀 Vitrine Matriz")
    st.subheader("Portal de Transparência e Performance")
    
    dash_service = DashboardService()
    rel_service = ReleaseService()
    stats = dash_service.get_summary_stats()

    # --- SEÇÃO 1: KPIs (Indicadores Chave) ---
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Entregas Totais", stats['total_tarefas'], delta="Tarefas")
    with col2:
        st.metric("Releases Publicadas", stats['total_releases'], delta="Versões")
    with col3:
        st.metric("Time de Devs", stats['total_devs'], delta="Especialistas")

    st.divider()

    # --- SEÇÃO 2: ATIVIDADE RECENTE ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 🗒️ Últimas Notas de Versão")
        df_rels = rel_service.get_all_releases().head(3) # Pega as 3 últimas
        if not df_rels.empty:
            for _, row in df_rels.iterrows():
                with st.expander(f"Versão {row['versao']} - {row['titulo_comunicado']}"):
                    st.write("Acesse a aba 'Notas de Versão' para detalhes completos.")
        else:
            st.info("Nenhuma release publicada ainda.")

    with col_right:
        st.markdown("### ⚡ Acesso Rápido")
        if st.button("➕ Lançar Nova Tarefa", use_container_width=True):
            st.switch_page("src/ui/pages/06_Cadastrar_Tarefa.py")
        if st.button("📦 Gerar Release", use_container_width=True):
            st.switch_page("src/ui/pages/01_Gerar_Release.py")
        if st.button("📄 Relatório PDF", use_container_width=True):
            st.switch_page("src/ui/pages/07_Relatorios.py")
    
    st.divider()

    # --- NOVA SEÇÃO: BACKLOG DE DESENVOLVIMENTO ---
    st.markdown("### 📋 Planejamento de Versões Futuras")
    
    # Definimos o caminho do arquivo Markdown
    backlog_path = Path("data/backlog.md")

    if backlog_path.exists():
        with open(backlog_path, "r", encoding="utf-8") as f:
            content = f.read()
            st.markdown(content)
    else:
        st.info("O arquivo de backlog ainda não foi criado em `data/backlog.md`.")

    st.divider()
    
    st.caption("Versão 1.0.0-beta | Desenvolvido para gestão estratégica do Portal Matriz.")
    
    
# Configuração da página
st.set_page_config(page_title="Vitrine Matriz", page_icon="🖼️", layout="wide")

# Atualizamos os caminhos adicionando 'src/' na frente
pages = {
    "Menu Principal": [
        st.Page(home, title="Boas-vindas", icon="🏠", default=True),
    ],
    "Gerenciamento": [
        st.Page(get_page("01_Gerar_Release.py"), title="Gerar Release", icon="📦"),
        st.Page(get_page("06_Cadastrar_Tarefa.py"), title="Cadastrar Tarefa", icon="➕"),
        st.Page(get_page("05_Gerenciar_Perfil.py"), title="Gerenciar Perfis", icon="⚙️"),
    ],
    "Visualização": [
        st.Page(get_page("02_Notas_de_Versao.py"), title="Notas de Versão", icon="🗒️"),
        st.Page(get_page("03_Portfolio_Equipe.py"), title="Portfólio Equipe", icon="👥"),
        st.Page(get_page("04_Detalhes_Dev.py"), title="Detalhes do Dev", icon="👤"),
        st.Page(get_page("07_Relatorios.py"), title="Relatórios PDF", icon="📄"),
    ]
}

pg = st.navigation(pages)
pg.run()