📋 Roadmap de Desenvolvimento (v0.4.0)
Configuração do Ambiente:

[ ] Criar arquivo .env (baseado no .env.example).

[ ] Atualizar src/core/config.py para carregar variáveis de ambiente.

Camada Core (Infraestrutura):

[ ] Refatorar src/core/database.py (Implementar Factory e Row Factory).

[ ] Implementar src/core/crud_mixin.py (O "Motor" de Query Dinâmica).

Camada de Modelo (Models):

[ ] Criar src/models/__init__.py (Para exportação modular).

[ ] Converter DevMD em DevModel (Herdando Mixin).

[ ] Converter TskMD em TaskModel (Herdando Mixin).

[ ] Converter RelMD em ReleaseModel.

[ ] Converter UsrMD em UserModel.

Camada de Serviço (Refatoração):

[ ] Atualizar dev_service.py para usar DevModel.

[ ] Atualizar task_service.py para usar TaskModel (com Joins).

[ ] Atualizar demais serviços.