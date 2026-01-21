import streamlit as st
import os
from src.core.config import Config
from src.core.database import Database
from src.core.auth_middleware import require_auth
from src.core import ui_utils

# Apenas administradores podem alterar configurações globais
require_auth(allowed_roles=['admin'])

st.title("🛠️ Configurações do Sistema")
st.write("Gerencie os parâmetros globais e a identidade visual da plataforma.")

db = Database()

# --- ABA 1: IDENTIDADE VISUAL ---
tab_visual, tab_banco, tab_info = st.tabs(["Identidade Visual", "Banco de Dados", "Informações do Sistema"])

with tab_visual:
    st.subheader("Personalização")
    with st.form("form_visual"):
        app_title = st.text_input("Título da Aplicação", value=Config.APP_TITLE)
        app_subtitle = st.text_input("Subtítulo/Slogan", value=Config.APP_SUBTITLE)
        
        st.info("💡 As alterações nos títulos e logotipos serão refletidas após o reinício da aplicação.")
        
        if st.form_submit_button("Salvar Identidade", type="primary"):
            # Aqui você pode implementar a lógica para gravar no .env ou em uma tabela T_Cfg
            st.success("Configurações visuais enviadas para processamento.")

with tab_banco:
    st.subheader("Status do Banco de Dados")
    col1, col2 = st.columns(2)
    
    # Busca estatísticas reais das tabelas revisadas
    try:
        total_usr = db.select("SELECT COUNT(*) as total FROM T_Usr")[0]['total']
        total_trf = db.select("SELECT COUNT(*) as total FROM T_Trf")[0]['total']
        total_rel = db.select("SELECT COUNT(*) as total FROM T_Rel")[0]['total']
        total_dev = db.select("SELECT COUNT(*) as total FROM T_Dev")[0]['total']
        
        col1.metric("Usuários Cadastrados", total_usr)
        col1.metric("Desenvolvedores no Time", total_dev)
        col2.metric("Total de Tarefas", total_trf)
        col2.metric("Releases Publicadas", total_rel)
    except Exception as e:
        st.error(f"Erro ao ler estatísticas: {e}")

    st.divider()
    st.subheader("Manutenção")
    if st.button("📦 Realizar Backup do Banco"):
        st.warning("Funcionalidade em desenvolvimento: O arquivo vitrine.db será compactado.")

with tab_info:
    st.subheader("Ambiente de Execução")
    st.text(f"Diretório Raiz: {Config.BASE_DIR}")
    st.text(f"Caminho do Banco: {Config.DB_STR_PATH}")
    st.text(f"Pasta de Uploads: {Config.AVATAR_PATH}")
    st.text(f"Ambiente: {Config.ENV.upper()}")
    
    st.divider()
    st.caption("Vitrine-Matriz Framework | 2026")