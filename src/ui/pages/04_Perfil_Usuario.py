import streamlit as st
import os
from src.services.user_service import UserService
from src.models.UserProfileModel import UserProfileModel
from src.core.ui_utils import load_avatar
from src.core.config import Config
from src.core.auth_middleware import require_auth

require_auth()

st.title("👤 Meu Perfil")

user_service = UserService()
current_user = st.session_state['user']
user_id = current_user['UsrCod']

# Carrega dados atuais do perfil
profile_data = user_service.get_user_profile(user_id)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Foto de Perfil")
    # Exibe avatar atual ou padrão
    current_foto = profile_data.get('UsrPrfFto')
    st.image(load_avatar(current_foto), width=200)
    
    # Upload de nova foto
    new_foto = st.file_uploader("Alterar foto", type=['png', 'jpg', 'jpeg'])
    
with col2:
    st.subheader("Informações Profissionais")
    with st.form("form_perfil"):
        cargo = st.text_input("Cargo/Função", value=profile_data.get('UsrPrfCgo', ''))
        url = st.text_input("LinkedIn ou Portfólio (URL)", value=profile_data.get('UsrPrfUrl', ''))
        bio = st.text_area("Biografia Profissional", value=profile_data.get('UsrPrfBio', ''), height=150)
        
        if st.form_submit_button("Atualizar Perfil", type="primary"):
            updated_data = {
                "UsrPrfCgo": cargo,
                "UsrPrfUrl": url,
                "UsrPrfBio": bio,
                "UsrPrfAudUsr": current_user['UsrLgn']
            }
            
            # Lógica de processamento da imagem
            if new_foto:
                # Gera nome único para o arquivo: usr_1_timestamp.png
                file_ext = os.path.splitext(new_foto.name)[1]
                file_name = f"avatar_{user_id}{file_ext}"
                save_path = os.path.join(Config.AVATAR_PATH, file_name)
                
                with open(save_path, "wb") as f:
                    f.write(new_foto.getbuffer())
                
                updated_data["UsrPrfFto"] = save_path

            # Salva no banco via Service
            if user_service.update_profile(user_id, updated_data):
                st.success("Perfil atualizado com sucesso!")
                # Atualiza sessão para refletir mudanças no menu lateral imediatamente
                new_profile = user_service.get_user_profile(user_id)
                st.session_state['user'].update(new_profile)
                st.rerun()
            else:
                st.error("Erro ao atualizar perfil.")