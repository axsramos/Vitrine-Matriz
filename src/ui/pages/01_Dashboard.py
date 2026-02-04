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
all_releases = rel_service.get_all_releases()
last_rel = all_releases[0] if all_releases else {}

versao_txt = last_rel.get('RelVrs', 'N/A')
data_txt = last_rel.get('RelDat')
if data_txt:
    try:
        data_txt = datetime.strptime(str(data_txt), "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        pass
else:
    data_txt = "N/A"

# Container estilizado do Topo
with st.container():
    c1, c2, c3 = st.columns([1, 3, 1])
    
    # Versão
    lbl_versao = RelMD.FIELDS_MD.get('RelVrs', {}).get('Label', 'Versão')
    c1.metric(label=lbl_versao, value=versao_txt)
    
    c2.info(f"**Última Atualização em {data_txt}**")
    
    # Situação
    lbl_sit = RelMD.FIELDS_MD.get('RelSit', {}).get('Label', 'Situação')
    c3.metric(label=lbl_sit, value=last_rel.get('RelSit', '-'))

st.divider()

# --- KPI's (Métricas Principais) ---
kpis = dash_service.get_kpis()

col_k1, col_k2, col_k3, col_k4 = st.columns(4)
col_k1.metric("Tarefas Abertas", kpis['total_open'])
col_k2.metric("Tarefas Concluídas", kpis['total_closed'])
col_k3.metric("Releases Publicadas", kpis['total_releases'])
col_k4.metric("Devs Ativos", kpis['active_devs'])

st.divider()

# --- GRÁFICOS ---
# Layout de gráficos: Esquerda (Barras), Direita (Pizza)
g_col1, g_col2 = st.columns([2, 1])

# 1. Gráfico de Tarefas por Desenvolvedor (Barras)
with g_col1:
    st.subheader("Produtividade por Dev")
    data_dev = dash_service.get_tasks_by_dev()
    
    if not data_dev:
        st.info("Sem dados para exibir.")
    else:
        # CORREÇÃO AQUI: Adicionado :N e :Q
        bar = alt.Chart(alt.Data(values=data_dev)).mark_bar().encode(
            x=alt.X('Desenvolvedor:N', title='Desenvolvedor', sort='-y'), # :N = Nominal (Texto)
            y=alt.Y('Tarefas:Q', title='Qtd. Tarefas'),                   # :Q = Quantitativo (Número)
            tooltip=['Desenvolvedor:N', 'Tarefas:Q']
        ).properties(height=300)
        
        st.altair_chart(bar, use_container_width=True)

# 2. Gráfico de Tarefas por Status (Donut)
with g_col2:
    st.subheader("Distribuição de Status")
    data_status = dash_service.get_tasks_by_status()
    
    if not data_status:
        st.info("Sem dados.")
    else:
        # CORREÇÃO AQUI: Adicionado :Q e :N
        base = alt.Chart(alt.Data(values=data_status)).encode(
            theta=alt.Theta("Quantidade:Q", stack=True) # :Q = Quantitativo
        )
        
        pie = base.mark_arc(outerRadius=100, innerRadius=50).encode(
            color=alt.Color("Status:N"),                # :N = Nominal
            order=alt.Order("Quantidade:Q", sort="descending"),
            tooltip=["Status:N", "Quantidade:Q"]
        ).properties(height=300)
        
        st.altair_chart(pie, use_container_width=True)

# --- ATIVIDADE RECENTE ---
st.divider()
st.subheader("🕒 Atividade Recente")

recent_activity = dash_service.get_recent_activity(limit=5)

if recent_activity:
    # Cabeçalho usando MD
    c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 2])
    c1.caption(f"**{TrfMD.FIELDS_MD['TrfTit']['Label']}**")
    c2.caption(f"**{TrfMD.FIELDS_MD['TrfStt']['Label'] if 'TrfStt' in TrfMD.FIELDS_MD else 'Status'}**")
    c3.caption("**Data**")
    c4.caption(f"**{DevMD.FIELDS_MD['DevNom']['Label']}**")
    
    for item in recent_activity:
        with st.container(border=True):
            rc1, rc2, rc3, rc4 = st.columns([3, 1.5, 1.5, 2])
            rc1.write(item.get('Tarefa', '-'))
            
            # Badge simples de status
            status = item.get('Status', 'N/A')
            status_color = "green" if status == 'Concluído' else "orange"
            rc2.markdown(f":{status_color}[{status}]")
            
            # Formatação de data
            data_raw = item.get('Data')
            data_fmt = data_raw
            if data_raw:
                try:
                    data_fmt = datetime.strptime(str(data_raw), "%Y-%m-%d %H:%M:%S").strftime("%d/%m %H:%M")
                except:
                    pass
            rc3.write(data_fmt)
            
            rc4.write(item.get('Dev', '-'))
else:
    st.info("Nenhuma atividade registrada recentemente.")