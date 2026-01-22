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
    # 1. Garantimos que RelDat seja datetime e removemos NaT (Not a Time)
    df_rel['RelDat'] = pd.to_datetime(df_rel['RelDat'], errors='coerce')
    df_validos = df_rel.dropna(subset=['RelDat']).copy()
    
    if df_validos.empty:
        st.warning("Sem datas válidas para agrupamento.")
    else:
        # 2. Criamos a chave de agrupamento (Ano-Mês para ordenação correta)
        df_validos['MesAnoKey'] = df_validos['RelDat'].dt.to_period('M')
        
        # 3. Ordenamos para que os meses mais recentes apareçam primeiro
        meses_ordenados = sorted(df_validos['MesAnoKey'].unique(), reverse=True)

        for mes in meses_ordenados:
            # Filtramos as releases deste mês específico
            subset = df_validos[df_validos['MesAnoKey'] == mes]
            
            # Exibição do Header do Mês (Ex: DEZEMBRO / 2025)
            nome_mes = subset['RelDat'].iloc[0].strftime('%B / %Y').upper()
            st.subheader(f"🗓️ {nome_mes}")
            
            for _, row in subset.iterrows():
                devs = row['Desenvolvedores'] if row['Desenvolvedores'] else "Equipe"
                qtd = row['QtdTarefas']
                
                # Card resumido da release
                with st.container(border=True):
                    c1, c2 = st.columns([1, 4])
                    c1.metric("Versão", row['RelVrs'])
                    with c2:
                        st.markdown(f"**{row['RelTtlCmm'] or 'Sem título'}**")
                        st.caption(f"📅 {row['RelDat'].strftime('%d/%m/%Y')} | 👥 {devs} | 📊 {qtd} tarefas")
            st.divider()