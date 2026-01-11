import streamlit as st
import os
from src.models.desenvolvedor import Desenvolvedor
from src.services.dev_service import DevService

def save_photo(uploaded_file, dev_id):
    """Encapsula a lógica de salvar o arquivo no disco."""
    upload_dir = "assets/uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Define extensão e caminho final
    file_ext = os.path.splitext(uploaded_file.name)[1]
    file_name = f"dev_{dev_id}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    # Gravação binária
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

st.set_page_config(page_title="Gerenciar Perfil - Vitrine Matriz", layout="centered")

st.title("⚙️ Gerenciar Perfil")

# 1. Seleção do Desenvolvedor para Edição
service = DevService()
df_team = service.get_team_stats()

if df_team.empty:
    st.warning("Nenhum desenvolvedor encontrado para editar.")
    st.stop()

selected_dev_name = st.selectbox(
    "Selecione o Desenvolvedor para atualizar:",
    df_team['nome'].tolist()
)

# Recupera os dados atuais do dev selecionado
dev_data = df_team[df_team['nome'] == selected_dev_name].iloc[0]
dev_id = dev_data['id']

st.divider()

# 2. Formulário de Edição
with st.form("form_edicao_dev", clear_on_submit=False):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Preview da foto atual
        if dev_data['foto_path'] and os.path.exists(dev_data['foto_path']):
            st.image(dev_data['foto_path'], caption="Foto Atual", width=150)
        else:
            st.info("Sem foto.")
            
    with col2:
        novo_nome = st.text_input("Nome Completo", value=dev_data['nome'])
        novo_cargo = st.text_input("Cargo/Função", value=dev_data['cargo'])
    
    nova_bio = st.text_area("Bio/Menção (Frase do Card)", value=dev_data['bio'])
    novo_github = st.text_input("URL GitHub", value=dev_data['github_url'])
    
    # Componente de Upload
    nova_foto = st.file_uploader("Trocar Foto de Perfil", type=["jpg", "png", "jpeg"])
    
    submit = st.form_submit_button("💾 Salvar Alterações")

# 3. Processamento do Submit
if submit:
    # Instancia o modelo com os dados do formulário
    dev_model = Desenvolvedor({
        "id": int(dev_id),
        "nome": novo_nome,
        "cargo": novo_cargo,
        "bio": nova_bio,
        "github_url": novo_github
    })
    
    # Se houver nova foto, processa o upload primeiro
    if nova_foto:
        try:
            path_salvo = save_photo(nova_foto, dev_id)
            dev_model.att["foto_path"] = path_salvo
        except Exception as e:
            st.error(f"Erro ao salvar imagem: {e}")
            st.stop()
    else:
        # Mantém a foto antiga se não subiu uma nova
        dev_model.att["foto_path"] = dev_data['foto_path']

    # Persistência via CrudMixin
    if dev_model.update():
        st.success(f"Perfil de {novo_nome} atualizado com sucesso!")
        st.balloons()
    else:
        st.error("Erro ao atualizar o banco de dados.")