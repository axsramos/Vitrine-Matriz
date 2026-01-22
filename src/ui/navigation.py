import streamlit as st
from src.core.config import Config

def render_navigation():
    # 1. Identifica o estado do usuário na sessão
    user = st.session_state.get('user')
    user_role = user.get('UsrPrm') if user else None

    # --- PARTE 1: Identidade e Sessão (Topo) ---
    with st.sidebar:
        if user:
            # Pega o primeiro nome do usuário
            nome_completo = user.get('UsrNom', 'Usuário')
            primeiro_nome = nome_completo.split()[0]
            
            st.write(f"👋 Olá, **{primeiro_nome}**")
            st.caption(f"Perfil: {user_role.capitalize()}")
            
            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        else:
            st.write("👋 Bem-vindo, **Visitante**")
            st.caption("Acesse sua conta para gerenciar tarefas.")
            
            if st.button("🔑 Login", use_container_width=True, type="primary"):
                # Se a página de Login não estiver no menu fixo, você pode usar switch_page
                st.switch_page("src/ui/pages/Login.py")

        st.divider()

    # --- PARTE 2: Estrutura do Menu ---
    # Páginas Públicas (Sempre visíveis)
    nav_structure = {
        "📊 Dashboard": [
            # st.Page("src/ui/pages/00_Home.py", title="Visão Geral", icon="🏠", default=True),
            st.Page("src/ui/pages/01_Dashboard.py", title="Dashboard", icon="🏠", default=True),
        ],
        "🔍 Consultas": [
            st.Page("src/ui/pages/02_Notas_de_Versao.py", title="Notas de Versão", icon="📜"),
            st.Page("src/ui/pages/03_Portfolio_Equipe.py", title="Time de Devs", icon="👥"),
        ]
    }

    # Páginas Privadas (Apenas para logados)
    if user:
        nav_structure["⚙️ Operacional"] = [
            st.Page("src/ui/pages/06_Cadastrar_Tarefa.py", title="Gestão de Tarefas", icon="📝"),
            st.Page("src/ui/pages/01_Gerar_Release.py", title="Gerar Release", icon="📦"),
        ]
        
        nav_structure["👤 Minha Conta"] = [
            st.Page("src/ui/pages/04_Perfil_Usuario.py", title="Meu Perfil", icon="👤"),
        ]

        if user_role == 'admin':
            nav_structure["🛠️ Administração"] = [
                st.Page("src/ui/pages/05_Gerenciar_Usuarios.py", title="Usuários", icon="👥"),
                st.Page("src/ui/pages/08_Configuracoes.py", title="Configurações", icon="🔧"),
            ]
    else:
        # Se visitante, garante que o Login esteja no menu para navegação fluida
        nav_structure["🔑 Acesso"] = [
            st.Page("src/ui/pages/Login.py", title="Entrar no Sistema", icon="🔓")
        ]

    # --- PASSO 3: Retorno do Objeto ---
    return st.navigation(nav_structure)