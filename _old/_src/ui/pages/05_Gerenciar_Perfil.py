import streamlit as st
import os
from PIL import Image

# Imports do sistema
from src.core import ui_utils
from src.core.auth_middleware import require_auth
from src.models.UserProfileModel import UserProfileModel

# 1. Configuração
ui_utils.init_page(page_title="Meu Perfil", icon="👤")
require_auth()

current_user = st.session_state['user']
user_id = current_user.get('id')

st.title(f"👤 Perfil: {current_user['name']}")

# 2. Carregamento
profile = UserProfileModel()
profile_loaded = profile.load_by_user(user_id)

# Se for um perfil novo (ainda não salvo no banco)
if not profile_loaded:
    profile.prepare_for_save(user_id)

# Abas
tab1, tab2 = st.tabs(["🔐 Dados da Conta", "💻 Perfil Profissional"])

with tab1:
    with st.container(border=True):
        st.write(f"**Nome:** {current_user['name']}")
        st.write(f"**Login:** {current_user['username']}")
        st.info("Configurações de conta são gerenciadas pelo administrador.")

with tab2:
    with st.form("form_profissional"):
        st.write("### Informações Profissionais")
        
        # Campos de Texto
        new_cgo = st.text_input("Cargo / Função", value=profile.UsrPrfCgo if profile.UsrPrfCgo else "")
        new_bio = st.text_area("Biografia", value=profile.UsrPrfBio if profile.UsrPrfBio else "", height=100)
        new_url = st.text_input("LinkedIn / Portfólio", value=profile.UsrPrfUrl if profile.UsrPrfUrl else "")

        st.write("---")
        st.write("### 📸 Foto de Perfil")

        # Visualização da Foto
        if profile.UsrPrfFto and os.path.exists(profile.UsrPrfFto):
            st.image(profile.UsrPrfFto, caption="Foto Atual", width=150)
        else:
            st.image("assets/default_user.png", caption="Sem foto", width=150)

        uploaded_file = st.file_uploader("Alterar foto", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            st.image(Image.open(uploaded_file), caption="Prévia", width=150)

        submitted = st.form_submit_button("💾 Salvar Alterações", type="primary")

        if submitted:
            # Atualiza objeto
            profile.UsrPrfCgo = new_cgo
            profile.UsrPrfBio = new_bio
            profile.UsrPrfUrl = new_url
            
            # Garante o vínculo (caso tenha se perdido ou seja novo insert)
            profile.prepare_for_save(user_id)

            # Upload
            if uploaded_file is not None:
                upload_dir = "data/uploads"
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                # Nome do arquivo: user_{ID_DO_USER}_avatar
                file_ext = uploaded_file.name.split('.')[-1]
                file_name = f"user_{user_id}_avatar.{file_ext}"
                full_path = os.path.join(upload_dir, file_name)
                
                with open(full_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                profile.UsrPrfFto = full_path
                
                # Atualiza Sidebar
                current_user['UsrFto'] = full_path
                st.session_state['user'] = current_user

            # Persistência
            if profile.save():
                st.success("Perfil salvo com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao salvar perfil.")