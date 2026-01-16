import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
from src.core import config
from src.services.dashboard_service import DashboardService
from src.services.release_service import ReleaseService
from src.services.auth_service import AuthService
from src.core.ui_utils import init_page

init_page("Login", "wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None

def home():
    st.title(config.APP_TITLE)
    st.subheader(config.APP_SUBTITLE)
    
    dash_service = DashboardService()
    rel_service = ReleaseService()

    # 1. Interface de Filtros
    st.markdown("### 📅 Filtros de Análise")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        # Padrão: últimos 30 dias
        data_ini = st.date_input("Início", datetime.now() - timedelta(days=30))
    with col_f2:
        data_fim = st.date_input("Fim", datetime.now())
    
    # 2. Carregamento de Dados Filtrados
    dash_service = DashboardService()
    df_impacto = dash_service.get_impact_distribution(data_ini, data_fim)

    # --- SEÇÃO 1: KPIs (Indicadores Chave) ---
    stats = dash_service.get_summary_stats(data_ini, data_fim)
    
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

    # --- SEÇÃO 3: 
    if not df_impacto.empty:
        # Mapeamento de cores para manter a identidade visual
        cores_map = {
            "Crítico": "#EF553B", # Vermelho
            "Alto": "#FFA15A",    # Laranja
            "Médio": "#636EFA",   # Azul
            "Baixo": "#AB63FA"    # Roxo/Cinza
        }

        # Criando o gráfico com Plotly
        fig = px.pie(
            df_impacto, 
            values='total', 
            names='impacto', 
            title="Distribuição de Valor de Negócio (Impacto)",
            color='impacto',
            color_discrete_map=cores_map,
            hole=0.4 # Transforma em gráfico de rosca
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ainda não há tarefas cadastradas para gerar o gráfico de impacto.")

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
    
    st.caption("Versão 0.3.0-beta | Desenvolvido para gestão estratégica do Portal Matriz.")

def login_page():
    # Centralizando o formulário na tela
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.write("### Identifique-se")
            user_input = st.text_input("Usuário")
            pass_input = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                auth = AuthService()
                user = auth.check_login(user_input, pass_input)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success("Login realizado!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")

def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

pages = {}

public_list = [
    st.Page("src/ui/pages/02_Notas_de_Versao.py", title="Notas de Versão", icon="🗒️"),
    st.Page("src/ui/pages/03_Portfolio_Equipe.py", title="Portfólio Equipe", icon="👥")
]

if st.session_state.authenticated:
    pages["Dashboard"] = [st.Page(home, title="Home", icon="🏠")]
    pages["Consulta"] = public_list
    pages["Gerenciamento"] = [
        st.Page("src/ui/pages/01_Gerar_Release.py", title="Gerar Release", icon="📦"),
        st.Page("src/ui/pages/06_Cadastrar_Tarefa.py", title="Cadastrar Tarefa", icon="➕"),
        st.Page("src/ui/pages/07_Relatorios.py", title="Relatórios PDF", icon="📄"),
        st.Page("src/ui/pages/08_Gerenciar_Usuarios.py", title="Gerenciar Usuários", icon="👥")
    ]
    pages["Conta"] = [
        st.Page("src/ui/pages/09_Alterar_Senha.py", title="Alterar Senha", icon="🔑"),
        st.Page(logout, title="Sair", icon="🚪")
    ]
else:
    pages["Início"] = [st.Page(home, title="Boas-vindas", icon="🏠")]
    pages["Consulta Pública"] = public_list
    pages["Admin"] = [st.Page(login_page, title="Login", icon="🔐")]

# 4. Execução da Navegação
pg = st.navigation(pages)
pg.run()

