import streamlit as st
from src.services.user_service import UserService
from src.core import ui_utils
from src.core.config import Config

# Configuração da página (Login geralmente não usa o menu completo antes de logar)
st.set_page_config(page_title="Login - Vitrine Matriz", page_icon="🔑")

# Centralização visual
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Exibe Logo parametrizado
    ui_utils.display_logo()
    
    st.title("Acesso ao Sistema")
    
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu login")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submit = st.form_submit_button("Entrar", use_container_width=True, type="primary")
        
        if submit:
            service = UserService()
            user_data = service.login(username, password)
            
            if user_data:
                # 1. Busca dados do perfil para enriquecer a sessão (Foto, Cargo)
                profile = service.get_user_profile(user_data['UsrCod'])
                
                # 2. Consolida dados na sessão (Padrão Usr...)
                # Mesclamos os dados básicos com os do perfil
                st.session_state['user'] = {**user_data, **profile}
                
                st.success(f"Bem-vindo, {user_data['UsrNom']}!")
                st.rerun() # Redireciona para a Home automaticamente via navigation
            else:
                st.error("Usuário ou senha inválidos.")

    st.caption(f"Configuração: {Config.ENV.upper()} Mode")