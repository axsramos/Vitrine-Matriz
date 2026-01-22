import streamlit as st
import pandas as pd
from src.services.release_service import ReleaseService
from src.core.auth_middleware import require_auth

# require_auth()

st.title("📑 Notas de Versão")

rel_service = ReleaseService()
# Chamada ao novo método que traz os agregados de tarefas e devs
data = rel_service.get_release_details()

if data is None or (isinstance(data, pd.DataFrame) and data.empty) or (isinstance(data, list) and not data):
    st.info("Nenhuma nota de versão cadastrada.")
    st.stop()

df_rel = pd.DataFrame(data)
df_rel['RelDat'] = pd.to_datetime(df_rel['RelDat'], errors='coerce')

tab_padrao, tab_periodo = st.tabs(["🕒 Histórico Recente", "📅 Agrupado por Mês"])

# --- ABA 1: VISUALIZAÇÃO PADRÃO ---
with tab_padrao:
    for _, row in df_rel.iterrows():
        data_fmt = row['RelDat'].strftime('%d/%m/%Y') if pd.notnull(row['RelDat']) else "S/D"
        devs = row['Desenvolvedores'] if row['Desenvolvedores'] else "Não identificado"
        qtd = row['QtdTarefas']
        
        with st.expander(f"📦 Versão {row['RelVrs']} — {data_fmt}"):
            # Informações de entrega em destaque
            col1, col2 = st.columns(2)
            col1.info(f"👥 **Devs:** {devs}")
            col2.info(f"📊 **Entregas:** {qtd} tarefas")
            
            st.markdown(f"**Comentários da Release:**")
            st.write(row['RelTtlCmm'] if row['RelTtlCmm'] else "Sem descrição.")

# --- ABA 2: VISUALIZAÇÃO POR MÊS/ANO ---
with tab_periodo:
    df_validos = df_rel[df_rel['RelDat'].notnull()].copy()
    
    if df_validos.empty:
        st.warning("Sem datas válidas para agrupamento.")
    else:
        df_validos['MesAno'] = df_validos['RelDat'].dt.strftime('%Y-%m')
        for mes in df_validos['MesAno'].unique():
            data_ref = df_validos[df_validos['MesAno'] == mes]['RelDat'].iloc[0]
            st.subheader(f"🗓️ {data_ref.strftime('%B / %Y').capitalize()}")
            
            subset = df_validos[df_validos['MesAno'] == mes]
            for _, row in subset.iterrows():
                # Linha resumida para visualização mensal
                st.markdown(f"**{row['RelVrs']}** ({row['RelDat'].strftime('%d/%m')}) — `{row['QtdTarefas']} tarefa(s)` por: *{row['Desenvolvedores']}*")
                st.caption(f"📝 {row['RelTtlCmm']}")
            st.divider()