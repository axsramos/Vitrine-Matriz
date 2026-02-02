import streamlit as st
from datetime import datetime
from collections import defaultdict

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth

# --- SERVIÇOS ---
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService

# --- METADADOS ---
from src.models.md.RelMD import RelMD
from src.models.md.TrfMD import TrfMD

# Configuração da Página
st.set_page_config(
    page_title=f"Notas de Versão | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth()

st.title("📑 Notas de Versão")

# Instância dos Serviços
rel_service = ReleaseService()
task_service = TaskService()

# --- CARREGAMENTO DE DADOS ---
# Buscamos todas as releases ordenadas (assumindo que o service traz DESC por data ou ID)
releases_data = rel_service.get_all_releases()

if not releases_data:
    st.info("Nenhuma nota de versão publicada até o momento.")
    st.stop()

# Constante de Meses para Exibição
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# --- FUNÇÕES AUXILIARES DE UI ---
def format_date(date_str):
    """Converte YYYY-MM-DD para DD/MM/YYYY de forma segura."""
    if not date_str: return "N/A"
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return str(date_str)

def get_tasks_text_list(rel_id):
    """Busca tarefas vinculadas a uma release específica."""
    # Aqui usamos o TaskService para buscar os detalhes
    tasks = task_service.get_tasks_by_release(rel_id)
    return tasks

# --- ABAS DE NAVEGAÇÃO ---
tab_historico, tab_periodo, tab_export = st.tabs(["🕒 Histórico Recente", "📅 Agrupado por Mês", "📄 Exportar PDF"])

# --- ABA 1: HISTÓRICO RECENTE ---
with tab_historico:
    st.subheader("🚀 Últimos Lançamentos")
    
    for rel in releases_data:
        # Extração de dados usando chaves do MD
        r_id = rel['RelCod']
        r_ver = rel['RelVrs']
        r_tit = rel['RelTit']
        r_dat = rel['RelDat']
        r_dsc = rel.get('RelDsc', '')

        with st.container(border=True):
            c1, c2 = st.columns([1, 5])
            
            # Coluna Esquerda: Versão
            with c1:
                st.metric(label=RelMD.FIELDS_MD['RelVrs']['Label'], value=r_ver)
                st.caption(f"📅 {format_date(r_dat)}")
            
            # Coluna Direita: Detalhes
            with c2:
                st.markdown(f"#### {r_tit}")
                if r_dsc:
                    st.write(r_dsc)
                
                # Expander para ver as tarefas (Feature List)
                with st.expander("Ver itens incluídos nesta versão"):
                    tasks = get_tasks_text_list(r_id)
                    if tasks:
                        for t in tasks:
                            # Tenta pegar status e título
                            t_tit = t.get('TrfTit', 'Sem título')
                            t_tipo = t.get('TrfTip', 'Tarefa')
                            st.markdown(f"- **[{t_tipo}]** {t_tit}")
                    else:
                        st.caption("Nenhuma tarefa listada individualmente.")

# --- ABA 2: AGRUPADO POR MÊS ---
with tab_periodo:
    st.subheader("🗓️ Linha do Tempo")
    
    # Lógica de Agrupamento (Substituindo Pandas GroupBy)
    grouped_releases = defaultdict(list)
    
    for rel in releases_data:
        raw_date = rel.get('RelDat')
        if raw_date:
            try:
                dt = datetime.strptime(str(raw_date), "%Y-%m-%d")
                key = (dt.year, dt.month)
                grouped_releases[key].append(rel)
            except ValueError:
                continue

    # Ordena chaves: Ano Decrescente, Mês Decrescente
    sorted_keys = sorted(grouped_releases.keys(), key=lambda x: (x[0], x[1]), reverse=True)

    if not sorted_keys:
        st.warning("Não foi possível agrupar as datas.")
    
    for ano, mes in sorted_keys:
        nome_mes = MESES_PT.get(mes, "Mês").upper()
        st.markdown(f"### {nome_mes} / {ano}")
        
        items = grouped_releases[(ano, mes)]
        for item in items:
            # Card Simplificado para lista mensal
            st.info(f"**v{item['RelVrs']}** - {item['RelTit']} ({format_date(item['RelDat'])})")

# --- ABA 3: EXPORTAÇÃO ---
with tab_export:
    st.subheader("🖨️ Gerar Relatório Mensal")
    st.write("Gera um arquivo PDF com todas as releases agrupadas por mês para documentação oficial.")
    
    if st.button("Gerar PDF de Notas de Versão", type="primary"):
        with st.spinner("Processando documento..."):
            # 1. Busca dados enriquecidos (método específico do release_service para relatórios)
            report_data = rel_service.get_release_details_for_report()
            
            # 2. Gera o binário do PDF
            pdf_bytes = rel_service.generate_monthly_pdf(report_data)
            
            if pdf_bytes:
                st.success("Relatório gerado com sucesso!")
                st.download_button(
                    label="⬇️ Baixar PDF",
                    data=pdf_bytes,
                    file_name=f"notas_versao_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Não foi possível gerar o PDF. Verifique se existem dados válidos.")