import streamlit as st
import os
from PIL import Image

# Imports do sistema
from src.core import ui_utils
from src.core.auth_middleware import require_auth
# Note que agora usamos o novo modelo de perfil, não mais o DevModel para isso
from src.models.UserProfileModel import UserProfileModel

# 1. Configuração Inicial
ui_utils.init_page(page_title="Meu Perfil", icon="👤")
require_auth()

current_user = st.session_state['user']
user_id = current_user.get('id')

st.title(f"👤 Perfil: {current_user['name']}")

# 2. Carregamento do Perfil (Nova Arquitetura T_Usr_Prf)
profile = UserProfileModel()
profile_loaded = profile.load_by_user(user_id)

# Se não existir perfil, cria um objeto "em branco" vinculado ao usuário
if not profile_loaded:
    profile.PrfUsrCod = user_id

# Abas para separar dados
tab1, tab2 = st.tabs(["🔐 Dados da Conta", "💻 Perfil Profissional"])

# --- ABA 1: Dados da Conta (Apenas Leitura da T_Usr) ---
with tab1:
    with st.container(border=True):
        st.write(f"**Nome:** {current_user['name']}")
        st.write(f"**Login:** {current_user['username']}")
        st.write(f"**Permissão:** {current_user['role']}")
        st.info("Para alterar sua senha, utilize o menu lateral 'Segurança' > 'Alterar Senha'.")

# --- ABA 2: Perfil Estendido (Editável - T_Usr_Prf) ---
with tab2:
    with st.form("form_profissional"):
        st.write("### Informações Profissionais")
        
        # MERGE: Usando lógica de campos manuais para ter controle total,
        # mas mapeando para os novos campos (PrfCgo, PrfBio, etc)
        
        # Cargo
        new_cgo = st.text_input(
            "Cargo / Função", 
            value=profile.PrfCgo if profile.PrfCgo else "",
            placeholder="Ex: Analista de Sistemas Pleno"
        )
        
        # Biografia
        new_bio = st.text_area(
            "Biografia Resumida", 
            value=profile.PrfBio if profile.PrfBio else "", 
            height=100,
            placeholder="Conte um pouco sobre sua experiência..."
        )
        
        # Portfólio / URL
        new_url = st.text_input(
            "Link do Portfólio / LinkedIn", 
            value=profile.PrfUrl if profile.PrfUrl else "",
            placeholder="https://..."
        )

        st.write("---")
        st.write("### 📸 Foto de Perfil")

        # MERGE: Recuperando a lógica visual do arquivo OLD
        
        # 1. Exibe a prévia atual (buscando do novo campo PrfFto)
        if profile.PrfFto and os.path.exists(profile.PrfFto):
            st.image(profile.PrfFto, caption="Foto Atual", width=150)
        else:
            st.image("assets/default_user.png", caption="Sem foto definida", width=150)

        # 2. Componente de Upload
        uploaded_file = st.file_uploader("Alterar foto (JPG/PNG)", type=["jpg", "jpeg", "png"])

        # 3. Prévia imediata ao selecionar arquivo
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Prévia da Nova Foto", width=150)

        submitted = st.form_submit_button("💾 Salvar Perfil", type="primary")

        if submitted:
            # Atualiza os dados de texto no objeto
            profile.PrfCgo = new_cgo
            profile.PrfBio = new_bio
            profile.PrfUrl = new_url
            
            # MERGE: Lógica de Salvamento de Arquivo
            if uploaded_file is not None:
                upload_dir = "data/uploads"
                # Garante que a pasta existe
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                # Define nome único baseado no ID do Usuário
                file_ext = uploaded_file.name.split('.')[-1]
                file_name = f"user_{user_id}_avatar.{file_ext}"
                full_path = os.path.join(upload_dir, file_name)
                
                # Salva fisicamente
                with open(full_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Atualiza caminho no objeto do banco
                profile.PrfFto = full_path

                # ATUALIZAÇÃO CRÍTICA: Atualiza a sessão para o menu lateral mudar na hora
                current_user['UsrFto'] = full_path
                st.session_state['user'] = current_user

            # Persistência no Banco
            if profile.save():
                st.success("Perfil atualizado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao salvar as informações no banco de dados.")