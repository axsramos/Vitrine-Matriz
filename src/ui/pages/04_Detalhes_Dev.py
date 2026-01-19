import os
import streamlit as st
from src.services.dev_service import DevService
from src.services.task_service import TaskService
from src.models import DevModel

# Define o caminho da imagem padrão
DEFAULT_IMAGE = "assets/default_user.png"

st.set_page_config(page_title="Detalhes do Desenvolvedor")

st.title("🕵️ Detalhes do Profissional")

dev_service = DevService()
task_service = TaskService()

# 1. Seleção do Desenvolvedor
df_devs = dev_service.get_all_developers()

if df_devs.empty:
    st.warning("Nenhum desenvolvedor cadastrado.")
    st.stop()

# Cria um Selectbox para escolher quem detalhar
dev_options = df_devs['DevCod'].tolist()
dev_names = {row['DevCod']: row['DevNme'] for _, row in df_devs.iterrows()}

selected_dev_cod = st.selectbox(
    "Selecione o Desenvolvedor:",
    options=dev_options,
    format_func=lambda x: dev_names.get(x, x)
)

if selected_dev_cod:
    # 2. Carrega dados do Model
    dev_model = DevModel()
    
    if dev_model.load(selected_dev_cod):
        
        # Layout de Cabeçalho
        col_img, col_info = st.columns([1, 3])
        
        with col_img:
            # img_url = dev_model.DevFto if dev_model.DevFto else "https://via.placeholder.com/200"
            img_url = dev_model.DevFto if dev_model.DevFto else DEFAULT_IMAGE
            st.image(img_url, width=150)
            
            if dev_model.DevPgeUrl:
                st.link_button("Acessar GitHub/Portfólio", dev_model.DevPgeUrl)
        
        with col_info:
            st.header(dev_model.DevNme)
            st.subheader(f"💼 {dev_model.DevCgo}")
            st.write(dev_model.DevBio)
            
        st.divider()
        
        # 3. Histórico de Tarefas (Timeline)
        st.subheader("Histórico de Entregas")
        
        # Busca tarefas onde DevCod é o selecionado
        # Usamos o método read_join para ter dados da Release também
        df_tasks = task_service.get_all_tasks() # Pega tudo e filtra no pandas (ou cria método específico no service)
        
        if not df_tasks.empty:
            # Filtra pelo DevCod (convertendo para int para garantir)
            df_dev_tasks = df_tasks[df_tasks['DevCod'] == selected_dev_cod]
            
            if not df_dev_tasks.empty:
                for _, task in df_dev_tasks.iterrows():
                    rel_info = f" (v{task['RelVrs']})" if 'RelVrs' in task and task['RelVrs'] else " (Em Backlog)"
                    st.markdown(f"- **{task['TskTtl']}** {rel_info}")
                    st.caption(f"  *Impacto: {task['TskImp']}*")
            else:
                st.info("Este desenvolvedor ainda não possui tarefas vinculadas.")
    else:
        st.error("Erro ao carregar dados do desenvolvedor.")