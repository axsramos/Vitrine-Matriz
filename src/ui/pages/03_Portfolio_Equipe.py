import streamlit as st
import os
from src.services.dev_service import DevService
from src.core import config
from src.core.ui_utils import init_page

init_page("Portfólio da Equipe", "wide")

# Estilização CSS Customizada (Cards)
st.markdown("""
    <style>
    .dev-card {
        border: 1px solid #e6e9ef;
        border-radius: 15px;
        padding: 25px;
        background-color: #ffffff;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .dev-card:hover {
        transform: translateY(-5px);
        border-color: #4b8bbe;
    }
    .dev-name { font-size: 22px; font-weight: bold; color: #1e3d59; margin-top: 10px; }
    .dev-role { color: #6e7c7c; font-style: italic; margin-bottom: 15px; font-size: 14px; }
    .dev-mention { 
        font-size: 14px; 
        color: #444; 
        background: #f0f2f6; 
        padding: 10px; 
        border-radius: 8px; 
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stat-box { font-size: 16px; margin: 15px 0; color: #333; }
    </style>
""", unsafe_allow_html=True)

st.title("👥 Portfólio da Equipe")
st.write("Conheça os especialistas responsáveis pela evolução técnica do **Portal Matriz**.")

# Inicialização do Serviço e Busca de Dados
service = DevService()
df_team = service.get_team_stats()

if df_team.empty:
    st.info("Ainda não há desenvolvedores com atividades registradas no banco.")
else:
    # Criação do Grid de 3 colunas
    cols = st.columns(3)
    
    for index, row in df_team.iterrows():
        with cols[index % 3]:
            # Lógica para exibir foto ou placeholder
            foto_url = row['foto_path'] if row['foto_path'] and os.path.exists(row['foto_path']) else "https://via.placeholder.com/150/e6e9ef/6e7c7c?text=Foto"
            
            # Container do Card
            with st.container():
                # Exibição da Imagem (Redonda usando CSS do Streamlit)
                st.image(foto_url, use_container_width=True)
                
                # Conteúdo do Card via HTML
                st.markdown(f"""
                    <div class="dev-card">
                        <div class="dev-name">{row['nome']}</div>
                        <div class="dev-role">{row['cargo']}</div>
                        <div class="dev-mention">"{row['bio'] or 'Focado em entregar valor através do código!'}"</div>
                        <div class="stat-box">
                            <strong>🚀 {row['total_releases']}</strong> Releases &nbsp; | &nbsp;
                            <strong>✅ {row['total_tarefas']}</strong> Tarefas
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botão de Ação (Redirecionamento)
                if st.button(f"Ver Trajetória de {row['nome'].split()[0]}", key=f"btn_{row['id']}", use_container_width=True):
                    # Usamos session_state para garantir a passagem imediata do ID
                    st.session_state["selected_dev_id"] = row['id']
                    st.switch_page(config.get_page("04_Detalhes_Dev.py"))

st.divider()

dev_service = DevService()
# 1. Seleção de Desenvolvedor
df_equipa = dev_service.get_team_stats()
dev_nomes = df_equipa['nome'].tolist()
dev_sel = st.selectbox("Consultar Especialista:", options=dev_nomes)

if dev_sel:
    dev_id = df_equipa[df_equipa['nome'] == dev_sel]['id'].values[0]
    dev_info = df_equipa[df_equipa['nome'] == dev_sel].iloc[0]
    df_profile = dev_service.get_dev_full_profile(dev_id)

    # 2. Cabeçalho do Perfil (Destaque)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150) # Placeholder
    with col2:
        st.header(dev_sel)
        st.subheader(f"🚀 {dev_info['cargo']}")
        st.write(f"**Bio:** {dev_info['bio'] or 'Desenvolvedor focado em entregas de alto valor.'}")
    with col3:
        st.metric("Total de Entregas", dev_info['total_tarefas'])

    st.divider()

    # 3. Timeline de Impacto
    st.markdown("### 📈 Histórico de Contribuições")
    
    if df_profile.empty:
        st.info("Este desenvolvedor ainda não possui tarefas registadas.")
    else:
        for _, row in df_profile.iterrows():
            with st.expander(f"📌 {row['tarefa_titulo']} (v{row['versao'] or 'Aguardando'})"):
                c1, c2 = st.columns([1, 3])
                
                # Badge de Impacto
                cor = "red" if row['impacto'] == "Crítico" else "orange" if row['impacto'] == "Alto" else "blue"
                c1.markdown(f"**Impacto:** :{cor}[{row['impacto']}]")
                c1.caption(f"📅 {row['data']}")
                
                c2.markdown(f"**Valor de Negócio:**\n{row['impacto_negocio']}")

st.markdown("---")
st.caption(f"Dados gerados a partir do cruzamento de metadados do { config.APP_TITLE } e Bitrix24.")