import streamlit as st
import pandas as pd
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService
from src.core.auth_middleware import require_auth

require_auth(allowed_roles=['admin', 'manager'])

st.title("📦 Gerar Nova Release")
st.write("Consolide as tarefas concluídas em uma nova versão oficial do sistema.")

rel_service = ReleaseService()
task_service = TaskService()

# 1. Busca tarefas prontas (Concluídas e sem Release)
df_ready = task_service.get_all_tasks_filtered(where="t.TrfStt = 'Concluído' AND t.TrfRelCod IS NULL")

if df_ready.empty:
    st.info("✨ Não há tarefas concluídas aguardando release no momento.")
else:
    st.subheader("📋 Tarefas para inclusão")
    st.dataframe(
        df_ready[['TrfCod', 'TrfTtl', 'DevNome', 'TrfDatEnt']],
        column_config={"TrfCod": "ID", "TrfTtl": "Título", "DevNome": "Responsável", "TrfDatEnt": "Conclusão"},
        use_container_width=True, hide_index=True
    )
    
    st.divider()
    
    # 2. Formulário da Nova Release
    with st.form("form_release"):
        col1, col2 = st.columns(2)
        version = col1.text_input("Versão (ex: v1.2.0)", placeholder="vX.X.X")
        date_rel = col2.date_input("Data da Release")
        title = st.text_input("Título/Descrição da Versão")
        
        if st.form_submit_button("📦 Fechar e Publicar Release", type="primary", use_container_width=True):
            if not version or not title:
                st.error("Versão e Título são obrigatórios.")
            else:
                # A) Cria a Release
                success, rel_id_or_msg = rel_service.create_release(version, title, st.session_state['user']['UsrLgn'])
                
                if success:
                    # B) Vincula todas as tarefas da lista à nova Release
                    count = 0
                    for _, row in df_ready.iterrows():
                        if task_service.update_task_release(row['TrfCod'], rel_id_or_msg):
                            count += 1
                    
                    st.success(f"Release {version} publicada! {count} tarefas vinculadas.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(rel_id_or_msg)