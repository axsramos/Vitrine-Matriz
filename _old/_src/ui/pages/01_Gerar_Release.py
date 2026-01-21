import streamlit as st
import time
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService
from src.core import ui_utils
from src.models.ReleaseModel import ReleaseModel # Certifique-se que este import existe

# 1. Configuração da Página
ui_utils.init_page(page_title="Gerar Release", icon="📦")
st.title("📦 Gerar Nova Release")

# 2. Instância dos Serviços
rel_service = ReleaseService()
task_service = TaskService()

# 3. Formulário da Nova Versão
with st.container(border=True):
    st.subheader("Dados da Versão")
    
    # Inputs diretos para garantir funcionamento
    version = st.text_input("Versão (Ex: 1.0.0)", placeholder="1.0.0")
    title = st.text_input("Título/Comentário", placeholder="Release de Correção de Bugs")

# 4. Seleção de Tarefas Pendentes
st.subheader("Vincular Tarefas")

# Busca tarefas que não têm release vinculada (TrfRelCod IS NULL)
df_pending = task_service.get_pending_tasks()

selected_tasks = []

if df_pending.empty:
    st.info("Não há tarefas pendentes para vincular nesta versão.")
else:
    # Cria uma coluna visual para o dropdown
    # USANDO OS NOMES CORRETOS: TrfCod e TrfTtl
    df_pending['display_text'] = df_pending.apply(
        lambda x: f"[{x['TrfCod']}] {x['TrfTtl']}", axis=1
    )
    
    # Multiselect retornando os IDs (TrfCod)
    selected_indices = st.multiselect(
        "Selecione as tarefas que entram nesta versão:",
        options=df_pending['TrfCod'].tolist(),
        format_func=lambda x: df_pending[df_pending['TrfCod'] == x]['display_text'].values[0]
    )
    selected_tasks = selected_indices

st.divider()

# 5. Botão de Ação
if st.button("🚀 Publicar Release", type="primary", use_container_width=True):
    # Validações
    if not version or not title:
        st.error("Por favor, preencha a Versão e o Título da Release.")
    elif not selected_tasks:
        st.error("Selecione pelo menos uma tarefa para compor a release.")
    else:
        with st.spinner("Criando release e vinculando tarefas..."):
            # A. Cria a Release na T_Rel
            success, result = rel_service.create_release(version, title)
            
            if success:
                new_rel_id = result # O serviço retorna o ID da nova release
                
                # B. Vincula cada tarefa selecionada à nova Release
                count_ok = 0
                for task_id in selected_tasks:
                    if task_service.update_task_release(task_id, new_rel_id):
                        count_ok += 1
                
                # Feedback de Sucesso
                st.success(f"✅ Release **{version}** criada com sucesso!")
                st.toast(f"{count_ok} tarefas foram vinculadas à versão {version}.", icon="🔗")
                
                # Efeito visual e Reload
                st.balloons()
                time.sleep(2) # Dá tempo de ler a mensagem
                st.rerun()    # Limpa a tela
            else:
                st.error(f"Erro ao criar release: {result}")