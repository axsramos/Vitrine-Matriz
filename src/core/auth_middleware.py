import streamlit as st

def require_auth():
    """Bloqueia a execução da página se o usuário não estiver logado."""
    if not st.session_state.get("authenticated"):
        st.error("🚫 **Acesso Negado.**")
        st.warning("Esta área é restrita a administradores. Por favor, realize o login na página inicial.")
        
        # O st.stop() interrompe a renderização do restante da página imediatamente
        st.stop()