import streamlit as st
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService
from src.core import ui_utils
from src.models import ReleaseModel

st.set_page_config(page_title="Gerar Release")
st.title("📦 Gerar Nova Release")

rel_service = ReleaseService()
task_service = TaskService()

# 1. Formulário da Nova Versão
with st.container(border=True):
    st.subheader("Dados da Versão")
    # Usa render_model_field para consistência
    version = ui_utils.render_model_field(ReleaseModel, 'RelVrs')
    title = ui_utils.render_model_field(ReleaseModel, 'RelTtlCmm')

# 2. Seleção de Tarefas Pendentes
st.subheader("Vincular Tarefas")
df_pending = task_service.get_pending_tasks()

if df_pending.empty:
    st.info("Não há tarefas pendentes para vincular.")
    selected_tasks = []
else:
    # Cria uma coluna amigável para exibição no multiselect
    # Ex: "[1234] Ajuste no Login"
    df_pending['display'] = df_pending.apply(
        lambda x: f"[{x['TskExtCod']}] {x['TskTtl']}", axis=1
    )
    
    selected_indices = st.multiselect(
        "Selecione as tarefas que entram nesta versão:",
        options=df_pending['TskCod'].tolist(),
        format_func=lambda x: df_pending[df_pending['TskCod'] == x]['display'].values[0]
    )
    selected_tasks = selected_indices

# 3. Botão de Ação
if st.button("🚀 Publicar Release", type="primary"):
    if not version or not title:
        ui_utils.show_error_message("Preencha a Versão e o Título.")
    elif not selected_tasks:
        ui_utils.show_error_message("Selecione pelo menos uma tarefa.")
    else:
        # Cria Release
        success, result = rel_service.create_release(version, title)
        
        if success:
            new_rel_id = result
            # Vincula Tarefas
            count = 0
            for tsk_cod in selected_tasks:
                if task_service.update_task_release(tsk_cod, new_rel_id):
                    count += 1
            
            ui_utils.show_success_message(f"Release {version} criada com {count} tarefas vinculadas!")
            st.rerun()
        else:
            ui_utils.show_error_message(result)