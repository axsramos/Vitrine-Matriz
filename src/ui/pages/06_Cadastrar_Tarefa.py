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

# --- SEÇÃO 2: MINHAS ATIVIDADES (OPÇÃO 2 - CHECKBOX/BULK) ---
st.subheader("🚀 Minhas Atividades Pendentes")

# Captura o código do usuário logado na sessão
usr_logado = st.session_state['user']

# Busca tarefas onde o desenvolvedor vinculado é o usuário logado
minhas_trfs = task_service.get_tasks_by_dev(usr_logado['UsrCod'])

if not minhas_trfs:
    st.info("Nenhuma tarefa pendente.")
else:
    for t in minhas_trfs:
        with st.container(border=True):
            col_info, col_btn_check, col_btn_del = st.columns([3, 1, 1])
            
            with col_info:
                st.write(f"**{t['TrfTtl']}**")
                status_cor = "🟢" if t['TrfStt'] == "Concluído" else "🟡"
                st.caption(f"{status_cor} Status: {t['TrfStt']} | Impacto: {t['TrfImp']}")
            
            # --- BOTÃO CONCLUIR ---
            with col_btn_check:
                is_concluida = t['TrfStt'] == "Concluído"
                # Trocado use_container_width por width='stretch' para eliminar o warning
                if st.button("✅ Feito", key=f"chk_{t['TrfCod']}", 
                            disabled=is_concluida,
                            width='stretch'): 
                    
                    if task_service.update_status(t['TrfCod'], "Concluído"):
                        st.toast("Status atualizado!")
                        st.rerun() # OBRIGATÓRIO para a tela ler o novo status do banco
                    else:
                        st.error("Erro ao persistir status.")

            # --- BOTÃO EXCLUIR ---
            with col_btn_del:
                # Regra: Só exclui se NÃO tiver release (TrfRelCod is null)
                pode_excluir = t.get('TrfRelCod') is None
                if st.button("🗑️", key=f"del_{t['TrfCod']}", 
                             disabled=not pode_excluir,
                             use_container_width=True,
                             help="Excluir (apenas tarefas sem versão)"):
                    if task_service.delete_task(t['TrfCod']):
                        st.success("Tarefa removida!")
                        st.rerun()

# if not minhas_trfs:
#     st.info("Você não possui tarefas pendentes no momento.")
# else:
#     df_minhas = pd.DataFrame(minhas_trfs)
    
#     # Inserimos a coluna de seleção para o checkbox
#     df_minhas.insert(0, "Selecionar", False)

#     # Editor de dados para permitir a seleção de linhas
#     edited_df = st.data_editor(
#         df_minhas,
#         column_order=("Selecionar", "TrfTtl", "TrfPrio", "TrfDatEnt"),
#         column_config={
#             "Selecionar": st.column_config.CheckboxColumn("Finalizar?", help="Marque para concluir"),
#             "TrfTtl": "Tarefa",
#             "TrfPrio": "Prioridade",
#             "TrfDatEnt": st.column_config.DateColumn("Prazo", format="DD/MM/YYYY")
#         },
#         disabled=["TrfTtl", "TrfPrio", "TrfDatEnt"], # Impede edição acidental dos dados
#         hide_index=True,
#         use_container_width=True,
#         key="editor_minhas_tarefas"
#     )

#     # Identifica quais IDs foram marcados no checkbox
#     ids_to_finalize = edited_df[edited_df["Selecionar"] == True]["TrfCod"].tolist()

#     if ids_to_finalize:
#         col_btn, _ = st.columns([1, 2])
#         if col_btn.button(f"🏁 Concluir {len(ids_to_finalize)} Item(ns)", type="primary", use_container_width=True):
#             if task_service.finalize_tasks_bulk(ids_to_finalize, usr_logado['UsrLgn']):
#                 st.toast("Atividades concluídas!", icon="✅")
#                 st.rerun()

st.divider()

# --- SEÇÃO 3: CONSULTA GERAL (SOMENTE LEITURA) ---
st.subheader("📋 Visão Geral do Projeto")
df_all = task_service.get_all_tasks()
if not df_all.empty:
    st.dataframe(df_all, use_container_width=True, hide_index=True)