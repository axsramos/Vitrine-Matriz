import streamlit as st
import altair as alt
from datetime import datetime

# Serviços e Configurações
from src.core.config import Config
from src.core.auth_middleware import require_auth
from src.services.dashboard_service import DashboardService
from src.services.release_service import ReleaseService

# Metadados para Labels Padronizados
from src.models.md.TrfMD import TrfMD
from src.models.md.RelMD import RelMD
from src.models.md.DevMD import DevMD

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(
    page_title=f"Dashboard | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth()

st.title("📊 Painel de Controle")

# Instância dos Serviços
dash_service = DashboardService()
rel_service = ReleaseService()

# --- HEADER (Informações da Versão) ---
# Busca todas as releases para pegar a mais recente (index 0 se ordenado por data DESC)
all_releases = rel_service.get_all_releases() # O service já ordena por padrão? Assumindo que sim ou filtrando.
# Nota: Para garantir a última, idealmente o service teria um get_last, 
# mas vamos pegar a primeira da lista assumindo ordenação do Model.
last_rel = all_releases[0] if all_releases else {}

versao_txt = last_rel.get('RelVrs', 'N/A')
data_raw = last_rel.get('RelDat')
data_txt = 'N/A'

if data_raw:
    try:
        # Tenta parsear formato do banco
        dt_obj = datetime.strptime(str(data_raw), "%Y-%m-%d")
        data_txt = dt_obj.strftime("%d/%m/%Y")
    except ValueError:
        data_txt = str(data_raw)

# Container estilizado do Topo
with st.container():
    c1, c2, c3 = st.columns([1, 3, 1])
    # Label vindo do MD: RelVrs -> "Versão"
    c1.metric(label=RelMD.FIELDS_MD['RelVrs']['Label'], value=versao_txt)
    c2.info(f"**Última Atualização em {data_txt}**")
    # Label vindo do MD: RelSit -> "Situação"
    c3.metric(label=RelMD.FIELDS_MD['RelSit']['Label'], value=last_rel.get('RelSit', '-'))

st.divider()

# --- KPIS (Indicadores Gerais) ---
stats = dash_service.get_general_stats()

k1, k2, k3 = st.columns(3)
k1.metric("Tarefas Totais", stats.get('total_tasks', 0))
k2.metric("Pendentes (Backlog)", stats.get('pending_tasks', 0))
k3.metric("Releases Abertas", stats.get('active_releases', 0))

st.divider()

# --- GRÁFICOS (Altair sem Pandas) ---
col_gf1, col_gf2 = st.columns(2)

with col_gf1:
    # Título usando Label do MD: TrfStt -> "Situação"
    st.subheader(f"Distribuição por {TrfMD.FIELDS_MD['TrfStt']['Label']}")
    
    data_status = dash_service.get_task_status_distribution()
    # data_status = [{'Status': 'Aberto', 'Quantidade': 10}, ...]

    if data_status:
        base = alt.Chart(alt.Data(values=data_status)).encode(
            theta=alt.Theta("Quantidade:Q", stack=True)
        )
        
        pie = base.mark_arc(outerRadius=120).encode(
            color=alt.Color("Status:N"),
            order=alt.Order("Quantidade:Q", sort="descending"),
            tooltip=["Status", "Quantidade"]
        )
        
        text = base.mark_text(radius=140).encode(
            text=alt.Text("Quantidade:Q"),
            order=alt.Order("Quantidade:Q", sort="descending"),
            color=alt.value("black")
        )
        
        st.altair_chart(pie + text, use_container_width=True)
    else:
        st.info("Sem dados para exibir.")

with col_gf2:
    st.subheader("⚖️ Carga de Trabalho")
    
    data_workload = dash_service.get_dev_workload()
    # data_workload = [{'Desenvolvedor': 'Nome', 'Total': 5}, ...]

    if data_workload:
        # Label do MD: DevNom -> "Nome Completo" (ou similar)
        label_dev = DevMD.FIELDS_MD['DevNom']['Label']
        
        bar = alt.Chart(alt.Data(values=data_workload)).mark_bar().encode(
            x=alt.X('Total:Q', title='Qtd Tarefas'),
            y=alt.Y('Desenvolvedor:N', title=label_dev, sort='-x'),
            color=alt.value('#4c78a8'),
            tooltip=['Desenvolvedor', 'Total']
        ).properties(height=300)
        
        st.altair_chart(bar, use_container_width=True)
    else:
        st.caption("Nenhum registro de carga de trabalho.")

# --- MATRIZ DE PRIORIDADE ---
st.subheader("🎯 Matriz de Prioridade vs Impacto")
data_matrix = dash_service.get_priority_impact_matrix()

if data_matrix:
    # Labels do MD
    lbl_prio = TrfMD.FIELDS_MD['TrfPri']['Label'] # Prioridade
    lbl_imp = TrfMD.FIELDS_MD['TrfImp']['Label']  # Impacto (se existir no MD, caso contrário string fixa)
    
    # Heatmap
    heatmap = alt.Chart(alt.Data(values=data_matrix)).mark_rect().encode(
        x=alt.X('Prioridade:N', title=lbl_prio),
        y=alt.Y('Impacto:N', title="Impacto"), # Ajustar se houver TrfImp no MD
        color=alt.Color('Total:Q', legend=None),
        tooltip=['Prioridade', 'Impacto', 'Total']
    )
    
    text_mat = heatmap.mark_text().encode(
        text='Total:Q',
        color=alt.value('white')
    )
    
    st.altair_chart(heatmap + text_mat, use_container_width=True)

# --- TABELA DE ATIVIDADE RECENTE ---
st.divider()
st.subheader("🕒 Atividade Recente")

recent_activity = dash_service.get_recent_activity(limit=5)

if recent_activity:
    # Mapeamento manual simples para tabela visual
    # Poderíamos usar st.dataframe, mas st.table ou colunas ficam mais limpos para poucos dados
    
    # Cabeçalho usando MD
    c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 2])
    c1.caption(f"**{TrfMD.FIELDS_MD['TrfTit']['Label']}**")
    c2.caption(f"**{TrfMD.FIELDS_MD['TrfStt']['Label']}**")
    c3.caption("**Data**") # Data geralmente é auditoria
    c4.caption(f"**{DevMD.FIELDS_MD['DevNom']['Label']}**")
    
    for item in recent_activity:
        with st.container(border=True):
            rc1, rc2, rc3, rc4 = st.columns([3, 1.5, 1.5, 2])
            rc1.write(item['Tarefa'])
            
            # Badge simples de status
            status_color = "green" if item['Status'] == 'Concluído' else "orange"
            rc2.markdown(f":{status_color}[{item['Status']}]")
            
            # Formatação de data
            data_fmt = item['Data']
            try:
                if data_fmt:
                    d = datetime.strptime(str(data_fmt), "%Y-%m-%d %H:%M:%S")
                    data_fmt = d.strftime("%d/%m %H:%M")
            except:
                pass
            rc3.write(data_fmt)
            
            rc4.write(item['Autor'] if item['Autor'] else "N/A")

else:
    st.info("Nenhuma atividade recente registrada.")