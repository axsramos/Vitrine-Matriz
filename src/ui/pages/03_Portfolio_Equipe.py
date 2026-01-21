import streamlit as st
from src.services.dev_service import DevService
from src.core.ui_utils import load_avatar
from src.core.auth_middleware import require_auth

# Proteção de acesso
require_auth()

st.title("👥 Time de Desenvolvedores")
st.write("Equipe técnica responsável pelo ecossistema Vitrine-Matriz.")

dev_service = DevService()
df_devs = dev_service.get_all_devs_dataframe()

if df_devs.empty:
    st.info("Nenhum desenvolvedor cadastrado no time no momento.")
else:
    # Define a grade visual (3 colunas)
    cols = st.columns(3)
    
    for idx, row in df_devs.iterrows():
        with cols[idx % 3]:
            # Container com borda para efeito de "Card"
            with st.container(border=True):
                # load_avatar busca do Config.AVATAR_PATH (database/uploads/avatars)
                # com fallback para o assets/default_user.png
                foto = load_avatar(row['UsrPrfFto'])
                st.image(foto, use_container_width=True)
                
                st.subheader(row['DevNom'])
                st.caption(f"💼 {row['UsrPrfCgo'] or 'Desenvolvedor'}")
                
                # Exibição limitada da Bio
                bio = row['UsrPrfBio'] if row['UsrPrfBio'] else ""
                if bio:
                    st.write(f"{bio[:120]}..." if len(bio) > 120 else bio)
                
                if row['UsrPrfUrl']:
                    st.link_button("🌐 Portfólio / LinkedIn", row['UsrPrfUrl'], use_container_width=True)

st.divider()
st.caption("Informações atualizadas via Gestão de Usuários e Perfis.")