import streamlit as st
from src.services.tarefa_service import TarefaService
from src.models.release import Release
from src.models.tarefa import Tarefa

st.set_page_config(page_title="Gerar Release - Vitrine Matriz", layout="wide")

st.title("📦 Gerar / Atualizar Release")

# 1. Carregamento e Filtro
tarefa_service = TarefaService()
df_total = tarefa_service.get_all_tasks_for_release()

# Filtro pré-definido na lateral
show_all = st.sidebar.checkbox("Exibir tarefas já publicadas", value=False)

if not show_all:
    df_exibicao = df_total[df_total['status_vinculo'] == '⭐ Nova'].copy()
else:
    df_exibicao = df_total.copy()

# 2. Formulário
with st.form("form_release_dinamica"):
    col1, col2 = st.columns(2)
    with col1:
        versao = st.text_input("Número da Versão", placeholder="Ex: v1.0.2")
    with col2:
        titulo_comunicado = st.text_input("Título do Comunicado", placeholder="Ex: Melhorias de Performance")

    st.write("### Seleção de Itens")
    df_exibicao.insert(0, "Selecionar", False)
    
    # Grid de Edição
    df_editado = st.data_editor(
        df_exibicao,
        column_config={
            "Selecionar": st.column_config.CheckboxColumn("Selecionar"),
            "status_vinculo": st.column_config.TextColumn("Status", help="⭐ Nova = Sem release | ✅ Publicada = Já vinculada"),
            "titulo": st.column_config.TextColumn("Tarefa", width="large"),
            "desenvolvedor": st.column_config.TextColumn("Dev", width="medium"),
        },
        disabled=["id", "bitrix_task_id", "titulo", "desenvolvedor", "status_vinculo"],
        hide_index=True,
        use_container_width=True,
    )

    btn_publicar = st.form_submit_button("🚀 Publicar Release")

# 3. Lógica de Persistência
if btn_publicar:
    selecionados = df_editado[df_editado["Selecionar"] == True]
    
    if not versao or selecionados.empty:
        st.error("Preencha a versão e selecione ao menos uma tarefa.")
    else:
        rel_id = Release({"versao": versao, "titulo_comunicado": titulo_comunicado}).create()
        
        if rel_id:
            for _, row in selecionados.iterrows():
                # Atualiza o vínculo (sobrescreve se já existia, ou mantém se for nova)
                Tarefa({"id": row["id"], "id_release": rel_id}).update()
            
            st.success(f"Release {versao} gerada com sucesso!")
            st.rerun()