import streamlit as st
from src.core import config

def init_page(subtitulo: str, layout: str = "wide"):
    """
    Padroniza a configuração da página e o título.
    """
    st.set_page_config(
        page_title=f"{subtitulo} - {config.APP_TITLE}",
        page_icon="🖼️",
        layout=layout
    )