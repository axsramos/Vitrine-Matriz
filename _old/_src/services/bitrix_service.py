import requests
import os
from dotenv import load_dotenv
from src.models.tarefa import Tarefa

load_dotenv()

class BitrixService:
    def __init__(self):
        self.webhook_url = os.getenv("BITRIX_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("BITRIX_WEBHOOK_URL não configurada no .env")

    def get_task_details(self, task_id):
        """Busca detalhes de uma tarefa específica."""
        url = f"{self.webhook_url}tasks.task.get"
        params = {"taskId": task_id}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('result', {}).get('task')
        return None

    def list_completed_tasks(self, user_id=None):
        """Lista tarefas finalizadas para importação."""
        url = f"{self.webhook_url}tasks.task.list"
        
        # Filtros: Status 5 = Concluída
        params = {
            "filter[STATUS]": 5,
            "select[]": ["ID", "TITLE", "DESCRIPTION", "RESPONSIBLE_ID"]
        }
        
        if user_id:
            params["filter[RESPONSIBLE_ID]"] = user_id

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('result', {}).get('tasks', [])
        return []

    def sync_task_to_db(self, bitrix_task):
        """
        Mapeia o JSON do Bitrix para o modelo Tarefa e persiste no SQLite
        usando o seu CrudMixin.
        """
        dados_tarefa = {
            "bitrix_task_id": bitrix_task['id'],
            "titulo": bitrix_task['title'],
            "descricao_tecnica": bitrix_task['description'],
            # id_desenvolvedor e id_release seriam vinculados aqui
        }
        
        tarefa_model = Tarefa(dados_tarefa)
        return tarefa_model.create()

    def list_tasks_mock(self):
        """Retorna dados fictícios para desenvolvimento da interface."""
        return [
            {
                "id": "101",
                "title": "Ajuste no cálculo de juros FIDC",
                "description": "Corrigido arredondamento na parcela final conforme regra da empresa.",
                "responsible_id": "1"
            },
            {
                "id": "102",
                "title": "Integração API Banco Central",
                "description": "Endpoint de consulta de taxas atualizado para v2.",
                "responsible_id": "2"
            },
            {
                "id": "103",
                "title": "Correção de Layout - Portal Matriz",
                "description": "Ajuste de padding nas tabelas de extrato no ambiente mobile.",
                "responsible_id": "1"
            }
        ]