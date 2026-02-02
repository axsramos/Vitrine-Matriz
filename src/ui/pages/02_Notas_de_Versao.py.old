import streamlit as st
import pandas as pd
from src.services.release_service import ReleaseService
from src.core.auth_middleware import require_auth
from datetime import datetime

# require_auth()

st.title("📑 Notas de Versão")

rel_service = ReleaseService()
data = rel_service.get_release_details()

if not data:
    st.info("Nenhuma nota de versão cadastrada.")
    st.stop()

df_rel = pd.DataFrame(data)
df_rel['RelDat'] = pd.to_datetime(df_rel['RelDat'], errors='coerce')

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

tab_historico, tab_periodo = st.tabs(["🕒 Histórico Recente", "📅 Agrupado por Mês"])

def exibir_card_release(row):
    """Padronização visual dos cards na tela (Mimetizando Bitrix24)"""
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        col1.metric("Versão", row['RelVrs'])
        with col2:
            st.markdown(f"#### {row['RelTtlCmm'] or 'Sem título'}")
            st.caption(f"📅 {row['RelDat'].strftime('%d/%m/%Y')} | 👥 {row.get('Desenvolvedores') or 'Equipe'}")
            
            if row.get('ListaTarefas'):
                with st.expander("Ver itens desta release"):
                    tarefas = str(row['ListaTarefas']).split('||')
                    for t in tarefas:
                        st.markdown(f"- {t}")

# --- ABA 1: HISTÓRICO RECENTE ---
with tab_historico:
    st.subheader("🚀 Histórico de Lançamentos")
    for _, row in df_rel.iterrows():
        exibir_card_release(row)

# --- ABA 2: AGRUPADO POR MÊS ---
with tab_periodo:
    df_v = df_rel.dropna(subset=['RelDat']).copy()
    
    if not df_v.empty:
        df_v['Ano'] = df_v['RelDat'].dt.year
        df_v['MesNum'] = df_v['RelDat'].dt.month
        
        # Ordenação para os meses mais recentes aparecerem primeiro
        grupos = df_v.sort_values(['Ano', 'MesNum'], ascending=False).groupby(['Ano', 'MesNum'], sort=False)

        for (ano, mes_num), subset in grupos:
            st.subheader(f"🗓️ {MESES_PT.get(mes_num)} / {ano}")
            for _, row in subset.iterrows():
                exibir_card_release(row)