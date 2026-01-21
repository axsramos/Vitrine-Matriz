import streamlit as st
import os
from src.core.ui_utils import load_avatar 
from src.core.config import Config

def render_navigation():
    # 1. Definição das Páginas (Estrutura de Menus)
    # Nota: Certifique-se de que os nomes dos arquivos físicos coincidam com estes caminhos
    pages_dict = {
        "📊 Dashboard": [
            st.Page("src/ui/pages/00_Home.py", title="Painel de Controle", icon="📈", default=True),
        ],
        "🔑 Acesso": [
            st.Page("src/ui/pages/Login.py", title="Entrar no Sistema", icon="🔓"),
        ],
        "⚙️ Operacional": [
            st.Page("src/ui/pages/06_Cadastrar_Tarefa.py", title="Gestão de Tarefas", icon="📝"),
            st.Page("src/ui/pages/01_Gerar_Release.py", title="Fechar Release", icon="📦"),
        ],
        "🔍 Consultas": [
            st.Page("src/ui/pages/02_Notas_de_Versao.py", title="Notas de Versão", icon="📜"),
            st.Page("src/ui/pages/03_Portfolio_Equipe.py", title="Time de Devs", icon="👥"),
        ],
        "🛠️ Administração": [
            st.Page("src/ui/pages/05_Gerenciar_Usuarios.py", title="Usuários", icon="👤"),
            st.Page("src/ui/pages/08_Configuracoes.py", title="Configurações", icon="🔧"),
        ]
    }

    # --- PARTE SUPERIOR DA SIDEBAR (PERFIL) ---
    with st.sidebar:
        if 'user' in st.session_state:
            user = st.session_state['user']
            
            # Busca avatar usando a lógica centralizada (database/uploads/avatars)
            # user.get('UsrPrfFto') vem do JOIN que faremos no login/perfil
            avatar_img = load_avatar(user.get('UsrPrfFto')) 
            
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                st.image(avatar_img, width=70)
            
            with col_info:
                # Usando UsrNom conforme nosso padrão PASSO 2
                full_name = user.get('UsrNom', 'Usuário')
                first_name = full_name.split()[0] if full_name else "Usuário"
                role = user.get('UsrPrm', 'user').capitalize()
                
                st.markdown(f"**{first_name}**")
                st.caption(f"🔑 {role}")
            
            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        else:
            # Estado Visitante / Logo do Sistema
            if os.path.exists(Config.LOGO_IMG):
                st.image(Config.LOGO_IMG, use_container_width=True)
            else:
                st.title("Vitrine Matriz")
            
            st.info("Efetue login para acessar as ferramentas.")

        st.divider()

        # --- RENDERIZAÇÃO DO MENU DINÂMICO ---
        # Filtra quais menus aparecem dependendo do nível de acesso (UsrPrm)
        filtered_pages = {}
        user_role = st.session_state.get('user', {}).get('UsrPrm', None)

        for section, pages in pages_dict.items():
            # Regra simples: Apenas Admin vê a seção "Administração"
            if section == "🛠️ Administração" and user_role != 'admin':
                continue
            
            # Oculta seção de Login se já estiver logado
            if section == "🔑 Acesso" and user_role is not None:
                continue
                
            filtered_pages[section] = pages

        # Registra a navegação no Streamlit
        pg = st.navigation(filtered_pages)
        pg.run()