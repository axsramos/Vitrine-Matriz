import streamlit as st
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.core.auth_middleware import require_auth
from src.core.ui_utils import init_page

# Proteção da página
require_auth()
init_page("Alterar Senha")

st.title("🔑 Alterar Minha Senha")

user_info = st.session_state.user # Dados do usuário logado
service = UserService()
auth_service = AuthService()

with st.form("form_alterar_senha"):
    senha_atual = st.text_input("Senha Atual", type="password")
    nova_senha = st.text_input("Nova Senha", type="password")
    confirma_senha = st.text_input("Confirme a Nova Senha", type="password")
    
    if st.form_submit_button("Atualizar Senha", use_container_width=True):
        # 1. Valida a senha atual
        if not auth_service.check_login(user_info['username'], senha_atual):
            st.error("A 'Senha Atual' está incorreta.")
        # 2. Valida se as novas são iguais
        elif nova_senha != confirma_senha:
            st.warning("A nova senha e a confirmação não conferem.")
        # 3. Valida tamanho mínimo (exemplo de boa prática)
        elif len(nova_senha) < 6:
            st.warning("A nova senha deve ter pelo menos 6 caracteres.")
        else:
            service.update_password(user_info['id'], nova_senha)
            st.success("Senha alterada com sucesso!")