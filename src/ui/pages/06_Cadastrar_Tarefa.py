import streamlit as st
import pandas as pd
from src.services.task_service import TaskService
from src.services.dev_service import DevService
from src.models.TaskModel import TaskModel
from src.core import ui_utils
from src.core.auth_middleware import require_auth

# Segurança: Garante que apenas usuários logados acessem
require_auth()

st.title("📝 Gestão de Tarefas")

# Inicialização dos serviços
task_service = TaskService()
dev_service = DevService()

# --- CARREGAMENTO DE DEPENDÊNCIAS ---
df_devs = dev_service.get_all_devs_dataframe()
if df_devs.empty:
    st.warning("⚠️ Nenhum desenvolvedor cadastrado. Cadastre um desenvolvedor antes de criar tarefas.")
    st.stop()

# Mapeamento para o Selectbox
dev_options = dict(zip(df_devs['DevNom'], df_devs['DevCod']))

# --- SEÇÃO 1: FORMULÁRIO DE CADASTRO ---
with st.expander("➕ Nova Tarefa", expanded=True):
    with st.form("form_nova_trf", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Renderização automática via Metadados (TrfMD)
            trf_ttl = ui_utils.render_model_field(TaskModel, 'TrfTtl')
            trf_desc = ui_utils.render_model_field(TaskModel, 'TrfDesc')
            
        with col2:
            dev_nom = st.selectbox("Responsável", options=list(dev_options.keys()))
            trf_prio = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Crítica"], index=1)
            trf_imp = st.selectbox("Impacto", ["Baixo", "Médio", "Alto"], index=1)
            trf_dat_ent = st.date_input("Prazo de Entrega")

        if st.form_submit_button("Salvar Registro", type="primary", use_container_width=True):
            if not trf_ttl:
                st.error("O título é obrigatório.")
            else:
                payload = {
                    "TrfTtl": trf_ttl,
                    "TrfDesc": trf_desc,
                    "TrfDevCod": dev_options[dev_nom],
                    "TrfPrio": trf_prio,
                    "TrfImp": trf_imp,
                    "TrfDatEnt": trf_dat_ent.strftime('%Y-%m-%d'),
                    "TrfStt": "A Fazer",
                    "TrfAudUsr": st.session_state['user']['UsrLgn'] # Auditoria
                }
                
                sucesso, msg = task_service.save_task(payload)
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

st.divider()

# --- SEÇÃO 2: CONSULTA (TABELA) ---
st.subheader("📋 Consultar Registros")
df_tasks = task_service.get_all_tasks()

if not df_tasks.empty:
    # Filtro de busca simples na tabela
    search = st.text_input("Filtrar por título ou responsável", placeholder="Digite para buscar...")
    if search:
        mask = df_tasks['TrfTtl'].str.contains(search, case=False) | \
               df_tasks['DevNome'].str.contains(search, case=False)
        df_tasks = df_tasks[mask]

    st.dataframe(
        df_tasks,
        column_order=("TrfCod", "TrfTtl", "DevNome", "TrfPrio", "TrfStt", "TrfDatEnt"),
        column_config={
            "TrfCod": "ID",
            "TrfTtl": "Título",
            "DevNome": "Responsável",
            "TrfPrio": "Prioridade",
            "TrfStt": "Status",
            "TrfDatEnt": st.column_config.DateColumn("Prazo", format="DD/MM/YYYY")
        },
        hide_index=True,
        use_container_width=True
    )