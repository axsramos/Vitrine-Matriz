import streamlit as st
from src.services.user_service import UserService
from src.core import ui_utils
from src.core.config import Config

# Configuração da página
st.set_page_config(page_title="Acesso - Vitrine Matriz", page_icon="🔑", layout="wide")

# --- CENTRALIZAÇÃO E LARGURA ---
# A proporção [1, 2, 1] cria um formulário bem largo na horizontal
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Espaçamento superior
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 1. TÍTULO E SUBTÍTULO (Baseados no Config/Env)
    # Título principal (H2) e Subtítulo (H5/Small)
    st.markdown(f"""
        <div style='text-align: center;'>
            <h2 style='margin-bottom: 0px;'>{Config.APP_TITLE}</h2>
            <p style='font-size: 1.1em; color: gray;'>{Config.APP_SUBTITLE}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. FORMULÁRIO AMPLIADO
    with st.form("login_form"):
        # st.write("### Identificação")
        
        # Inputs que se adaptam à largura da coluna central
        username = st.text_input("Usuário", placeholder="Digite seu login...")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submit = st.form_submit_button("Acessar Painel", use_container_width=True, type="primary")
        
        if submit:
            service = UserService()
            user_data = service.login(username, password)
            
            if user_data:
                profile = service.get_user_profile(user_data['UsrCod'])
                st.session_state['user'] = {**user_data, **profile}
                st.success("Acesso autorizado! Carregando...")
                st.rerun()
            else:
                st.error("Credenciais inválidas. Verifique usuário e senha.")

    # Rodapé discreto
    st.markdown(
        f"<div style='text-align: center; color: gray; font-size: 0.8em;'>"
        f"Ambiente: {Config.ENV.upper()} | Vitrine Matriz &copy; 2026"
        f"</div>", 
        unsafe_allow_html=True
    )