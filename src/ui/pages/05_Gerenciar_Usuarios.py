import streamlit as st
from src.services.user_service import UserService
from src.services.dev_service import DevService
from src.core.auth_middleware import require_auth

# Proteção da página
require_auth(allowed_roles=['admin'])

st.title("👥 Gerenciar Usuários")

user_service = UserService()
dev_service = DevService()

# --- SEÇÃO 1: CADASTRO ---
with st.expander("➕ Cadastrar Novo Usuário"):
    with st.form("form_registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_lgn = st.text_input("Login")
            new_nom = st.text_input("Nome")
        with col2:
            new_pwd = st.text_input("Senha", type="password")
            new_prm = st.selectbox("Permissão", ["user", "manager", "admin"])
        
        if st.form_submit_button("Salvar", type="primary"):
            success, msg = user_service.create_user(new_lgn, new_nom, new_pwd, new_prm)
            if success:
                st.success("Usuário criado!")
                st.rerun()
            else:
                st.error(msg)

st.divider()

# --- SEÇÃO 2: LISTAGEM ---
st.subheader("📋 Usuários do Sistema")
usuarios = user_service.get_all_users()

if not usuarios:
    st.info("Nenhum usuário encontrado.")
else:
    for u in usuarios:
        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 1, 1.5])
            
            c1.write(f"**{u['UsrNom']}**")
            c1.caption(f"Login: {u['UsrLgn']} | Nível: {u['UsrPrm'].upper()}")
            
            # Coluna 3 agora terá dois botões pequenos
            btn_col1, btn_col2 = c3.columns(2)
            
            # BOTÃO 1: Promoção / Detalhes
            is_dev = dev_service.check_if_exists(u['UsrCod'])
            if not is_dev:
                if btn_col1.button("🚀 Dev", key=f"prom_{u['UsrCod']}", help="Tornar Desenvolvedor"):
                    dev_service.create_dev_from_user(u['UsrCod'], u['UsrNom'])
                    st.toast(f"Usuário {u['UsrNom']} promovido a Desenvolvedor!", icon="🚀")
                    st.rerun()
            else:
                btn_col1.button("🔍 Ver", key=f"det_{u['UsrCod']}", disabled=True)

            # BOTÃO 2: Reset de Senha
            if btn_col2.button("🔑 Reset", key=f"pw_{u['UsrCod']}", help="Resetar para senha padrão '123'"):
                if user_service.reset_password(u['UsrCod']):
                    st.toast(f"Senha de {u['UsrNom']} resetada para '123'!", icon="🔐")
                else:
                    st.error("Erro ao resetar senha.")