import streamlit as st
from datetime import date, datetime
from src.models.TaskStatus import TaskStatus

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth

# --- SERVIÇOS ---
from src.services.task_service import TaskService
from src.services.dev_service import DevService

# --- METADADOS E ENUMS ---
from src.models.md.TrfMD import TrfMD
from src.models.md.DevMD import DevMD
from src.models.UserRole import UserRole
from src.models.TaskTip import TaskTip  # <--- NOVA IMPORTAÇÃO

# Configuração da Página
st.set_page_config(
    page_title=f"Gestão de Tarefas | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth(allowed_roles=[UserRole.USER, UserRole.MANAGER, UserRole.ADMIN, UserRole.DEVELOPMENT])

st.title("📝 Gestão de Tarefas")
st.write("Crie novas demandas e gerencie o fluxo de trabalho.")

# Instância dos Serviços
task_service = TaskService()
dev_service = DevService()

# --- CARREGAMENTO DE DADOS INICIAIS ---
dev_options = dev_service.get_dev_options()
if not dev_options:
    st.warning("⚠️ Nenhum desenvolvedor cadastrado. Contate o administrador.")
    st.stop()

# Identifica usuário atual para pré-seleção no combo de Devs
current_user_id = st.session_state['user']['UsrCod']
current_dev_id = None
current_dev_name_index = 0

all_devs_data = dev_service.get_all_devs()
for dev in all_devs_data:
    if dev.get('DevUsrCod') == current_user_id:
        current_dev_id = dev['DevCod']
        try:
            nomes_lista = list(dev_options.keys())
            current_dev_name_index = nomes_lista.index(dev['DevNom'])
        except ValueError:
            pass
        break

# --- ESTRUTURA DE ABAS ---
tab_nova, tab_minhas, tab_todas = st.tabs([
    "➕ Nova Tarefa", 
    "👤 Minhas Pendências", 
    "🌎 Visão Geral"
])

# ==============================================================================
# ABA 1: NOVA TAREFA (FORMULÁRIO)
# ==============================================================================
with tab_nova:
    st.subheader("Cadastrar Atividade")
    
    with st.form("form_tarefa", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        
        with c1:
            # Título
            lbl_tit = TrfMD.FIELDS_MD['TrfTit']['Label']
            new_tit = st.text_input(f"{lbl_tit} *", placeholder="Resumo da atividade")
            
            # Descrição
            lbl_dsc = TrfMD.FIELDS_MD['TrfDsc']['Label']
            new_dsc = st.text_area(lbl_dsc, height=120, placeholder="Detalhes técnicos...")

        with c2:
            # Responsável
            lbl_dev = DevMD.FIELDS_MD['DevNom']['Label']
            selected_dev_name = st.selectbox(f"{lbl_dev} *", options=dev_options.keys(), index=current_dev_name_index)
            
            # Prazo
            lbl_prz = TrfMD.FIELDS_MD['TrfDatEnt']['Label']
            new_prazo = st.date_input(lbl_prz, value=None, min_value=date.today())
            
            # Metadados Extras (Tipo e Prioridade)
            c2a, c2b = st.columns(2)
            with c2a:
                # TIPO DE TAREFA (Usando Enum TaskTip)
                lbl_tip = TrfMD.FIELDS_MD['TrfTip']['Label']
                # Obtém a lista dinâmica da classe TaskTip (Feature, Bugfix, etc.)
                new_tip = st.selectbox(lbl_tip, options=TaskTip.list()) 
                
            with c2b:
                # PRIORIDADE
                lbl_pri = TrfMD.FIELDS_MD['TrfPri']['Label']
                prios = ["Baixa", "Média", "Alta", "Crítica"]
                new_pri = st.select_slider(lbl_pri, options=prios, value="Média")

        # Ação
        submitted = st.form_submit_button("🚀 Cadastrar Tarefa", type="primary", use_container_width=True)

        if submitted:
            if not new_tit:
                st.error("O título da tarefa é obrigatório.")
            else:
                dev_id_selecionado = dev_options[selected_dev_name]
                prazo_str = new_prazo.strftime('%Y-%m-%d') if new_prazo else None
                
                success, msg = task_service.create_task(
                    titulo=new_tit,
                    desc=new_dsc,
                    tipo=new_tip, # Passando o valor do Enum selecionado
                    prio=new_pri,
                    dev_id=dev_id_selecionado,
                    prazo=prazo_str
                )
                
                if success:
                    st.toast(msg, icon="✅")
                    # Hack para atualizar visualmente as outras abas sem perder o toast
                    # st.rerun() 
                else:
                    st.error(msg)

# ==============================================================================
# ABA 2: MINHAS PENDÊNCIAS (INTERATIVO)
# ==============================================================================
with tab_minhas:
    if current_dev_id:
        st.subheader(f"Lista de Trabalho: {st.session_state['user']['UsrNom']}")
        
        # Busca tarefas não concluídas do Dev logado
        my_tasks = task_service.get_detailed_tasks(
            where="t.TrfDevCod = ? AND t.TrfSit != ?", 
            params=(current_dev_id, TaskStatus.CONCLUIDO)
        )
        
        if not my_tasks:
            st.info("Você não possui tarefas pendentes. 🎉")
        else:
            # Prepara dados para DataEditor
            display_list = []
            for t in my_tasks:
                
                # Conversão de Data (String -> Objeto) para evitar erro no editor
                prazo_obj = None
                raw_date = t.get('TrfDatEnt')
                if raw_date and raw_date != "-":
                    try:
                        prazo_obj = datetime.strptime(str(raw_date), "%Y-%m-%d").date()
                    except ValueError:
                        prazo_obj = None

                display_list.append({
                    "Selecionar": False, # MUDANÇA: Nome genérico para aceitar múltiplas ações
                    "ID": t['TrfCod'],
                    TrfMD.FIELDS_MD['TrfTit']['Label']: t['TrfTit'],
                    TrfMD.FIELDS_MD['TrfTip']['Label']: t['TrfTip'],
                    TrfMD.FIELDS_MD['TrfPri']['Label']: t['TrfPri'],
                    TrfMD.FIELDS_MD['TrfSit']['Label']: t['TrfSit'],
                    TrfMD.FIELDS_MD['TrfDatEnt']['Label']: prazo_obj 
                })
                
            # Exibe Tabela Editável
            edited_data = st.data_editor(
                display_list,
                column_config={
                    "Selecionar": st.column_config.CheckboxColumn("Ação", width="small"), # Checkbox
                    "ID": st.column_config.NumberColumn(width="small"),
                    TrfMD.FIELDS_MD['TrfDatEnt']['Label']: st.column_config.DateColumn("Prazo", format="DD/MM/YYYY")
                },
                disabled=["ID", TrfMD.FIELDS_MD['TrfTit']['Label'], TrfMD.FIELDS_MD['TrfTip']['Label'], TrfMD.FIELDS_MD['TrfPri']['Label'], TrfMD.FIELDS_MD['TrfSit']['Label'], TrfMD.FIELDS_MD['TrfDatEnt']['Label']],
                hide_index=True,
                use_container_width=True,
                key="editor_my_tasks"
            )
            
            # --- ÁREA DE AÇÃO (BOTÕES) ---
            # Identifica quais IDs foram marcados
            selected_ids = [row['ID'] for row in edited_data if row['Selecionar']]
            
            if selected_ids:
                st.markdown("### Ações em Lote")
                c_btn1, c_btn2, _ = st.columns([1.5, 1.5, 4])
                
                # BOTÃO 1: CONCLUIR
                with c_btn1:
                    if st.button(f"🏁 Concluir ({len(selected_ids)})", type="primary", use_container_width=True):
                        success_count = 0
                        for t_id in selected_ids:
                            if task_service.update_task_status(t_id, 'Concluído'):
                                print('%1 - %2'.format(t_id, TaskStatus.CONCLUIDO))
                                success_count += 1
                        
                        if success_count > 0:
                            st.toast(f"{success_count} tarefas concluídas!", icon="✅")
                            st.rerun()

                # BOTÃO 2: EXCLUIR
                with c_btn2:
                    # Usamos um botão normal (secondary) para delete, ou type="primary" se quiser destaque
                    if st.button(f"🗑️ Excluir ({len(selected_ids)})", use_container_width=True):
                        del_count = 0
                        for t_id in selected_ids:
                            if task_service.delete_task(t_id):
                                del_count += 1
                        
                        if del_count > 0:
                            st.toast(f"{del_count} tarefas removidas.", icon="🗑️")
                            st.rerun()

    else:
        st.info("Seu usuário não está vinculado a um perfil de Desenvolvedor.")

# ==============================================================================
# ABA 3: VISÃO GERAL (TODAS AS TAREFAS)
# ==============================================================================
with tab_todas:
    st.subheader("📋 Backlog Geral")
    
    # Filtro
    c_filtro1, _ = st.columns([1, 4])
    with c_filtro1:
        show_closed = st.toggle("Mostrar tarefas concluídas", value=False)
    
    where_clause = None if show_closed else "t.TrfSit != '{}'".format(TaskStatus.CONCLUIDO)
    
    all_tasks = task_service.get_detailed_tasks(where=where_clause)
    
    if not all_tasks:
        st.info("Nenhuma tarefa encontrada.")
    else:
        view_data = []
        for t in all_tasks:
            view_data.append({
                "ID": t['TrfCod'],
                TrfMD.FIELDS_MD['TrfTit']['Label']: t['TrfTit'],
                "Responsável": t.get('NomeDesenvolvedor', '-'),
                TrfMD.FIELDS_MD['TrfTip']['Label']: t['TrfTip'], # Tipo também na visão geral
                TrfMD.FIELDS_MD['TrfPri']['Label']: t['TrfPri'],
                "Status": t['TrfSit'],
                "Entrega": t.get('TrfDatEnt')
            })
            
        st.dataframe(
            view_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Situação",
                    help="Status atual",
                    validate="^(Aberto|Concluído)$"
                ),
                "Entrega": st.column_config.DateColumn("Prazo", format="DD/MM/YYYY")
            }
        )