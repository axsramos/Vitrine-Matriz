import streamlit as st

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth

# --- SERVIÇOS ---
from src.services.user_service import UserService
from src.services.dev_service import DevService

# --- METADADOS ---
from src.models.md.UsrMD import UsrMD
from src.models.UserRole import UserRole

# Configuração da Página
st.set_page_config(
    page_title=f"Gerenciar Usuários | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso (Apenas Admins)
require_auth(allowed_roles=[UserRole.ADMIN])

st.title("👥 Gerenciar Usuários")
st.write("Administração centralizada de acessos e permissões.")

# Instância dos Serviços
user_service = UserService()
dev_service = DevService()

# --- FORMULÁRIO DE CADASTRO ---
with st.expander("➕ Cadastrar Novo Usuário", expanded=False):
    with st.form("form_registro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        
        with c1:
            # Login
            lbl_lgn = UsrMD.FIELDS_MD['UsrLgn']['Label']
            req_lgn = UsrMD.FIELDS_MD['UsrLgn']['Required']
            new_lgn = st.text_input(f"{lbl_lgn} {'*' if req_lgn else ''}")
            
            # Nome
            lbl_nom = UsrMD.FIELDS_MD['UsrNom']['Label']
            req_nom = UsrMD.FIELDS_MD['UsrNom']['Required']
            new_nom = st.text_input(f"{lbl_nom} {'*' if req_nom else ''}")
            
        with c2:
            # Senha (Campo especial, sem MD direto para 'Label' de input de senha, usamos fixo ou adaptado)
            new_pwd = st.text_input("Senha Inicial *", type="password")
            
            # Permissão (Enum)
            lbl_prm = UsrMD.FIELDS_MD['UsrPrm']['Label']
            new_prm = st.selectbox(lbl_prm, options=UserRole.list())
        
        # Botão de Ação
        if st.form_submit_button("💾 Salvar Usuário", type="primary", use_container_width=True):
            if not new_lgn or not new_pwd:
                st.warning("Login e Senha são obrigatórios.")
            else:
                success, msg = user_service.create_user(new_lgn, new_nom, new_pwd, new_prm)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

st.divider()

# --- LISTAGEM DE USUÁRIOS ---
st.subheader("📋 Usuários Ativos")

# Busca dados via serviço
usuarios = user_service.get_all_users()

if not usuarios:
    st.info("Nenhum usuário encontrado.")
else:
    # Cabeçalho visual da lista
    cols_header = st.columns([2, 1.5, 1, 2.5])
    cols_header[0].caption(f"**{UsrMD.FIELDS_MD['UsrNom']['Label']}**")
    cols_header[1].caption(f"**{UsrMD.FIELDS_MD['UsrLgn']['Label']}**")
    cols_header[2].caption(f"**{UsrMD.FIELDS_MD['UsrPrm']['Label']}**")
    cols_header[3].caption("**Ações**")
    
    for u in usuarios:
        u_id = u['UsrCod']
        u_nome = u['UsrNom']
        
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 1.5, 1, 2.5])
            
            # Colunas de Dados
            c1.write(f"**{u_nome}**")
            c2.write(u['UsrLgn'])
            
            # Badge de Permissão
            role = u['UsrPrm']
            color = "red" if role == 'admin' else "blue" if role == 'manager' else "green"
            c3.markdown(f":{color}[{role.upper()}]")
            
            # Coluna de Ações (Botões)
            # Verifica se já é desenvolvedor para desabilitar/alterar botão de promoção
            is_dev = dev_service.check_if_user_is_dev(u_id)
            
            col_b1, col_b2, col_b3 = c4.columns(3)
            
            # 1. Botão PROMOVER (Dev)
            if not is_dev:
                if col_b1.button("🚀 Dev", key=f"dev_{u_id}", help="Promover a Desenvolvedor"):
                    success, msg = dev_service.create_dev_from_user(u_id, u_nome)
                    if success:
                        st.toast(msg, icon="✅")
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                col_b1.button("✅ Dev", key=f"isdev_{u_id}", disabled=True, help="Já é desenvolvedor")

            # 2. Botão RESET SENHA
            if col_b2.button("🔑 Reset", key=f"rst_{u_id}", help="Resetar senha para '123'"):
                if user_service.reset_password(u_id):
                    st.toast(f"Senha de {u_nome} resetada para '123'", icon="🔄")
                else:
                    st.error("Erro ao resetar senha.")

            # 3. Botão EXCLUIR
            # Proteção para não excluir o próprio admin logado
            meu_id = st.session_state['user']['UsrCod']
            if u_id != meu_id:
                if col_b3.button("🗑️", key=f"del_{u_id}", type="primary", help="Excluir Usuário"):
                    if user_service.delete_user(u_id):
                        st.toast(f"Usuário {u_nome} removido.", icon="🗑️")
                        st.rerun()
                    else:
                        st.error("Erro ao excluir.")
            else:
                col_b3.write("") # Espaço vazio para manter alinhamento