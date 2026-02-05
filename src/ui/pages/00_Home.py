import streamlit as st
import os
from src.core.config import Config

# Configuração da Página (Sem sidebar expandida inicialmente para focar no conteúdo)
st.set_page_config(
    page_title=f"Bem-vindo | {Config.APP_TITLE}",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def render_home():
    # Espaçamento vertical para não colar no topo
    st.write("")
    st.write("")

    # Layout Centralizado: Coluna Vazia | Conteúdo | Coluna Vazia
    # A proporção [1, 2, 1] garante que o conteúdo ocupe 50% da tela no meio
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        # 1. LOGO
        # Verifica se o arquivo existe para evitar erro feio na tela
        logo_path = "assets/logo.png"
        
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            # Placeholder caso a imagem não seja encontrada
            st.warning(f"Logo não encontrada em: {logo_path}")
            st.image("https://placehold.co/600x400?text=Logo+Vitrine", use_container_width=True)

        # 2. TÍTULOS CENTRALIZADOS
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 20px;">
                <h1 style="font-size: 3rem; margin-bottom: 0;">{Config.APP_TITLE}</h1>
                <h3 style="font-weight: 300; color: gray; margin-top: 5px;">
                    {getattr(Config, 'APP_SUBTITLE', 'Sistema de Gestão')}
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.divider()

        # 3. BOTÕES DE AÇÃO (Call to Action)
        # Verifica se já está logado para mostrar o botão certo
        user = st.session_state.get('user')
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            if user:
                # Se logado -> Botão para Dashboard
                st.info(f"Você está logado como **{user.get('UsrNom')}**")
                if st.button("🚀 Acessar Painel de Controle", type="primary", use_container_width=True):
                    st.switch_page("src/ui/pages/01_Dashboard.py")
            else:
                # Se deslogado -> Botão para Login
                if st.button("🔐 Acessar Sistema / Login", type="primary", use_container_width=True):
                    st.switch_page("src/ui/pages/Login.py")
                
                # Link secundário para Portfolio público
                if st.button("👥 Ver Time de Desenvolvedores", use_container_width=True):
                    st.switch_page("src/ui/pages/03_Portfolio_Equipe.py")

# Executa a renderização
render_home()