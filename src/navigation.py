import streamlit as st
from src.models.UserRole import UserRole

def get_navigation():
    """
    Define a estrutura de navegação baseada no estado da sessão (Logado/Visitante)
    e nas permissões (Role) do usuário.
    """
    
    # 1. Recupera contexto do usuário
    user = st.session_state.get('user')
    user_role = user.get('UsrPrm') if user else None

    # Dicionário que armazena as páginas por Categoria
    pages = {}

    # --- SEÇÃO 1: PÚBLICO / GERAL (Visível para todos ou Auth opcional) ---
    # Nota: Dashboard e Notas geralmente são públicos ou a landing page
    pages["Visão Geral"] = [
        st.Page("src/ui/pages/00_Home.py", title="Início", icon="🏠", default=True),
        st.Page("src/ui/pages/01_Dashboard.py", title="Painel de Controle", icon="🏠"),
        st.Page("src/ui/pages/02_Notas_de_Versao.py", title="Notas de Versão", icon="📜"),
        st.Page("src/ui/pages/03_Portfolio_Equipe.py", title="Time de Devs", icon="👥"),
    ]

    # --- SEÇÃO 2: ACESSO (Apenas se NÃO estiver logado) ---
    if not user:
        pages["Conta"] = [
            st.Page("src/ui/pages/Login.py", title="Acesso ao Sistema", icon="🔑")
        ]

    # --- SEÇÃO 3: ÁREA LOGADA (Apenas se ESTIVER logado) ---
    if user:
        # 3.1 Operacional (Dia a dia)
        ops_pages = [
            st.Page("src/ui/pages/06_Cadastrar_Tarefa.py", title="Gestão de Tarefas", icon="📝"),
            st.Page("src/ui/pages/04_Relatorios.py", title="Relatórios", icon="📊"), # Movemos para cá pois tem require_auth
        ]

        # Regra: 'Gerar Release' apenas para Admin, Manager ou Dev
        if user_role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.DEVELOPMENT]:
            ops_pages.append(
                st.Page("src/ui/pages/01_Gerar_Release.py", title="Gerar Release", icon="📦")
            )
        
        pages["Operacional"] = ops_pages

        # 3.2 Minha Conta
        pages["Minha Conta"] = [
            st.Page("src/ui/pages/04_Perfil_Usuario.py", title="Meu Perfil", icon="👤")
        ]

        # 3.3 Administração (Apenas Admin)
        if user_role == UserRole.ADMIN:
            pages["Administração"] = [
                st.Page("src/ui/pages/05_Gerenciar_Usuarios.py", title="Gerenciar Usuários", icon="🛡️"),
                st.Page("src/ui/pages/08_Configuracoes.py", title="Configurações", icon="⚙️")
            ]

    return pages

def sidebar_user_info():
    """Renderiza o cartão de usuário no topo da sidebar (opcional)."""
    user = st.session_state.get('user')
    if user:
        st.sidebar.markdown(f"**Olá, {user.get('UsrNom', 'Usuário').split()[0]}!**")
        st.sidebar.caption(f"Perfil: {user.get('UsrPrm', '').upper()}")
        
        if st.sidebar.button("Sair / Logout", icon="🚪", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    else:
        st.sidebar.info("Você está navegando como visitante.")
        # Botão de atalho para login se estiver longe do menu
        # if st.sidebar.button("Fazer Login"):
        #     st.switch_page("src/ui/pages/Login.py")