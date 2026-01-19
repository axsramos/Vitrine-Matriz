import streamlit as st
import streamlit.components.v1 as components  # Import necessário para o hack do foco
from src.services.auth_service import AuthService
from src.core.ui_utils import init_page, show_error_message, show_success_message

# Inicialização
init_page(page_title="Login", icon="🔐")

st.title("🔐 Acesso ao Sistema")

# Se já estiver logado, redireciona para a Home
if 'user' in st.session_state:
    st.info(f"Você já está logado como {st.session_state['user']['name']}.")
    if st.button("Ir para o Painel"):
        st.switch_page("src/ui/pages/00_Home.py")
    st.stop()

auth_service = AuthService()

# Layout Centralizado
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Usamos st.form para capturar o "Enter" do teclado
    with st.form(key="login_form"):
        st.markdown("### Credenciais")
        
        # Inputs
        username = st.text_input("Usuário", placeholder="Seu login")
        password = st.text_input("Senha", type="password", placeholder="Sua senha")
        
        # Botão de submit (funciona com Enter)
        submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)

    # --- HACK DE AUTOFOCUS (JavaScript) ---
    # Injeta um script que busca o primeiro input de texto da página e aplica .focus()
    components.html("""
        <script>
            var input = window.parent.document.querySelectorAll("input[type='text']");
            if (input.length > 0) {
                input[0].focus();
            }
        </script>
    """, height=0, width=0)
    # --------------------------------------

    # Lógica de processamento
    if submitted:
        if not username or not password:
            show_error_message("Preencha usuário e senha.")
        else:
            success, user_data = auth_service.check_credentials(username, password)
            
            if success:
                st.session_state['user'] = user_data
                show_success_message(f"Bem-vindo, {user_data['name']}!")
                st.switch_page("src/ui/pages/00_Home.py")
            else:
                show_error_message("Usuário ou senha incorretos.")

    st.caption("Caso não tenha acesso, contate o administrador.")