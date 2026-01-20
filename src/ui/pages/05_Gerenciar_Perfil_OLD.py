import os
from PIL import Image
import streamlit as st
from src.services.dev_service import DevService
from src.core import ui_utils
from src.models import DevModel
from src.core.auth_middleware import require_auth

# 1. Configuração Inicial (Padronizada)
ui_utils.init_page(page_title="Meu Perfil", icon="👤")

# 2. Segurança (Usa o Middleware Padrão)
# Isso adiciona automaticamente o botão "Ir para Login" se não estiver logado
require_auth()

# Se passou pelo require_auth, a sessão existe
current_user = st.session_state['user'] 
username = current_user['username']

st.title(f"👤 Perfil: {current_user['name']}")

dev_service = DevService()

# Busca o ID dentro do dicionário do usuário logado
user_id = current_user.get('id') 
dev_profile = dev_service.get_dev_by_user_id(user_id)

# Abas para separar dados de Conta e dados de Desenvolvedor
tab1, tab2 = st.tabs(["🔐 Dados da Conta", "💻 Perfil Profissional"])

with tab1:
    with st.container(border=True):
        st.write(f"**Nome:** {current_user['name']}")
        st.write(f"**Login:** {username}")
        st.write(f"**Permissão:** {current_user['role']}")
        st.info("Para alterar sua senha, utilize o menu lateral 'Segurança' > 'Alterar Senha'.")

with tab2:
    if dev_profile:
        with st.form("form_profissional"):
            # Usando o Model carregado para preencher os valores atuais
            
            # Cargo
            dev_cgo = ui_utils.render_model_field(
                DevModel, 'DevCgo', 
                default_value=dev_profile.DevCgo
            )
            
            # Bio (TextArea automático)
            dev_bio = ui_utils.render_model_field(
                DevModel, 'DevBio', 
                default_value=dev_profile.DevBio
            )

            st.write("### 📸 Foto de Perfil")
            
            # 1. Exibe a prévia atual (se existir)
            if dev_profile.DevFto:
                try:
                    st.image(dev_profile.DevFto, caption="Foto Atual", width=150)
                except:
                    st.caption("⚠️ Não foi possível carregar a imagem atual.")

            # 2. Componente de Upload
            uploaded_file = st.file_uploader("Selecione uma nova foto (JPG/PNG)", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                # 3. Prévia da nova imagem selecionada
                image = Image.open(uploaded_file)
                st.image(image, caption="Nova Foto Selecionada", width=150)
            
            # Portfolio URL
            dev_url = ui_utils.render_model_field(
                DevModel, 'DevPgeUrl', 
                default_value=dev_profile.DevPgeUrl
            )
            
            st.markdown("---")
            submitted = st.form_submit_button("💾 Atualizar Perfil Profissional", type="primary")

            if submitted:
                # 4. Lógica de Salvamento do Arquivo
                if uploaded_file is not None:
                    # Cria a pasta de uploads se não existir
                    upload_path = "data/uploads"
                    if not os.path.exists(upload_path):
                        os.makedirs(upload_path)
                    
                    # Define o nome do arquivo (sugestão: usar o ID do dev para ser único)
                    file_ext = uploaded_file.name.split('.')[-1]
                    file_name = f"dev_{dev_profile.DevCod}.{file_ext}"
                    full_path = os.path.join(upload_path, file_name)
                    
                    # Salva fisicamente o arquivo
                    with open(full_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Atualiza o caminho no objeto para salvar no banco
                    dev_profile.DevFto = full_path

                # Atualiza os demais campos
                dev_profile.DevCgo = dev_cgo
                dev_profile.DevBio = dev_bio
                # ...
                
                if dev_profile.save():
                    st.success("Perfil atualizado com sucesso!")
                    st.rerun()
