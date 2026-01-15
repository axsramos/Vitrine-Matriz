# Vitrine-Matriz
**Portal de Transparência, Performance e Gestão de Releases.**

## 📦 Notas de Versão: v0.2.0
**Data:** 14 de Janeiro de 2026

> Status: Stable Release

## 🚀 Resumo das Novidades
Esta versão marca a conclusão do módulo de Segurança e Gestão de Acessos. Agora, o portal possui áreas restritas e protegidas por criptografia, permitindo que múltiplos administradores gerenciem o conteúdo de forma segura.

## ✨ Novas Funcionalidades
- **Sistema de Autenticação:** Implementação de tela de login integrada ao banco de dados SQLite.
- **Gestão de Usuários (CRUD):** Interface administrativa para cadastrar, visualizar e remover operadores do sistema.
- **Self-Service de Senha:** Funcionalidade que permite ao usuário logado alterar sua própria senha de acesso.
- **Menu Dinâmico:** O menu lateral agora se adapta ao perfil do usuário (Logado vs. Visitante), exibindo apenas as opções permitidas.

## 🛡️ Segurança e Infraestrutura
- **Criptografia SHA-256:** As senhas não são mais armazenadas em texto simples, utilizando hashing para proteção de dados.
- **Middleware de Proteção:** Implementação de bloqueio de rotas para impedir que páginas administrativas sejam acessadas via URL direta por usuários não autenticados.
- **Configuração via .env:** Parametrização de títulos e subtítulos globais, facilitando o deploy em diferentes ambientes.
- **Clean Code (DRY):** Refatoração da inicialização de páginas e títulos para funções centralizadas em src/core/ui_utils.py.

## 📈 Impacto de Negócio
- **Integridade dos Dados:** Somente pessoal autorizado pode alterar informações de releases e tarefas.
- **Privacidade:** Informações estratégicas de gestão agora ficam ocultas para o público externo, mantendo apenas o portfólio e as notas de versão como consulta pública.
- **Escalabilidade:** A estrutura está pronta para receber novos módulos (como a integração Bitrix24) com a base de usuários já estabelecida.

## 🛠️ Mudanças Técnicas (Technical Changes)
- **Database:** Executada migration 02_create_users_table.sql.
- **Dependencies:** Adicionada biblioteca python-dotenv ao requirements.txt.
- **Core:** Adicionado auth_middleware.py para controle de fluxo de execução.
