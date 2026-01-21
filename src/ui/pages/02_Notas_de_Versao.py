import streamlit as st
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService
from src.core.auth_middleware import require_auth

# Proteção de acesso
require_auth()

st.title("📜 Notas de Versão")
st.write("Acompanhe o histórico de atualizações e melhorias implementadas no sistema.")

rel_service = ReleaseService()
task_service = TaskService()

# 1. Busca todas as releases publicadas (não deletadas)
df_releases = rel_service.get_all_releases()

if df_releases.empty:
    st.info("ℹ️ Nenhuma release foi publicada até o momento.")
else:
    # Itera sobre as releases para criar a visualização em "Timeline"
    for _, rel in df_releases.iterrows():
        # Container estilizado para cada versão
        with st.container(border=True):
            col_v, col_d = st.columns([1, 4])
            
            with col_v:
                st.subheader(f"🚀 {rel['RelVrs']}")
                st.caption(f"📅 {rel['RelDat']}")
            
            with col_d:
                st.markdown(f"### {rel['RelTtlCmm']}")
                
                # 2. Busca tarefas vinculadas a esta release específica
                # Usamos o filtro dinâmico que criamos no Passo 4
                df_tasks = task_service.get_all_tasks_filtered(where=f"t.TrfRelCod = {rel['RelCod']}")
                
                if not df_tasks.empty:
                    st.write("**O que mudou nesta versão:**")
                    # Exibe como uma lista de tópicos (Markdown)
                    for _, task in df_tasks.iterrows():
                        # Ícone baseado na prioridade para destaque visual
                        icon = "🔴" if task['TrfPrio'] == 'Crítica' else "🔹"
                        st.markdown(f"{icon} **{task['TrfTtl']}** - *{task['DevNome']}*")
                else:
                    st.caption("Nenhuma tarefa detalhada para esta versão.")

st.divider()
st.caption("Os dados desta página são gerados automaticamente após o fechamento de uma Release.")