import streamlit as st
from src.core.ui_utils import init_page

# 1. Configuração Global
init_page(page_title="Vitrine Matriz", icon="🚀")

# Inicializa as variáveis se elas não existirem
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. Definição da Estrutura de Navegação
pages = {
    "Principal": [
        st.Page("src/ui/pages/00_Home.py", title="Painel de Controle", icon="📊", default=True),
    ],
    "Acesso": [ # Nova Seção
        st.Page("src/ui/pages/Login.py", title="Login", icon="🔑"),
    ],
    "Operacional": [
        st.Page("src/ui/pages/01_Gerar_Release.py", title="Gerar Release", icon="📦"),
        st.Page("src/ui/pages/06_Cadastrar_Tarefa.py", title="Nova Tarefa", icon="📝"),
    ],
    "Consulta": [
        st.Page("src/ui/pages/02_Notas_de_Versao.py", title="Notas de Versão", icon="📜"),
        st.Page("src/ui/pages/03_Portfolio_Equipe.py", title="Portfólio", icon="👥"),
        st.Page("src/ui/pages/04_Detalhes_Dev.py", title="Detalhes Dev", icon="🕵️"),
    ],
    "Gestão": [
        st.Page("src/ui/pages/07_Relatorios.py", title="Relatórios", icon="📈"),
        st.Page("src/ui/pages/08_Gerenciar_Usuarios.py", title="Usuários", icon="🔐"),
    ],
    "Configuração": [
        st.Page("src/ui/pages/05_Gerenciar_Perfil.py", title="Meu Perfil", icon="👤"),
        st.Page("src/ui/pages/09_Alterar_Senha.py", title="Segurança", icon="🛡️"),
    ]
}

# 3. Sidebar Global
with st.sidebar:
    # st.image("https://via.placeholder.com/150?text=Logo+Matriz", use_container_width=True)
    st.image("https://api.dicebear.com/7.x/initials/svg?seed=Logo+Matriz", use_container_width=True)
    
    # Verifica Autenticação
    if 'user' in st.session_state:
        user = st.session_state['user']
        st.success(f"Olá, {user['name']}!")
        if st.button("Sair"):
            del st.session_state['user']
            st.rerun()
    else:
        st.info("Visitante")
        if st.button("Fazer Login"):
            # AGORA APONTA PARA A PÁGINA CORRETA
            st.switch_page("src/ui/pages/Login.py")

# 4. Executa Navegação
pg = st.navigation(pages)
pg.run()