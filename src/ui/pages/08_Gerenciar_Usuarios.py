import streamlit as st
from src.services.user_service import UserService
from src.core import config
from src.core.auth_middleware import require_auth
from src.core.ui_utils import init_page

require_auth()

init_page("Gerenciar Usuários", "wide")

st.title("👥 Gestão de Usuários")
    
service = UserService()

# --- Formulário de Cadastro ---
with st.expander("➕ Cadastrar Novo Usuário"):
    with st.form("form_novo_usuario"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo")
        user = col2.text_input("Username")
        senha = col1.text_input("Senha", type="password")
        role = col2.selectbox("Perfil", ["Admin", "Viewer"])
        
        if st.form_submit_button("Salvar Usuário"):
            if nome and user and senha:
                try:
                    service.create(nome, user, senha, role)
                    st.success("Usuário criado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao criar: {e}")
            else:
                st.warning("Preencha todos os campos.")

# --- Listagem e Exclusão ---
st.subheader("Usuários Ativos")
df_users = service.get_all()

if not df_users.empty:
    # Exibição em tabela
    st.dataframe(df_users, use_container_width=True)
    
    # Opção de exclusão
    id_excluir = st.number_input("ID para remover", min_value=1, step=1)
    if st.button("🗑️ Remover Usuário", type="secondary"):
        # Impede o admin de se auto-excluir (opcional)
        if st.session_state.user and id_excluir == st.session_state.user['id']:
            st.error("Você não pode excluir seu próprio usuário logado.")
        else:
            service.delete(id_excluir)
            st.success("Usuário removido.")
            st.rerun()