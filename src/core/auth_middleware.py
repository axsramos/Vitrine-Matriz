import streamlit as st

def require_auth(allowed_roles=None):
    """
    Protege o conteúdo da página sem redirecionar forçadamente,
    mantendo a estrutura do menu lateral intacta.
    """
    if 'user' not in st.session_state:
        st.title("🔒 Conteúdo Privado")
        st.warning("Esta funcionalidade é restrita a membros da equipe.")
        st.info("Por favor, utilize o botão de **Login** no menu lateral para acessar.")
        
        # O stop() impede que o restante da página (form, dados, etc) seja carregado
        st.stop() 

    if allowed_roles:
        user_role = st.session_state['user'].get('UsrPrm', 'user')
        if user_role not in allowed_roles:
            st.error("⛔ Você não tem permissão para acessar esta área.")
            st.stop()