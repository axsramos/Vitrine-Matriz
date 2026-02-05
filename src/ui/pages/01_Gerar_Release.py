import streamlit as st
from datetime import date

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService
from src.models.md.RelMD import RelMD
from src.models.md.TrfMD import TrfMD
from src.models.md.DevMD import DevMD
from src.models.UserRole import UserRole
from src.models.TaskStatus import TaskStatus

# Configuração da Página
st.set_page_config(
    page_title=f"Gerar Release | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança (Admin, Manager e Devs podem gerar release)
require_auth(allowed_roles=[UserRole.ADMIN, UserRole.MANAGER, UserRole.DEVELOPMENT])

# --- CABEÇALHO ---
st.title("📦 Gerar Nova Release")
st.write("Consolide as tarefas concluídas em uma nova versão oficial do sistema.")

# Instanciação dos Serviços
rel_service = ReleaseService()
task_service = TaskService()

# Identificação da Versão Atual
all_releases = rel_service.get_all_releases()
versao_atual = all_releases[0]['RelVrs'] if all_releases else "Inicial"

st.info(f"📢 **Última Versão Lançada:** {versao_atual}")
st.divider()

# --- SEÇÃO 1: LISTAGEM DE TAREFAS ELEGÍVEIS ---
# Busca tarefas que estão CONCLUÍDAS mas ainda SEM RELEASE
# Usamos o método get_detailed_tasks para ter o JOIN com Dev e Release
pending_tasks = task_service.get_detailed_tasks(
    where="t.TrfSit = ? AND t.TrfRelCod IS NULL",
    params=(TaskStatus.CONCLUIDO.value,)
    
)

if not pending_tasks:
    st.info("✨ Não há tarefas concluídas aguardando release no momento.")
else:
    st.subheader("📋 Tarefas para inclusão")
    
    # Preparação dos dados para exibição (Mapeamento Dicionário -> Colunas Visuais)
    # Aqui criamos uma lista simplificada apenas com o que queremos mostrar na tabela
    display_data = []
    for t in pending_tasks:
        display_data.append({
            TrfMD.FIELDS_MD['TrfCod']['Label']: t['TrfCod'],         # ID
            TrfMD.FIELDS_MD['TrfTit']['Label']: t['TrfTit'],         # Título
            DevMD.FIELDS_MD['DevNom']['Label']: t['NomeDesenvolvedor'], # Responsável
            "Conclusão": t.get('TrfDatEnt') or "N/A"                 # Data Entrega (campo não obrigatório no MD)
        })
    
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"Total de tarefas selecionadas: {len(display_data)}")
    st.divider()

    # --- SEÇÃO 2: FORMULÁRIO DE GERAÇÃO ---
    with st.form("form_release", clear_on_submit=True):
        st.subheader("Dados da Versão")
        
        c1, c2 = st.columns(2)
        
        # Campo VERSÃO
        with c1:
            lbl_vrs = RelMD.FIELDS_MD['RelVrs']['Label']
            req_vrs = RelMD.FIELDS_MD['RelVrs']['Required']
            versao_input = st.text_input(
                f"{lbl_vrs} {'*' if req_vrs else ''}", 
                placeholder="Ex: 1.2.0"
            )
            
        # Campo DATA
        with c2:
            lbl_dat = RelMD.FIELDS_MD['RelDat']['Label']
            data_input = st.date_input(lbl_dat, value=date.today())
            
        # Campo TÍTULO
        lbl_tit = RelMD.FIELDS_MD['RelTit']['Label']
        req_tit = RelMD.FIELDS_MD['RelTit']['Required']
        titulo_input = st.text_input(f"{lbl_tit} {'*' if req_tit else ''}", placeholder="Ex: Atualização de Segurança")
        
        # Botão de Ação
        submitted = st.form_submit_button("🚀 Publicar Release", type="primary", use_container_width=True)

        if submitted:
            # Validação Básica
            if not versao_input or not titulo_input:
                st.error("Por favor, preencha a Versão e o Título.")
            else:
                # 1. Cria a Release
                success, msg = rel_service.create_release(
                    titulo=titulo_input,
                    versao=versao_input,
                    data_publicacao=data_input.strftime('%Y-%m-%d')
                )
                
                if success:
                    # 2. Recupera o ID da Release recém-criada
                    # (Como create retorna boolean, buscamos pelo numero da versão para pegar o ID)
                    new_rel = rel_service.get_release_by_version(versao_input)
                    
                    if new_rel:
                        rel_id = new_rel['RelCod']
                        count_tasks = 0
                        
                        # 3. Vincula as tarefas listadas à nova Release
                        for t in pending_tasks:
                            task_id = t['TrfCod']
                            if task_service.assign_release(task_id, rel_id):
                                count_tasks += 1
                        
                        st.success(f"Sucesso! Release {versao_input} criada com {count_tasks} tarefas vinculadas.")
                        # Aguarda interação do usuário ou usa st.rerun() se disponível na versão
                        st.balloons()
                    else:
                        st.warning("Release criada, mas houve erro ao recuperar o ID para vincular tarefas.")
                else:
                    st.error(msg)