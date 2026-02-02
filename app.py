import streamlit as st
from src.navigation import get_navigation, sidebar_user_info

# Busca a estrutura de páginas
pages = get_navigation()

# Configura a navegação nativa do Streamlit
pg = st.navigation(pages)

# Renderiza info do usuário na sidebar (antes do menu)
sidebar_user_info()

# Executa a página selecionada
pg.run()
