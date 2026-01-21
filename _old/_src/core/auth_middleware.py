import streamlit as st

def require_auth(allowed_roles=None):
    """
    Middleware para proteger páginas.
    Verifica se o usuário está logado e, opcionalmente, se tem o cargo necessário.
    
    Args:
        allowed_roles (list): Lista de perfis permitidos (ex: ['Admin', 'Manager']).
                              Se None, apenas verifica se está logado.
    """
    # 1. Verifica se existe sessão de usuário
    if 'user' not in st.session_state:
        st.warning("⚠️ Acesso restrito. Por favor, faça login para continuar.")
        
        # --- CORREÇÃO AQUI ---
        # Antes apontava para 09_Alterar_Senha.py, agora aponta para Login.py
        if st.button("Ir para Login"):
            st.switch_page("src/ui/pages/Login.py")
        # ---------------------
        
        st.stop() # Interrompe a renderização da página protegida

    # 2. Verifica permissão de Role (se especificado)
    if allowed_roles:
        current_user = st.session_state['user']
        user_role = current_user.get('role', 'User') # Padrão 'User' se não tiver
        
        if user_role not in allowed_roles:
            st.error(f"⛔ Acesso Negado. Esta página requer perfil: {', '.join(allowed_roles)}")
            st.stop()

def get_current_user():
    """Retorna o usuário da sessão ou None"""
    return st.session_state.get('user')