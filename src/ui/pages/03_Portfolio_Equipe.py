import streamlit as st

# --- CONFIGURAÇÃO E CORE ---
from src.core.config import Config
from src.core.auth_middleware import require_auth
from src.core.ui_utils import load_avatar 

# --- SERVIÇOS ---
from src.services.dev_service import DevService

# --- METADADOS ---
from src.models.md.DevMD import DevMD
from src.models.md.UsrPrfMD import UsrPrfMD

# Configuração da Página
st.set_page_config(
    page_title=f"Equipe | {Config.APP_TITLE}", 
    layout="wide"
)

# Segurança de Acesso
require_auth()

# --- CABEÇALHO ---
st.title("👥 Time de Desenvolvedores")
st.write("Conheça os especialistas por trás do ecossistema.")

# Instância do Serviço
dev_service = DevService()

# Busca dados consolidados (Dev + Perfil)
# O método get_portfolio_data retorna lista de dicts com chaves: DevNom, UsrPrfBio, etc.
equipe = dev_service.get_portfolio_data()

# --- EXIBIÇÃO DOS CARDS ---
if not equipe:
    st.info("Nenhum portfólio registrado no momento.")
else:
    for dev in equipe:
        # Container isolado para cada membro
        with st.container(border=True):
            
            # Divisão interna: Foto (1) vs Informações (2)
            col_img, col_txt = st.columns([1, 3])
            
            # --- FOTO DO PERFIL ---
            with col_img:
                # Tenta carregar foto do perfil, senão usa avatar padrão
                foto_blob = dev.get('UsrPrfFto') 
                img = load_avatar(foto_blob) 
                st.image(img, use_container_width=True)
            
            # --- INFORMAÇÕES TEXTUAIS ---
            with col_txt:
                # Nome (Vindo de T_Dev)
                lbl_nome = DevMD.FIELDS_MD['DevNom']['Label']
                nome = dev.get('DevNom', 'Desenvolvedor')
                st.subheader(nome)
                
                # Cargo (Vindo de T_UsrPrf)
                cargo = dev.get('UsrPrfCgo')
                if cargo:
                    st.caption(f"**{cargo}**")
                
                # Bio (Vindo de T_UsrPrf)
                # lbl_bio = UsrPrfMD.FIELDS_MD['UsrPrfBio']['Label'] # Opcional usar o label
                bio = dev.get('UsrPrfBio') or "Perfil técnico focado em soluções tecnológicas."
                st.write(bio)
                
                # Link/Portfólio
                link = dev.get('UsrPrfUrl')
                lbl_link = UsrPrfMD.FIELDS_MD['UsrPrfUrl']['Label']
                
                st.markdown("---")
                
                if link:
                    # Garante protocolo http/https para o botão funcionar
                    url_final = link if link.startswith(('http://', 'https://')) else f"https://{link}"
                    st.link_button(f"🔗 {lbl_link}", url_final, use_container_width=True)
                else:
                    st.caption("🌐 Link profissional não informado.")
        
        # Espaçamento entre cards
        st.write("")