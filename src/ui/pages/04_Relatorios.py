import streamlit as st
import pandas as pd
from src.services.release_service import ReleaseService
from datetime import datetime

st.title("📊 Relatórios de Versão")

rel_service = ReleaseService()
data = rel_service.get_release_details() # MESMA FUNÇÃO DA TELA DE NOTAS

if data:
    df = pd.DataFrame(data)
    df['RelDat'] = pd.to_datetime(df['RelDat'])

    MESES_PT = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("Histórico Geral")
            st.write("Relatório detalhado por ordem cronológica.")
            pdf_g = rel_service.export_pdf_geral_direto(df)
            if pdf_g:
                st.download_button("📥 Baixar Geral", pdf_g, "geral.pdf", "application/pdf", key="g", use_container_width=True)

    with col2:
        with st.container(border=True):
            st.subheader("Resumo Mensal")
            st.write("Relatório executivo agrupado por mês.")
            pdf_m = rel_service.export_pdf_mensal_direto(df, MESES_PT)
            if pdf_m:
                st.download_button("🗓️ Baixar Mensal", pdf_m, "mensal.pdf", "application/pdf", key="m", use_container_width=True)
else:
    st.warning("Nenhuma informação disponível para gerar relatórios.")