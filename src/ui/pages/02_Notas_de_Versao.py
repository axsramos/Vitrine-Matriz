import streamlit as st
from src.services.release_service import ReleaseService

st.set_page_config(page_title="Notas de Versão - Portal Matriz", layout="centered")

st.title("🗒️ Notas de Versão")
st.markdown("---")

service = ReleaseService()
df = service.get_all_releases_with_tasks()

if df.empty:
    st.info("Nenhuma nota de versão publicada até ao momento.")
else:
    # Agrupamos por versão para exibir o cabeçalho uma única vez
    for versao, grupo in df.groupby("versao", sort=False):
        if versao == 'Sem Versão':
            st.header("⏳ Entregas em Aguardo de Release")
            st.caption("Estas tarefas já foram concluídas mas ainda não foram publicadas em uma versão oficial.")
        else:
            st.header(f"Versão {versao}")
            st.caption(f"Publicado em: {grupo['data_publicacao'].iloc[0]}")
            st.subheader(grupo['titulo_comunicado'].iloc[0])
            
            # Lista de Itens da Release
            for _, row in grupo.iterrows():
                with st.expander(f"🔹 {row['tarefa_titulo']}", expanded=False):
                    st.markdown(row['descricao_tecnica'])
            
            st.markdown("---")