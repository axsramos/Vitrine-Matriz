import streamlit as st
from src.services.user_service import UserService
from src.core.config import Config

# Configuração da página (Deve ser a primeira instrução Streamlit)
st.set_page_config(
    page_title=f"Acesso | {Config.APP_TITLE}", 
    page_icon="🔑", 
    layout="wide"
)

# Nota: Não usamos require_auth() aqui, pois é a tela pública.

# --- ESTILIZAÇÃO E LAYOUT ---
# Centralização: Colunas [1, 2, 1] deixam o formulário no centro com boa largura
col_esq, col_centro, col_dir = st.columns([1, 2, 1])

with col_centro:
    # Espaçamento superior para não colar no topo
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 1. CABEÇALHO (Identidade Visual)
    st.markdown(f"""
        <div style='text-align: center;'>
            <h2 style='margin-bottom: 0px;'>{Config.APP_TITLE}</h2>
            <p style='font-size: 1.1em; color: gray;'>{Config.APP_SUBTITLE}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. FORMULÁRIO DE LOGIN
    with st.form("login_form"):
        # Inputs simples e diretos
        username = st.text_input("Usuário", placeholder="Digite seu login...")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão de Ação (Primary para destaque)
        submit = st.form_submit_button("Acessar Painel", use_container_width=True, type="primary")
        
        if submit:
            service = UserService()
            
            # Chama o serviço (agora retorna Tupla: sucesso, dados_usuario)
            is_authenticated, user_data = service.login(username, password)
            
            if is_authenticated and user_data:
                # Busca dados complementares do perfil (Cargo, Foto, etc.)
                # Nota: Método renomeado de get_user_profile para get_profile
                profile_data = service.get_profile(user_data['UsrCod'])
                
                # Consolida os dados na Sessão
                session_data = {**user_data, **profile_data}
                
                # IMPORTANTE: Mapeamento para o SessionHelper funcionar na Auditoria
                # O Helper busca 'login', mas o banco traz 'UsrLgn'
                session_data['login'] = user_data['UsrLgn']
                
                st.session_state['user'] = session_data
                
                st.toast("Login realizado com sucesso!", icon="✅")
                st.success("Redirecionando...")
                st.rerun()
            else:
                st.error("Credenciais inválidas. Verifique usuário e senha.")

    # Rodapé discreto
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; font-size: 0.8em; color: #888;'>
            &copy; Vitrine de Matriz - Acesso Restrito
        </div>
    """, unsafe_allow_html=True)