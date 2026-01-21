import streamlit as st

def require_auth(allowed_roles=None):
    """
    Middleware para proteger páginas.
    Verifica se o usuário está logado e valida a permissão UsrPrm.
    """
    # 1. Verifica se existe sessão de usuário
    if 'user' not in st.session_state:
        st.warning("⚠️ Acesso restrito. Por favor, faça login para continuar.")
        
        # Centralizando o redirecionamento para a raiz (Login)
        if st.button("Ir para Login"):
            st.switch_page("app.py") # Geralmente o app.py gerencia o roteamento inicial
        
        st.stop()

    # 2. Verifica permissão baseada no novo campo UsrPrm
    if allowed_roles:
        current_user = st.session_state['user']
        # Ajustado de 'role' para 'UsrPrm' conforme o PASSO 2 da revisão
        user_role = current_user.get('UsrPrm', 'user') 
        
        if user_role not in allowed_roles:
            st.error(f"⛔ Acesso Negado. Requer perfil: {', '.join(allowed_roles)}")
            st.stop()