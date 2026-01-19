import streamlit as st
from src.services.auth_service import AuthService
from src.core.auth_middleware import require_auth

st.set_page_config(page_title="Alterar Senha")
require_auth() # Protege a página

st.title("🔒 Alterar Senha")

auth_service = AuthService()
user_session = st.session_state.get('user', {})
current_user = user_session.get('username')

if not current_user:
    st.error("Sessão inválida. Faça login novamente.")
    st.stop()

st.info(f"Alterando senha para: **{current_user}**")

with st.form("form_change_pass"):
    new_pass = st.text_input("Nova Senha", type="password")
    confirm_pass = st.text_input("Confirme a Nova Senha", type="password")
    
    submitted = st.form_submit_button("Atualizar Senha")
    
    if submitted:
        if new_pass != confirm_pass:
            st.error("As senhas não coincidem.")
        elif not new_pass:
            st.error("A senha não pode ser vazia.")
        else:
            success, msg = auth_service.change_password(current_user, new_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)