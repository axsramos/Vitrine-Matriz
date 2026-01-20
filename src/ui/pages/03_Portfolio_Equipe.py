import streamlit as st
import os
from src.services.dev_service import DevService
from src.core import ui_utils

# 1. Configuração da Página
ui_utils.init_page(page_title="Portfólio da Equipe", icon="👥")

st.title("👥 Nossa Equipe")
st.markdown("Conheça os profissionais que fazem a diferença na Vitrine Matriz.")
st.markdown("---")

# 2. Carregamento dos Dados
dev_service = DevService()

# Este método agora retorna um DataFrame com o merge entre T_Dev e T_UsrPrf
df_equipe = dev_service.get_all_devs_dataframe()

# 3. Renderização da Interface
if df_equipe.empty:
    st.info("Nenhum perfil profissional encontrado no momento.")
else:
    # Cria um layout de grade (3 colunas por linha)
    cols = st.columns(3)
    
    for index, row in df_equipe.iterrows():
        # Distribui os cards ciclicamente entre as colunas
        col = cols[index % 3]
        
        with col:
            with st.container(border=True):
                # --- A. Tratamento da Foto (UsrPrfFto) ---
                fto_path = row['UsrPrfFto']
                
                # Se existe caminho e o arquivo físico está lá, exibe. Senão, usa padrão.
                if fto_path and os.path.exists(fto_path):
                    st.image(fto_path, use_container_width=True)
                else:
                    st.image("assets/default_user.png", use_container_width=True)

                # --- B. Dados Principais ---
                # Nome vem da T_Dev (DevNme)
                st.subheader(row['DevNme'])
                
                # Cargo vem da T_UsrPrf (UsrPrfCgo)
                cargo = row['UsrPrfCgo'] if row['UsrPrfCgo'] else "Colaborador"
                st.caption(f"💼 {cargo}")
                
                # --- C. Biografia (UsrPrfBio) ---
                bio = row['UsrPrfBio']
                if bio:
                    # Limita o texto para não quebrar o layout se for muito grande
                    st.write(bio[:150] + "..." if len(bio) > 150 else bio)
                else:
                    st.write("Perfil em construção.")
                
                # --- D. Link Externo (UsrPrfUrl) ---
                url = row['UsrPrfUrl']
                if url:
                    st.link_button("🌐 Ver Portfólio", url, use_container_width=True)
                else:
                    st.button("🚫 Sem Link", disabled=True, use_container_width=True)