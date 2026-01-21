import streamlit as st
import pandas as pd
from src.services.dev_service import DevService
from src.services.task_service import TaskService
from src.core import ui_utils
from src.core.auth_middleware import require_auth

ui_utils.init_page(page_title="Gestão de Tarefas", icon="📝")
require_auth()

st.title("📝 Tarefas")

task_service = TaskService()
dev_service = DevService()

# Carregar Desenvolvedores
df_devs = dev_service.get_all_devs_dataframe()
if df_devs.empty:
    st.warning("Nenhum desenvolvedor cadastrado.")
    st.stop()

dev_map = dict(zip(df_devs['DevNom'], df_devs['DevCod']))

# --- FORMULÁRIO ---
with st.expander("➕ Nova Tarefa", expanded=True):
    with st.form("frm_task", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        titulo = c1.text_input("Título")
        resp = c2.selectbox("Responsável", options=list(dev_map.keys()))
        prio = c3.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Crítica"], index=1)
        
        c4, c5, c6 = st.columns([3, 2, 2])
        desc = c4.text_area("Descrição", height=100)
        impacto = c5.selectbox("Impacto", ["Baixo", "Médio", "Alto"], index=1)
        entrega = c6.date_input("Entrega")
        
        if st.form_submit_button("Salvar", type="primary", use_container_width=True):
            if not titulo:
                st.error("Título obrigatório.")
            else:
                payload = {
                    "TrfTtl": titulo, "TrfDesc": desc, 
                    "TrfDevCod": dev_map[resp], "TrfPrio": prio,
                    "TrfImp": impacto, "TrfDatEnt": entrega, "TrfStt": "A Fazer"
                }
                ok, msg = task_service.save_task(payload)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

st.divider()

# --- LISTAGEM ---
st.subheader("📋 Lista de Tarefas")
df = task_service.get_all_tasks()

if not df.empty:
    filtro = st.text_input("🔎 Pesquisar...", placeholder="Título ou Responsável")
    if filtro:
        m = df['TrfTtl'].astype(str).str.contains(filtro, case=False) | \
            df['DevNome'].astype(str).str.contains(filtro, case=False)
        df = df[m]

    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True,
        column_order=["TrfCod", "TrfTtl", "DevNome", "TrfPrio", "TrfImp", "TrfStt", "TrfDatEnt"],
        column_config={
            "TrfCod": st.column_config.NumberColumn("#", width="small"),
            "TrfTtl": "Tarefa",
            "DevNome": "Responsável",
            "TrfStt": st.column_config.SelectboxColumn("Status", options=["A Fazer", "Em Progresso", "Concluído"]),
            "TrfDatEnt": st.column_config.DateColumn("Prazo", format="DD/MM/YYYY")
        }
    )
else:
    st.info("Nenhuma tarefa cadastrada.")