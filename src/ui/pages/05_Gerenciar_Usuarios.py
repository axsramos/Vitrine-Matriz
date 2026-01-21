import streamlit as st
import pandas as pd
from src.services.user_service import UserService
from src.models.UserModel import UserModel
from src.core import ui_utils
from src.core.auth_middleware import require_auth

# Proteção: Apenas administradores acessam esta tela
require_auth(allowed_roles=['admin'])

st.title("👤 Gerenciamento de Usuários")

user_service = UserService()

# --- ABA 1: LISTAGEM ---
tab_lista, tab_novo = st.tabs(["Consultar Usuários", "Novo Usuário"])

with tab_lista:
    # Como não temos um UserService.get_all completo, usamos o Model diretamente via Mixin
    model = UserModel()
    # Filtra apenas não deletados
    usuarios = model.read_all()
    
    if usuarios:
        df = pd.DataFrame(usuarios)
        # Filtro de busca simples
        search = st.text_input("🔍 Buscar por nome ou login")
        if search:
            df = df[df['UsrNom'].str.contains(search, case=False) | df['UsrLgn'].str.contains(search, case=False)]
        
        st.dataframe(
            df[['UsrCod', 'UsrNom', 'UsrLgn', 'UsrPrm', 'UsrAudIns']],
            column_config={
                "UsrCod": "ID",
                "UsrNom": "Nome",
                "UsrLgn": "Login",
                "UsrPrm": "Permissão",
                "UsrAudIns": "Data Cadastro"
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum usuário cadastrado.")

# --- ABA 2: CADASTRO ---
with tab_novo:
    with st.form("form_novo_usuario"):
        st.write("Dados de Acesso")
        # Usando ui_utils para renderizar campos baseados no MD
        usr_nom = ui_utils.render_model_field(UserModel, 'UsrNom')
        usr_lgn = ui_utils.render_model_field(UserModel, 'UsrLgn')
        usr_pwd = ui_utils.render_model_field(UserModel, 'UsrPwd')
        usr_prm = st.selectbox("Permissão", ["user", "admin", "manager"])
        
        if st.form_submit_button("Cadastrar Usuário", type="primary"):
            if not usr_nom or not usr_lgn or not usr_pwd:
                st.error("Preencha todos os campos obrigatórios.")
            else:
                # Hash da senha antes de salvar (importante!)
                import hashlib
                pwd_hash = hashlib.sha256(usr_pwd.encode()).hexdigest()
                
                novo_usr = UserModel(
                    UsrNom=usr_nom,
                    UsrLgn=usr_lgn,
                    UsrPwd=pwd_hash,
                    UsrPrm=usr_prm,
                    UsrAudUsr=st.session_state['user']['UsrLgn']
                )
                
                if novo_usr.save():
                    st.success("Usuário criado com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao salvar usuário (Login pode já existir).")