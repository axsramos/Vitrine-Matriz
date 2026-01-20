import streamlit as st
from src.core.ui_utils import init_page
from src.ui.navigation import render_navigation

# 1. Configuração Global (Sempre o primeiro comando)
init_page(page_title="Vitrine Matriz", icon="🚀")

# 2. Inicialização do Estado da Sessão
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. Executa a Navegação Centralizada
pg = render_navigation()
pg.run()