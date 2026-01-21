from PIL import Image, ImageOps
import os
import streamlit as st
from typing import Any

def load_avatar(image_path, size=(150, 150)):
    """
    Carrega o avatar do usuário.
    Se falhar por qualquer motivo (caminho None, arquivo não existe, erro de leitura),
    retorna a imagem padrão ou um placeholder seguro.
    """
    default_path = "assets/default_user.png"
    
    # 1. Tenta carregar a imagem do usuário
    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            return ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        except Exception:
            pass # Se der erro, cai para o default
            
    # 2. Tenta carregar o default_user.png
    if os.path.exists(default_path):
        try:
            img = Image.open(default_path)
            return ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        except Exception:
            pass
            
    # 3. Fallback de Emergência (Se nem o padrão existir, para não travar o login)
    # Cria um quadrado cinza simples em memória
    return Image.new('RGB', size, color=(200, 200, 200))
    
# --- Função de Inicialização (Restaurada) ---
def init_page(page_title: str = "Vitrine Matriz", layout: str = "wide", sidebar_state: str = "expanded", icon: str = "🚀"):
    """
    Configurações iniciais da página (Título, Icone, Layout).
    Deve ser a primeira chamada Streamlit em cada página.
    """
    try:
        st.set_page_config(
            page_title=page_title,
            layout=layout,
            initial_sidebar_state=sidebar_state,
            page_icon=icon
        )
    except Exception:
        # st.set_page_config só pode ser chamado uma vez por execução.
        # Se der erro (ex: chamado duas vezes), ignoramos para não quebrar a app.
        pass

# --- Função de Renderização de Campos (Dinâmica) ---
def render_model_field(model_class, field_name: str, container=st, default_value=None, disabled=False, key=None) -> Any:
    """
    Renderiza um componente de input do Streamlit baseado nos metadados do Model.
    Lê atributos como: LongLabel, Type, Length, Required, TextHelp.
    """
    
    # 1. Validação de Metadados
    if not hasattr(model_class, 'FIELDS_MD') or field_name not in model_class.FIELDS_MD:
        return container.error(f"⚠️ Metadado não encontrado para o campo: {field_name}")

    meta = model_class.FIELDS_MD[field_name]
    
    # 2. Configurações Visuais
    label = meta.get('LongLabel', field_name)
    help_text = meta.get('TextHelp', '')
    placeholder = meta.get('TextPlaceholder', '')
    required = meta.get('Required', False)
    
    # Indicador visual de campo obrigatório (*)
    display_label = f"{label} *" if required else label
    
    # Determina valor inicial (Prioridade: default_value > Default do MD > String Vazia)
    val = default_value if default_value is not None else meta.get('Default', '')
    
    # Recupera definições de tipo e tamanho
    field_type = meta.get('Type', 'VARCHAR').upper() # Garante maiúsculo para comparação
    length = int(meta.get('Length', 255))

    # --- 3. Seleção Inteligente do Componente ---
    
    # Caso A: Campo de Texto Longo (Text Area)
    # Se o tamanho for maior que 255, assumimos que é uma descrição longa.
    if length > 255:
        return container.text_area(
            label=display_label,
            value=str(val) if val is not None else "",
            help=help_text,
            placeholder=placeholder,
            disabled=disabled,
            key=key
        )
    
    # Caso B: Campo Numérico (Integer)
    elif field_type in ('INTEGER', 'INT'):
        return container.number_input(
            label=display_label,
            value=int(val) if val else 0,
            help=help_text,
            disabled=disabled,
            step=1,
            key=key
        )
        
    # Caso C: Campo de Senha
    # Detecta se é senha pelo nome do campo ou label
    elif 'Pwd' in field_name or 'Senha' in label:
        return container.text_input(
            label=display_label,
            value=str(val) if val is not None else "",
            type="password",
            max_chars=length if length < 255 else None,
            help=help_text,
            disabled=disabled,
            key=key
        )

    # Caso D: Padrão (Texto Curto)
    else:
        return container.text_input(
            label=display_label,
            value=str(val) if val is not None else "",
            max_chars=length,
            help=help_text,
            placeholder=placeholder,
            disabled=disabled,
            key=key
        )

# --- Funções Auxiliares de Mensagem ---

def show_success_message(message: str):
    """Exibe mensagem de sucesso padronizada."""
    st.success(message, icon="✅")

def show_error_message(message: str):
    """Exibe mensagem de erro padronizada."""
    st.error(message, icon="🚨")

def show_info_message(message: str):
    """Exibe mensagem informativa padronizada."""
    st.info(message, icon="ℹ️")

def show_warning_message(message: str):
    """Exibe mensagem de aviso padronizada."""
    st.warning(message, icon="⚠️")
    
def show_help_message(message: str):
    st.help(message, icon="❓")

def clear_messages():
    st.empty()