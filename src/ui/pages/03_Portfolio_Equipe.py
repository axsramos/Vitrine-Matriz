import streamlit as st
from src.services.dev_service import DevService

# Define o caminho da imagem padrão
DEFAULT_IMAGE = "assets/default_user.png"

st.set_page_config(page_title="Portfólio da Equipe", layout="wide")

st.title("🚀 Nossa Equipe")
st.markdown("---")

service = DevService()
df_devs = service.get_all_developers()

if df_devs.empty:
    st.info("Nenhum desenvolvedor cadastrado na nova base de dados.")
else:
    # Cria colunas para o Grid (3 por linha)
    cols = st.columns(3)
    
    for index, row in df_devs.iterrows():
        col = cols[index % 3]
        
        with col:
            with st.container(border=True):
                # Foto
                foto = row['DevFto'] if row['DevFto'] else DEFAULT_IMAGE
                try:
                    st.image(foto, width=100)
                except:
                    st.image(DEFAULT_IMAGE, width=100)
                
                # Dados (Usando novos nomes de coluna)
                st.subheader(row['DevNme'])
                st.caption(f"💼 {row['DevCgo']}")
                
                # Bio truncada
                bio = row['DevBio'] if row['DevBio'] else "Sem biografia disponível."
                st.write(bio[:120] + "..." if len(bio) > 120 else bio)
                
                # Link GitHub
                if row['DevPgeUrl']:
                    st.link_button("Ver GitHub", row['DevPgeUrl'])