import streamlit as st
from src.services.release_service import ReleaseService
from src.services.task_service import TaskService

st.set_page_config(page_title="Notas de Versão (Changelog)")

st.title("📜 Notas de Versão")
st.markdown("Acompanhe a evolução do projeto e as entregas realizadas.")

rel_service = ReleaseService()
task_service = TaskService()

# 1. Busca todas as releases ordenadas
df_releases = rel_service.get_all_releases()

if df_releases.empty:
    st.info("Nenhuma versão publicada ainda.")
else:
    # Itera sobre as versões para montar o Changelog visual
    for index, row in df_releases.iterrows():
        versao = row['RelVrs']
        titulo = row['RelTtlCmm']
        data_pub = row['RelDtaPub']
        rel_cod = row['RelCod']
        
        # Container da Versão
        with st.expander(f"📦 {versao} - {titulo} ({data_pub})", expanded=(index == 0)):
            # Busca tarefas vinculadas a esta release (Pelo RelCod)
            df_tasks = task_service.get_tasks_by_release(rel_cod)
            
            if not df_tasks.empty:
                st.markdown("### Mudanças e Melhorias")
                
                for _, task in df_tasks.iterrows():
                    # Formata o item da lista
                    # Ícone baseado no impacto
                    impacto = task.get('TskImp', 'Baixo')
                    icon = "🔥" if impacto == 'Crítico' else "✨" if impacto == 'Alto' else "🔹"
                    
                    st.markdown(f"{icon} **[{task['TskExtCod']}] {task['TskTtl']}**")
                    if task['TskDsc']:
                        st.caption(f"> {task['TskDsc']}")
            else:
                st.caption("Esta versão não possui tarefas detalhadas vinculadas.")