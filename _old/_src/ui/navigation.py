import streamlit as st
import os
# Certifique-se de que a função load_avatar está no ui_utils.py
from src.core.ui_utils import load_avatar 

def render_navigation():
    # 1. Definição das Páginas
    pages_dict = {
        "Principal": [
            st.Page("src/ui/pages/00_Home.py", title="Painel de Controle", icon="📊", default=True),
        ],
        "Acesso": [
            st.Page("src/ui/pages/Login.py", title="Login", icon="🔑"),
        ],
        "Operacional": [
            st.Page("src/ui/pages/01_Gerar_Release.py", title="Gerar Release", icon="📦"),
            st.Page("src/ui/pages/06_Cadastrar_Tarefa.py", title="Nova Tarefa", icon="📝"),
        ],
        "Consulta": [
            st.Page("src/ui/pages/02_Notas_de_Versao.py", title="Notas de Versão", icon="📜"),
            st.Page("src/ui/pages/03_Portfolio_Equipe.py", title="Portfólio", icon="👥"),
            st.Page("src/ui/pages/04_Detalhes_Dev.py", title="Detalhes Dev", icon="🕵️"),
        ],
        "Gestão": [
            st.Page("src/ui/pages/07_Relatorios.py", title="Relatórios", icon="📈"),
            st.Page("src/ui/pages/08_Gerenciar_Usuarios.py", title="Usuários", icon="🔐"),
        ],
        "Configuração": [
            st.Page("src/ui/pages/05_Gerenciar_Perfil.py", title="Meu Perfil", icon="👤"),
            st.Page("src/ui/pages/09_Alterar_Senha.py", title="Segurança", icon="🛡️"),
        ]
    }

    pg = st.navigation(pages_dict, position="hidden")

    with st.sidebar:
        # --- PARTE SUPERIOR: Identidade ---
        if 'user' in st.session_state:
            user = st.session_state['user']
            
            # CORREÇÃO DO ERRO: 
            # Em vez de verificar if path exists manualmente, chamamos a função que trata tudo
            avatar_img = load_avatar(user.get('UsrFto')) 
            
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                st.image(avatar_img, width=80)
            
            with col_info:
                # Tratamento para exibir apenas o primeiro nome
                nome = user.get('name', 'Usuário')
                primeiro_nome = nome.split()[0] if nome else "Usuário"
                st.write(f"Olá,\n**{primeiro_nome}**")
            
            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()
                
        else:
            # Visitante
            st.image("assets/logo.png", width=120)
            st.write("**Visitante**")
            if st.button("🔑 Login", use_container_width=True):
                st.switch_page("src/ui/pages/Login.py")

        st.markdown("---")

        # --- PARTE INFERIOR: Menu ---
        for section_name, pages in pages_dict.items():
            # Oculta Login se já estiver logado
            if section_name == "Acesso" and 'user' in st.session_state:
                continue

            st.caption(section_name.upper())
            for page in pages:
                st.page_link(page, label=page.title, icon=page.icon)
                
    return pg