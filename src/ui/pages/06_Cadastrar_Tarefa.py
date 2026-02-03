import streamlit as st

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth

# --- SERVIÇOS ---
from src.services.task_service import TaskService
from src.services.dev_service import DevService

# --- METADADOS ---
from src.models.md.TrfMD import TrfMD
from src.models.md.DevMD import DevMD
from src.models.UserRole import UserRole
from src.models.TaskTip import TaskTip

# Configuração da Página
st.set_page_config(
    page_title=f"Gestão de Tarefas | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth(allowed_roles=[UserRole.USER, UserRole.MANAGER, UserRole.ADMIN, UserRole.DEVELOPMENT])

st.title("📝 Gestão de Tarefas")
st.write("Crie novas demandas e gerencie suas pendências.")

# Instância dos Serviços
task_service = TaskService()
dev_service = DevService()

# --- CARREGAMENTO DE DADOS ---
# 1. Busca dicionário {Nome: ID} para o dropdown
dev_options = dev_service.get_dev_options()

if not dev_options:
    st.warning("⚠️ Nenhum desenvolvedor cadastrado. Contate o administrador.")
    st.stop()

# 2. Identifica o Dev ID do usuário logado (se houver)
current_user_id = st.session_state['user']['UsrCod']
current_dev_id = None
current_dev_name_index = 0

# Precisamos iterar para achar qual Dev corresponde ao UsrCod atual
# (Poderíamos ter um método específico no service, mas vamos iterar a lista completa que é leve)
all_devs_data = dev_service.get_portfolio_data() #get_all_devs()
for dev in all_devs_data:
    if dev.get('DevUsrCod') == current_user_id:
        current_dev_id = dev['DevCod']
        # Acha o índice no dict de opções para setar valor padrão no selectbox
        try:
            nomes_lista = list(dev_options.keys())
            current_dev_name_index = nomes_lista.index(dev['DevNom'])
        except ValueError:
            pass
        break

st.divider()

# --- FORMULÁRIO DE CADASTRO ---
st.subheader("➕ Nova Tarefa")

with st.form("form_tarefa", clear_on_submit=True):
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # Título
        lbl_tit = TrfMD.FIELDS_MD['TrfTit']['Label']
        req_tit = TrfMD.FIELDS_MD['TrfTit']['Required']
        new_tit = st.text_input(f"{lbl_tit} {'*' if req_tit else ''}", placeholder="Resumo da atividade")
        
        # Descrição
        lbl_dsc = TrfMD.FIELDS_MD['TrfDsc']['Label']
        new_dsc = st.text_area(lbl_dsc, height=100, placeholder="Detalhes técnicos...")

    with c2:
        # Responsável (Dropdown)
        lbl_dev = DevMD.FIELDS_MD['DevNom']['Label']
        selected_dev_name = st.selectbox(
            f"{lbl_dev} *", 
            options=dev_options.keys(),
            index=current_dev_name_index
        )
        
        # Tipo de Tarefa ("Feature", "Bugfix", "Refactor", "Documentation", "Support")
        lbl_tip = TrfMD.FIELDS_MD['TrfTip']['Label']
        tipos_disponiveis = TaskTip.list()
        new_tip = st.selectbox(lbl_tip, options=tipos_disponiveis)
        
        # Prioridade
        lbl_pri = TrfMD.FIELDS_MD['TrfPri']['Label']
        pri_disponiveis = ["Baixa", "Média", "Alta", "Crítica"]
        new_pri = st.select_slider(lbl_pri, options=pri_disponiveis, value="Média")

    # Botão de Envio
    submitted = st.form_submit_button("🚀 Cadastrar Tarefa", type="primary", use_container_width=True)

    if submitted:
        if not new_tit:
            st.error("O título da tarefa é obrigatório.")
        else:
            # Recupera ID do dev selecionado
            dev_id_selecionado = dev_options[selected_dev_name]
            
            success, msg = task_service.create_task(
                titulo=new_tit,
                desc=new_dsc,
                tipo=new_tip,
                prio=new_pri,
                dev_id=dev_id_selecionado
            )
            
            if success:
                st.success(msg)
                # st.rerun() # Opcional: Recarregar para limpar form visualmente se clear_on_submit falhar em versões antigas
            else:
                st.error(msg)

st.divider()

# --- LISTAGEM: MINHAS TAREFAS PENDENTES ---
# Se o usuário for um Dev, mostramos as tarefas dele. Se for Admin, mostra tudo ou filtra.
# Aqui assumimos a visão "Minhas Tarefas" baseada no usuário logado.

if current_dev_id:
    st.subheader(f"📋 Pendências de {st.session_state['user']['UsrNom']}")
    
    # Busca tarefas detalhadas (com JOIN para exibir nomes se precisasse, mas aqui o foco é a ação)
    # Filtro: Pertence ao Dev E Status não é Concluído
    my_tasks = task_service.get_detailed_tasks(
        where="t.TrfDevCod = ? AND t.TrfStt != 'Concluído'", 
        params=(current_dev_id,)
    )
    
    if not my_tasks:
        st.info("Você não possui tarefas pendentes. Bom trabalho! 🎉")
    else:
        # Prepara dados para o Data Editor (Adiciona coluna de checkbox)
        display_list = []
        for t in my_tasks:
            display_list.append({
                "Concluir": False, # Checkbox inicial
                "ID": t['TrfCod'],
                TrfMD.FIELDS_MD['TrfTit']['Label']: t['TrfTit'],
                TrfMD.FIELDS_MD['TrfPri']['Label']: t['TrfPri'],
                TrfMD.FIELDS_MD['TrfTip']['Label']: t['TrfTip']
            })
            
        # Editor de Dados Interativo
        edited_data = st.data_editor(
            display_list,
            column_config={
                "Concluir": st.column_config.CheckboxColumn(
                    "Ação",
                    help="Marque para finalizar a tarefa",
                    default=False,
                ),
                "ID": st.column_config.NumberColumn(width="small"),
            },
            disabled=["ID", TrfMD.FIELDS_MD['TrfTit']['Label'], TrfMD.FIELDS_MD['TrfPri']['Label'], TrfMD.FIELDS_MD['TrfTip']['Label']],
            hide_index=True,
            use_container_width=True,
            key="editor_tasks"
        )
        
        # Lógica de Processamento em Lote
        # Verifica quais linhas foram marcadas como True
        tasks_to_close = [row['ID'] for row in edited_data if row['Concluir']]
        
        if tasks_to_close:
            col_btn, _ = st.columns([1, 4])
            if col_btn.button(f"🏁 Finalizar {len(tasks_to_close)} Selecionada(s)", type="primary"):
                success_count = 0
                for t_id in tasks_to_close:
                    if task_service.update_task_status(t_id, "Concluído"):
                        success_count += 1
                
                if success_count > 0:
                    st.toast(f"{success_count} tarefa(s) concluída(s) com sucesso!", icon="✅")
                    st.rerun()

else:
    # Caso o usuário logado não seja um desenvolvedor cadastrado
    st.info("Seu usuário não está vinculado a um perfil de Desenvolvedor, por isso a lista de 'Minhas Tarefas' está vazia.")
    st.caption("Utilize o formulário acima para delegar tarefas a outros desenvolvedores.")