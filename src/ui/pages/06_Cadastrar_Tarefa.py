import streamlit as st
from src.models.tarefa import Tarefa
from src.services.dev_service import DevService
from src.services.release_service import ReleaseService
from src.core import config
from src.core.auth_middleware import require_auth
from src.core.ui_utils import init_page

require_auth()

init_page("Lançamento de Tarefas", "centered")
    
st.title("➕ Lançamento de Tarefas")
st.markdown("Utilize este formulário para registrar entregas de forma manual ou em regime de contingência.")

# 1. Carregamento de Dados (Serviços)
dev_service = DevService()
rel_service = ReleaseService()

df_devs = dev_service.get_team_stats()
df_rels = rel_service.get_all_releases()

if df_devs.empty:
    st.warning("⚠️ Cadastre ao menos um desenvolvedor antes de lançar tarefas.")
    st.stop()

# 2. Preparação dos Mapeamentos (Combos)
# Criamos a lista de desenvolvedores
dev_map = {row['nome']: row['id'] for _, row in df_devs.iterrows()}

# Criamos a lista de releases incluindo a opção nula no topo
rel_options = ["-- Sem versão (Aguardo) --"] + list(df_rels['versao'].tolist())
rel_map = {row['versao']: row['id'] for _, row in df_rels.iterrows()}
rel_map["-- Sem versão (Aguardo) --"] = None  # No SQLite, None será inserido como NULL

# 3. Formulário de Cadastro
with st.form("form_cadastro_tarefa", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input("Título da Entrega", placeholder="Ex: Otimização do SQL de Login")
        bitrix_id = st.number_input("ID de Referência (Opcional)", min_value=0, value=0)
        
    with col2:
        dev_selecionado = st.selectbox("Desenvolvedor Responsável", options=list(dev_map.keys()))
        rel_selecionada = st.selectbox("Vincular à Release", options=rel_options)

    desc_tecnica = st.text_area("Descrição Técnica", help="Detalhes sobre o que foi alterado no código.")
    impacto_negocio = st.text_area("Impacto para o Negócio", help="Explique o valor gerado para o cliente ou gestor.")
    
    submit = st.form_submit_button("🚀 Gravar Entrega")

# 4. Processamento da Persistência
if submit:
    if not titulo or not desc_tecnica:
        st.error("Campos 'Título' e 'Descrição Técnica' são obrigatórios.")
    else:
        # Instancia o modelo com os IDs mapeados
        nova_tarefa = Tarefa({
            "bitrix_task_id": bitrix_id if bitrix_id > 0 else None,
            "titulo": titulo,
            "descricao_tecnica": desc_tecnica,
            "impacto_negocio": impacto_negocio,
            "id_desenvolvedor": dev_map[dev_selecionado],
            "id_release": rel_map[rel_selecionada] # Envia None se for "Sem versão"
        })
        
        # Persistência via CrudMixin
        if nova_tarefa.create():
            st.success(f"Tarefa '{titulo}' registrada com sucesso!")
            st.balloons()
        else:
            st.error("Erro ao salvar a tarefa no banco de dados.")

st.divider()
st.info("💡 Tarefas marcadas como '-- Sem versão --' aparecerão agrupadas em 'Aguardando Release' nas Notas de Versão.")