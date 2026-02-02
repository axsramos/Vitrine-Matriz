import streamlit as st

class SessionHelper:
    @staticmethod
    def get_current_user_login() -> str:
        """
        Recupera o login do usuário atual de forma segura.
        Retorna 'system' se não houver sessão ativa.
        """
        try:
            if hasattr(st, "session_state") and \
               "user" in st.session_state and \
               st.session_state["user"] and \
               "login" in st.session_state["user"]:
                return st.session_state["user"]["login"]
        except Exception:
            pass
        return "system"