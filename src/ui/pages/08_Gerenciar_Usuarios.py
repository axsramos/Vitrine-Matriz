import streamlit as st
import pandas as pd
from src.services.user_service import UserService
from src.services.dev_service import DevService
from src.core.auth_middleware import require_auth
from src.core import ui_utils
from src.models import UserModel

# Configuração da Página
ui_utils.init_page(page_title="Gerenciar Usuários", icon="👥")
require_auth(allowed_roles=['Admin']) 

st.title("👥 Gerenciar Usuários")

user_service = UserService()
dev_service = DevService()

# --- ABA 1: Adicionar Usuário ---
with st.expander("➕ Adicionar Novo Usuário", expanded=False):
    
    # [CORREÇÃO] Lógica de Limpeza Prévia (Flag Pattern)
    # Verifica se deve limpar ANTES de renderizar os widgets
    if st.session_state.get('clear_form_user_flag'):
        st.session_state['new_usr_name'] = ""
        st.session_state['new_usr_login'] = ""
        st.session_state['new_usr_pwd'] = ""
        st.session_state['new_usr_role'] = "User" # Reseta o selectbox para o valor padrão
        # Desliga a flag para não limpar novamente
        st.session_state['clear_form_user_flag'] = False

    with st.form("form_add_user"):
        col1, col2 = st.columns(2)
        
        with col1:
            # As chaves (keys) aqui serão lidas do session_state limpo acima
            name = ui_utils.render_model_field(UserModel, 'UsrNme', key="new_usr_name")
            login = ui_utils.render_model_field(UserModel, 'UsrLgn', key="new_usr_login")
        
        with col2:
            pwd = st.text_input("Senha *", type="password", key="new_usr_pwd")
            role_label = UserModel.FIELDS_MD['UsrRle']['LongLabel']
            role = st.selectbox(role_label, ["User", "Admin", "Manager"], key="new_usr_role")

        submit = st.form_submit_button("Salvar Usuário", type="primary")
        
        if submit:
            if not name or not login or not pwd:
                ui_utils.show_error_message("Preencha todos os campos obrigatórios.")
            else:
                success, msg = user_service.create_user(name, login, pwd, role)
                if success:
                    ui_utils.show_success_message(msg)
                    
                    # [CORREÇÃO] Apenas ativa a flag e recarrega
                    # A limpeza real acontecerá no início da próxima execução
                    st.session_state['clear_form_user_flag'] = True
                    st.rerun()
                else:
                    ui_utils.show_error_message(msg)

st.markdown("---")

# --- LISTAGEM E AÇÕES ---
st.subheader("Base de Usuários")

df_users = user_service.get_all_users()

if not df_users.empty:
    col_table, col_actions = st.columns([2, 1])
    
    selected_usr_login = None
    
    # 1. RENDERIZA A COLUNA DA DIREITA PRIMEIRO (Ações)
    with col_actions:
        st.info("🛠️ **Ações do Usuário**")
        
        user_options = df_users.to_dict('records')
        
        selected_user = st.selectbox(
            "Selecione um Usuário:",
            options=user_options,
            format_func=lambda x: f"{x['UsrLgn']} | {x['UsrNme']}",
            key="sel_user_action"
        )
        
        if selected_user:
            selected_usr_login = selected_user['UsrLgn']

            st.divider()
            st.markdown(f"**Alvo:** {selected_user['UsrNme']}")
            
            # Botão Promover
            btn_promote = st.button("👨‍💻 Tornar Desenvolvedor", use_container_width=True)
            if btn_promote:
                success, msg = dev_service.create_dev_from_user(
                    user_name=selected_user['UsrNme'],
                    user_login=selected_user['UsrLgn']
                )
                if success:
                    ui_utils.show_success_message(msg)
                else:
                    ui_utils.show_warning_message(msg)
            
            # Botão Excluir
            st.divider()
            if st.button("🗑️ Excluir Usuário", type="secondary", use_container_width=True):
                if selected_user['UsrLgn'] == 'admin':
                    ui_utils.show_error_message("O admin principal não pode ser excluído.")
                else:
                    svc_success, svc_msg = user_service.delete_user(int(selected_user['UsrCod']))
                    if svc_success:
                        ui_utils.show_success_message(svc_msg)
                        st.rerun()
                    else:
                        ui_utils.show_error_message(svc_msg)

    # 2. RENDERIZA A COLUNA DA ESQUERDA (Tabela)
    with col_table:
        display_cols = ['UsrCod', 'UsrNme', 'UsrLgn', 'UsrRle']
        df_display = df_users[display_cols].copy()

        def highlight_selected_row(row):
            if selected_usr_login and row['UsrLgn'] == selected_usr_login:
                # Fundo amarelo claro com texto em negrito
                return ['background-color: #ffeeb0; color: #333333; font-weight: bold'] * len(row)
            return [''] * len(row)

        try:
            styled_df = df_display.style.apply(highlight_selected_row, axis=1)
            
            st.dataframe(
                styled_df, 
                use_container_width=True,
                column_config={"UsrCod": "ID", "UsrNme": "Nome", "UsrLgn": "Login", "UsrRle": "Perfil"},
                hide_index=True
            )
        except Exception:
            st.dataframe(df_display, use_container_width=True, hide_index=True)

else:
    st.info("Nenhum usuário encontrado.")