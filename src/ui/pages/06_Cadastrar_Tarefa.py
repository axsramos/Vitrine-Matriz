import streamlit as st
from src.services.task_service import TaskService
from src.services.dev_service import DevService
from src.services.release_service import ReleaseService
from src.models import TaskModel
from src.core import ui_utils

# Inicializa a página
ui_utils.init_page(page_title="Cadastrar Tarefa", icon="📝")

st.title("📝 Nova Tarefa")

# Instancia Serviços
task_service = TaskService()
dev_service = DevService()
rel_service = ReleaseService()

# Carrega listas para os Dropdowns (FKs)
df_devs = dev_service.get_all_developers()
df_rels = rel_service.get_all_releases()

# --- INÍCIO DO FORMULÁRIO ---
with st.form("form_nova_tarefa"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Campos automáticos via Metadados
        tsk_ext_cod = ui_utils.render_model_field(TaskModel, 'TskExtCod')
        tsk_ttl = ui_utils.render_model_field(TaskModel, 'TskTtl')
    
    with col2:
        # Dropdowns (FKs precisam ser manuais para mapear ID -> Nome)
        
        # Desenvolvedor
        label_dev = TaskModel.FIELDS_MD['DevCod']['LongLabel']
        
        # Monta opções com ID e Nome para exibição
        dev_options = df_devs['DevCod'].tolist() if not df_devs.empty else []
        
        # Função para mostrar o nome no selectbox
        def format_dev_func(cod):
            if df_devs.empty: return "N/A"
            row = df_devs[df_devs['DevCod'] == cod]
            if not row.empty:
                return row.iloc[0]['DevNme']
            return str(cod)

        dev_cod = st.selectbox(
            label_dev,
            options=dev_options,
            format_func=format_dev_func,
            index=None, # Permite vazio
            placeholder="Selecione um desenvolvedor..."
        )
        
        # Release
        label_rel = TaskModel.FIELDS_MD['RelCod']['LongLabel']
        rel_options = df_rels['RelCod'].tolist() if not df_rels.empty else []
        
        def format_rel_func(cod):
            if df_rels.empty: return "N/A"
            row = df_rels[df_rels['RelCod'] == cod]
            if not row.empty:
                return row.iloc[0]['RelVrs']
            return str(cod)

        rel_cod = st.selectbox(
            label_rel,
            options=rel_options,
            format_func=format_rel_func,
            index=None,
            placeholder="Selecione uma release (opcional)..."
        )

    # Descrição (Automático - vira TextArea pois Length > 255 no MD)
    tsk_dsc = ui_utils.render_model_field(TaskModel, 'TskDsc')
    
    # Impacto (Select estático)
    label_imp = TaskModel.FIELDS_MD['TskImp']['LongLabel']
    tsk_imp = st.selectbox(label_imp, ["Baixo", "Médio", "Alto", "Crítico"])

    st.markdown("---")
    
    # O BOTÃO DEVE ESTAR AQUI, DENTRO DO BLOCO 'WITH ST.FORM'
    submitted = st.form_submit_button("💾 Salvar Tarefa", type="primary")

# --- FIM DO FORMULÁRIO --- (Lógica de processamento fora)

if submitted:
    # Validações básicas antes de chamar o serviço
    if not tsk_ttl:
        ui_utils.show_warning_message("O Título da tarefa é obrigatório.")
    elif not tsk_ext_cod:
        ui_utils.show_warning_message("O Código Externo é obrigatório.")
    else:
        # Monta objeto com nomes de colunas do banco
        task_data = {
            'TskExtCod': tsk_ext_cod,
            'TskTtl': tsk_ttl,
            'TskDsc': tsk_dsc,
            'TskImp': tsk_imp,
            'DevCod': dev_cod if dev_cod else None, # Trata vazio como None
            'RelCod': rel_cod if rel_cod else None
        }
        
        success, message = task_service.save_task(task_data)
        
        if success:
            ui_utils.show_success_message(message)
            # Opcional: st.rerun() para limpar o form se desejar
        else:
            ui_utils.show_error_message(message)