import streamlit as st
import os
from src.services.dev_service import DevService
from src.core.config import get_page

# 1. Configuração da Página
st.set_page_config(page_title="Perfil do Desenvolvedor - Vitrine Matriz", layout="wide")

# 2. Recuperação do ID (Prioridade para Session State)
dev_id = st.session_state.get("selected_dev_id") or st.query_params.get("dev_id")

if not dev_id:
    st.error("⚠️ Desenvolvedor não selecionado.")
    if st.button("⬅️ Voltar para a Equipe"):
        st.switch_page(get_page("03_Portfolio_Equipe.py"))
    st.stop()

# 3. Busca de Dados
service = DevService()
df_profile = service.get_dev_full_profile(dev_id)

if df_profile.empty:
    st.warning("Perfil não encontrado no banco de dados.")
    if st.button("⬅️ Voltar"):
        st.switch_page(get_page("03_Portfolio_Equipe.py"))
    st.stop()

# Extraímos as informações fixas do dev (primeira linha do join)
dev_info = df_profile.iloc[0]

# 4. Cabeçalho do Perfil
col1, col2 = st.columns([1, 3])

with col1:
    # Lógica de Imagem Real vs Placeholder
    foto_path = dev_info.get('foto_path')
    if foto_path and os.path.exists(foto_path):
        st.image(foto_path, use_container_width=True)
    else:
        st.image("https://via.placeholder.com/300/e6e9ef/6e7c7c?text=Sem+Foto", use_container_width=True)

with col2:
    st.title(dev_info['nome'])
    st.subheader(f"🚀 {dev_info['cargo']}")
    st.markdown(f"**Bio:** {dev_info['bio'] or 'Desenvolvedor focado em soluções para o Portal Matriz.'}")
    
    if dev_info['github_url']:
        st.link_button("🌐 Acessar GitHub Profissional", dev_info['github_url'])

st.divider()

# 5. Linha do Tempo de Entregas e Valor Gerado
st.subheader("🛠️ Histórico de Entregas e Impacto de Negócio")

# Filtramos apenas as linhas que possuem tarefas (caso o dev exista mas não tenha tarefas)
df_tasks = df_profile[df_profile['tarefa_titulo'].notnull()]

if df_tasks.empty:
    st.info("Este desenvolvedor ainda não possui tarefas vinculadas a uma release.")
else:
    for _, tarefa in df_tasks.iterrows():
        with st.expander(f"📦 Versão {tarefa['versao']} - {tarefa['tarefa_titulo']}", expanded=True):
            c1, c2 = st.columns([1, 4])
            c1.metric("Release", tarefa['versao'])
            
            with c2:
                st.markdown("**Descrição Técnica:**")
                st.write(tarefa['tarefa_titulo'])
                
                # O grande diferencial para o gestor:
                st.markdown("---")
                st.markdown("**💡 Impacto para o Negócio:**")
                st.info(tarefa['impacto_negocio'] or "Impacto técnico em análise.")

# 6. Rodapé de Navegação
st.sidebar.markdown("---")
if st.sidebar.button("⬅️ Voltar para a Vitrine", use_container_width=True):
    # Limpamos o estado ao voltar para garantir nova seleção limpa
    if "selected_dev_id" in st.session_state:
        del st.session_state["selected_dev_id"]
    st.switch_page(get_page("03_Portfolio_Equipe.py"))