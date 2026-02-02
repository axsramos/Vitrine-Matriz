import streamlit as st
import os

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth
from src.core.ui_utils import load_avatar

# --- SERVIÇOS ---
from src.services.user_service import UserService

# --- METADADOS ---
from src.models.md.UsrPrfMD import UsrPrfMD

# Configuração da Página
st.set_page_config(
    page_title=f"Meu Perfil | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth()

# --- CABEÇALHO ---
st.title("👤 Meu Perfil")
st.write("Mantenha suas informações profissionais atualizadas.")

# Instância do Serviço e Dados de Sessão
user_service = UserService()
current_user = st.session_state['user']
user_id = current_user['UsrCod']

# --- CARREGAMENTO DE DADOS ---
# Busca o perfil através do serviço (abstração do banco)
profile_data = user_service.get_profile(user_id) or {}

# Layout em duas colunas: Foto (Esquerda) e Formulário (Direita)
col_foto, col_form = st.columns([1, 2])

# --- SEÇÃO DE UPLOAD DE FOTO ---
with col_foto:
    st.subheader("Foto de Perfil")
    
    # Exibe avatar atual
    current_foto_path = profile_data.get('UsrPrfFto')
    st.image(load_avatar(current_foto_path), width=200)
    
    # Campo de Upload
    new_foto_file = st.file_uploader(
        "Alterar foto", 
        type=['png', 'jpg', 'jpeg'],
        help="Recomendado: Imagem quadrada (Ratio 1:1)"
    )

# --- SEÇÃO DO FORMULÁRIO ---
with col_form:
    st.subheader("Informações Profissionais")
    
    with st.form("form_perfil"):
        # Campo CARGO
        lbl_cgo = UsrPrfMD.FIELDS_MD['UsrPrfCgo']['Label']
        val_cgo = profile_data.get('UsrPrfCgo', '')
        cargo_input = st.text_input(lbl_cgo, value=val_cgo)
        
        # Campo URL/LINK
        lbl_url = UsrPrfMD.FIELDS_MD['UsrPrfUrl']['Label']
        val_url = profile_data.get('UsrPrfUrl', '')
        url_input = st.text_input(lbl_url, value=val_url, placeholder="https://linkedin.com/in/...")
        
        # Campo BIO
        lbl_bio = UsrPrfMD.FIELDS_MD['UsrPrfBio']['Label']
        val_bio = profile_data.get('UsrPrfBio', '')
        bio_input = st.text_area(lbl_bio, value=val_bio, height=150)
        
        # Botão de Ação
        submitted = st.form_submit_button("💾 Salvar Alterações", type="primary")

        if submitted:
            # Prepara DTO (Data Transfer Object)
            update_data = {
                "UsrPrfCgo": cargo_input,
                "UsrPrfUrl": url_input,
                "UsrPrfBio": bio_input
            }
            
            # Chama serviço para atualizar (incluindo upload se houver)
            success, msg = user_service.update_profile(user_id, update_data, new_foto_file)
            
            if success:
                st.success(msg)
                # Opcional: st.rerun() para atualizar a foto imediatamente
            else:
                st.error(msg)