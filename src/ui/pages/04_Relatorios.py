import streamlit as st
import pandas as pd
from src.services.release_service import ReleaseService
from datetime import datetime

st.set_page_config(page_title="Central de Relatórios", page_icon="📊")

st.title("📊 Central de Relatórios")
st.markdown("Selecione o relatório desejado para gerar o documento oficial em PDF.")

rel_service = ReleaseService()
data = rel_service.get_release_details()

if not data:
    st.warning("Não há dados suficientes para gerar relatórios.")
    st.stop()

df = pd.DataFrame(data)
df['RelDat'] = pd.to_datetime(df['RelDat'], errors='coerce')

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Notas de Versão Geral")
        st.write("Exibe o histórico completo de lançamentos de forma cronológica.")
        pdf_geral = rel_service.export_pdf_geral(df)
        if pdf_geral:
            st.download_button(
                label="📄 Gerar PDF Geral",
                data=pdf_geral,
                file_name=f"notas_versao_geral_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                width='stretch'
            )

with col2:
    with st.container(border=True):
        st.subheader("Notas de Versão Mensal")
        st.write("Agrupa as entregas por Mês e Ano para visão gerencial.")
        df_v = df.dropna(subset=['RelDat']).copy()
        pdf_mensal = rel_service.export_pdf_mensal(df_v, MESES_PT)
        if pdf_mensal:
            st.download_button(
                label="🗓️ Gerar PDF Mensal",
                data=pdf_mensal,
                file_name=f"notas_versao_mensal_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                width='stretch'
            )