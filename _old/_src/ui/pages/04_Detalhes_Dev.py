import streamlit as st
import pandas as pd
import os
from src.services.dev_service import DevService
from src.core import ui_utils

# 1. Configuração da Página
ui_utils.init_page(page_title="Detalhes do Desenvolvedor", icon="🕵️")

st.title("🕵️ Detalhes do Profissional")
st.markdown("Visualize informações detalhadas e métricas de cada membro da equipe.")
st.markdown("---")

# 2. Carregamento dos Dados
dev_service = DevService()

# CORREÇÃO: Usamos o método novo que retorna o DataFrame consolidado (T_Dev + T_UsrPrf)
df_devs = dev_service.get_all_devs_dataframe()

if df_devs.empty:
    st.warning("Nenhum desenvolvedor encontrado na base de dados.")
    st.stop()

# 3. Seletor de Desenvolvedor
# Cria uma lista de nomes para o Selectbox
opcoes_devs = df_devs['DevNme'].tolist()
selected_dev_name = st.selectbox("Selecione um profissional:", options=opcoes_devs)

# Filtra o DataFrame para pegar os dados do selecionado
# (Como DevNme não é único idealmente, em produção usaríamos ID, mas aqui mantém a simplicidade visual)
dev_data = df_devs[df_devs['DevNme'] == selected_dev_name].iloc[0]

# --- Exibição dos Detalhes ---

# Layout em colunas (Foto/Info à esquerda, Métricas/Bio à direita)
col1, col2 = st.columns([1, 2])

with col1:
    with st.container(border=True):
        # Tratamento da Foto (UsrPrfFto)
        fto_path = dev_data['UsrPrfFto']
        if fto_path and os.path.exists(fto_path):
            st.image(fto_path, use_container_width=True)
        else:
            st.image("assets/default_user.png", use_container_width=True)
        
        # Link do Portfólio
        url = dev_data['UsrPrfUrl']
        if url:
            st.link_button("🌐 Visitar Portfólio", url, use_container_width=True)

with col2:
    st.subheader(dev_data['DevNme'])
    
    # Cargo (UsrPrfCgo)
    cargo = dev_data['UsrPrfCgo'] if dev_data['UsrPrfCgo'] else "Cargo não definido"
    st.caption(f"💼 {cargo}")
    
    st.write("### Sobre")
    # Bio (UsrPrfBio)
    bio = dev_data['UsrPrfBio']
    if bio:
        st.write(bio)
    else:
        st.info("Este profissional ainda não adicionou uma biografia.")

    # Exemplo de onde você pode expandir futuramente (Métricas, Tarefas, etc.)
    # st.divider()
    # st.metric("Tarefas Concluídas", 42) # Exemplo estático