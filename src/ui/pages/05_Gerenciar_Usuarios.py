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
            c1, c2, c3 = st.columns([2, 1, 1])
            
            c1.write(f"**{u['UsrNom']}**")
            c1.caption(f"Login: {u['UsrLgn']}")
            c2.write(f"🏷️ {u['UsrPrm'].upper()}")
            
            # Lógica do Botão Dinâmico
            is_dev = dev_service.check_if_exists(u['UsrCod'])
            
            if not is_dev:
                # Caso não seja Dev, exibe botão de promoção
                if c3.button("🚀 Tornar Dev", key=f"promo_{u['UsrCod']}", use_container_width=True):
                    dev_data = {
                        "DevCod": u['UsrCod'],
                        "DevNom": u['UsrNom'],
                        "DevAudUsr": st.session_state['user']['UsrLgn']
                    }
                    if dev_service.promote_to_developer(dev_data):
                        st.toast(f"{u['UsrNom']} agora é Desenvolvedor!", icon="🚀")
                        st.rerun()
                    else:
                        # O erro detalhado deve aparecer no terminal do VS Code
                        st.error("Falha na promoção. Verifique o log.")
            else:
                # Caso já seja Dev, indica que terá detalhes futuramente
                c3.button("🔍 Detalhes", key=f"det_{u['UsrCod']}", disabled=True, use_container_width=True)