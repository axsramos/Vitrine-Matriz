import streamlit as st

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth
from src.models.UserRole import UserRole

# --- SERVIÇOS ---
# Importamos o novo serviço criado
from src.services.system_service import SystemService

# Configuração da Página
st.set_page_config(
    page_title=f"Configurações | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso (Apenas Admin)
require_auth(allowed_roles=[UserRole.ADMIN])

st.title("🛠️ Configurações do Sistema")
st.write("Gerencie parâmetros globais, backups e identidade visual.")

# Instância do Serviço
sys_service = SystemService()

# --- NAVEGAÇÃO ---
tab_visual, tab_backup, tab_info = st.tabs([
    "🎨 Identidade Visual", 
    "💾 Banco de Dados", 
    "ℹ️ Sistema"
])

# --- ABA 1: IDENTIDADE VISUAL ---
with tab_visual:
    st.subheader("Personalização")
    st.caption("Defina como a aplicação é apresentada aos usuários.")
    
    with st.form("form_visual"):
        # Labels fixos pois referem-se a config de sistema, não a banco
        app_title = st.text_input("Nome da Aplicação", value=Config.APP_TITLE)
        app_subtitle = st.text_input("Slogan / Subtítulo", value=Config.APP_SUBTITLE)
        
        st.info("💡 Nota: Para tornar estas alterações permanentes, é necessário implementar persistência em arquivo .env ou tabela T_Cfg.")
        
        if st.form_submit_button("Aplicar Alterações", type="primary"):
            # Aqui entraria a chamada para sys_service.update_config(...)
            st.success("Configurações visuais enviadas (Simulação).")

# --- ABA 2: BACKUP E MANUTENÇÃO ---
with tab_backup:
    st.subheader("Segurança de Dados")
    
    col_warn, col_action = st.columns([2, 1])
    
    with col_warn:
        st.warning(
            """
            **Atenção:** O backup realiza uma cópia física do arquivo SQLite.
            Recomenda-se realizar esta operação antes de grandes atualizações ou importações de dados.
            """
        )
    
    with col_action:
        st.write("###") # Espaçamento
        if st.button("🚀 Gerar Backup Agora", use_container_width=True):
            with st.spinner("Processando cópia de segurança..."):
                success, msg = sys_service.create_database_backup()
                
                if success:
                    st.toast("Backup realizado!", icon="✅")
                    st.success(msg)
                else:
                    st.error(msg)

# --- ABA 3: INFORMAÇÕES DO SISTEMA ---
with tab_info:
    st.subheader("Ambiente de Execução")
    
    info_data = sys_service.get_system_info()
    
    # Exibição formatada
    for key, value in info_data.items():
        with st.container(border=True):
            c1, c2 = st.columns([1, 3])
            c1.caption(key)
            c2.code(value, language="text")