import streamlit as st
from src.services.dev_service import DevService
from src.core.ui_utils import load_avatar
from src.core.auth_middleware import require_auth

# Proteção de acesso
# require_auth()

st.title("👥 Time de Desenvolvedores")
st.write("Equipe técnica responsável pelo ecossistema Vitrine-Matriz.")


dev_service = DevService()
equipe = dev_service.get_all_developers()

if not equipe:
    st.info("Nenhum portfólio registrado no momento.")
else:
    # Criamos um grid para exibir os perfis
    for dev in equipe:
        with st.container(border=True):
            col_img, col_txt = st.columns([1, 3])
            
            with col_img:
                # Tenta carregar a foto; se não houver, usa um placeholder
                foto = dev.get('DevFto')
                img = load_avatar(foto) 
                st.image(img, use_container_width=True)
            
            with col_txt:
                st.subheader(dev.get('DevNom', 'Desenvolvedor'))
                
                # Exibe a Bio ou um texto padrão
                bio = dev.get('DevBio') or "Desenvolvedor focado em soluções tecnológicas."
                st.write(bio)
                
                # Link do Portfólio
                link = dev.get('DevLnk')
                if link:
                    # Tratamento para evitar concatenação com a URL local
                    # Se o link não começar com http, nós adicionamos o protocolo
                    url_final = link if link.startswith(('http://', 'https://')) else f"https://{link}"
                    
                    st.link_button("🔗 Ver Portfólio Profissional", url_final, use_container_width=True)
                else:
                    st.caption("🌐 Link do portfólio não cadastrado.")

st.divider()

# dev_service = DevService()
# equipe = dev_service.get_all_developers()

# if not equipe:
#     st.info("Nenhum portfólio registrado no momento.")
# else:
#     # Iteramos sobre a equipe de 2 em 2 para criar as linhas
#     for i in range(0, len(equipe), 2):
#         # Cria as duas colunas principais da página
#         col_esq, col_dir = st.columns(2)
        
#         # Lista de colunas e devs para este bloco
#         devs_no_bloco = [equipe[i]]
#         if i + 1 < len(equipe):
#             devs_no_bloco.append(equipe[i+1])
            
#         # Renderiza cada dev em sua respectiva coluna principal
#         for idx, dev in enumerate(devs_no_bloco):
#             alvo = col_esq if idx == 0 else col_dir
            
#             with alvo:
#                 with st.container(border=True):
#                     # Sub-colunas internas para Foto vs Texto
#                     col_img, col_txt = st.columns([1, 2])
                    
#                     with col_img:
#                         foto = dev.get('DevFto')
#                         img = load_avatar(foto) 
#                         st.image(img, use_container_width=True)
                    
#                     with col_txt:
#                         st.subheader(dev.get('DevNom', 'Desenvolvedor'))
#                         bio = dev.get('DevBio') or "Desenvolvedor focado em soluções tecnológicas."
#                         st.write(bio)
                        
#                         link = dev.get('DevLnk')
#                         if link:
#                             url_final = link if link.startswith(('http://', 'https://')) else f"https://{link}"
#                             st.link_button("🔗 Portfólio", url_final, use_container_width=True)
#                         else:
#                             st.caption("🌐 Sem link cadastrado.")

# st.divider()
st.caption("Os dados acima são gerenciados individualmente por cada profissional em 'Meu Perfil'.")
