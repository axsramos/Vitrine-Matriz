from src.core.config import Config
import streamlit as st
import os
from PIL import Image, ImageOps

def load_avatar(image_path=None, size=(150, 150)):
    """
    Carrega o avatar do usuário com múltiplos fallbacks.
    """
    # 1. Tenta carregar a imagem do usuário (vinda do banco)
    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            return ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        except Exception:
            pass
            
    # 2. Fallback: Tenta carregar o default_user definido no Config
    default_user = Config.DEFAULT_USER_IMG
    if os.path.exists(default_user):
        try:
            img = Image.open(default_user)
            return ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        except Exception:
            pass
            
    # 3. Fallback de Emergência: Quadrado cinza
    return Image.new('RGB', size, color=(220, 220, 220))

def display_logo():
    """Exibe o logo na barra lateral ou no topo."""
    logo_path = Config.LOGO_IMG
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
        
def render_model_field(model_class, field_name, container=st, val=None, disabled=False):
    """
    Renderiza um campo do Streamlit baseado nos metadados do Model.
    """
    # Busca a definição no dicionário FIELDS_MD do Model
    md = model_class.FIELDS_MD.get(field_name, {})
    
    label = md.get("Label", field_name)
    required = md.get("Required", False)
    field_type = md.get("Type", "VARCHAR")
    
    display_label = f"{label} *" if required else label
    key = f"input_{model_class.TABLE_NAME}_{field_name}"

    # Lógica de renderização por tipo de metadado
    if field_type == "PASSWORD":
        return container.text_input(display_label, value=val or "", type="password", key=key)
    
    elif field_type == "TEXTAREA":
        return container.text_area(display_label, value=val or "", key=key)
    
    elif field_type == "DATE":
        return container.date_input(display_label, value=val, key=key)
    
    elif field_type == "INTEGER":
        return container.number_input(display_label, value=val or 0, step=1, key=key)
        
    else: # Default VARCHAR
        return container.text_input(display_label, value=val or "", key=key)

def init_page(page_title, icon="🚀"):
    """Inicializa configurações básicas da página."""
    st.set_page_config(page_title=page_title, page_icon=icon, layout="wide")

# Mantive suas funções de mensagens, elas estão ótimas.
def show_success_message(message: str):
    st.success(message, icon="✅")

def show_error_message(message: str):
    st.error(message, icon="🚨")