from src.models.desenvolvedor import Desenvolvedor
from src.models.release import Release
from src.models.tarefa import Tarefa
from run_migrations import run_migrations

def seed():
    # 1. Garante que as tabelas existem
    run_migrations()

    print("🌱 Iniciando o seeding do Vitrine Matriz...")

    # 2. Criar Desenvolvedores
    devs = [
        {
            "nome": "Alex Ramos",
            "login_bitrix": "alex.ramos",
            "cargo": "Desenvolvedor Full Stack",
            "bio": "Entusiasta de Python e arquitetura de sistemas. Sempre com um pão na chapa e um café!",
            "github_url": "https://github.com/axsramos"
        },
        {
            "nome": "Beatriz Silva",
            "login_bitrix": "beatriz.silva",
            "cargo": "Especialista em UI/UX",
            "bio": "Transformando requisitos complexos em interfaces simples e elegantes.",
            "github_url": "https://github.com"
        }
    ]

    dev_ids = []
    for d in devs:
        model = Desenvolvedor(d)
        dev_ids.append(model.create())

    # 3. Criar Releases
    rel_id = Release({
        "versao": "v1.5.0",
        "titulo_comunicado": "Módulo de Dashboards e Performance"
    }).create()

    # 4. Criar Tarefas com Impacto de Negócio
    tarefas = [
        {
            "bitrix_task_id": 5001,
            "titulo": "Otimização de Query SQL - Portal Matriz",
            "descricao_tecnica": "Refatoração do JOIN na tabela de extratos.",
            "impacto_negocio": "Redução de 40% no tempo de carregamento para o cliente final.",
            "id_desenvolvedor": dev_ids[0],
            "id_release": rel_id
        },
        {
            "bitrix_task_id": 5002,
            "titulo": "Novo Componente de Filtro Temporal",
            "descricao_tecnica": "Implementação de date-picker customizado em JS.",
            "impacto_negocio": "Melhoria na usabilidade, reduzindo tickets de suporte sobre filtros.",
            "id_desenvolvedor": dev_ids[1],
            "id_release": rel_id
        }
    ]

    for t in tarefas:
        Tarefa(t).create()

    print("✅ Dados de teste inseridos com sucesso!")

if __name__ == "__main__":
    seed()