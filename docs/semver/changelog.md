# Vitrine-Matriz
**Portal de Transparência, Performance e Gestão de Releases.**

Voltar para [README](/README.md)

# Changelog

Todas as alterações relevantes a este projeto serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) 
e este projeto adere ao [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!--
## [Unreleased]
Não lançado: Desenvolvimento em andamento.

### Added
Adicionado: Para novas funcionalidades.

### Changed
Modificado: Para alterações em funcionalidades existentes.

### Deprecated
Obsoleto: Para funcionalidades que estão para ser removidas.

### Removed
Removido: Para funcionalidades removidas nesta versão.

### Fixed
Corrigido: Para qualquer correção de bug.

### Security 
Segurança: Em caso de vulnerabilidades.
-->

---

## [0.4.0](./v0.4.0/whatsnew.md) - 22/01/2026
### Identidade Visual e Inteligência Analítica
#### Adicionado:
- **Nova Interface Cyber-Tech:** Implementação de Dark Mode profundo com paleta de cores neon (#00FF01) e degradês dinâmicos.
- **Dashboard Evoluído:** Gráficos interativos (Altair) para carga de trabalho por dev e status de atividades.
- **KPIs de Saúde:** Indicadores em tempo real para tarefas em atraso, taxa de conclusão e última release.
- **Navegação Inteligente:** Changelog com visualização por abas (Histórico vs. Mensal) e rastreabilidade de desenvolvedores por versão.
- **Gestão de Perfil:** Funcionalidade de promoção de usuários para o nível "Desenvolvedor" com criação automática de perfil técnico.

#### Modificado:
- **Estrutura de Release:** Refatoração completa da tabela `T_Rel` para suporte a campos de data e títulos comunicativos padronizados.
- **Portfólio em Grid:** Exibição da equipe otimizada para duas colunas, melhorando a densidade de informação.
- **Service Layer:** Expansão dos serviços de Dashboard e Release para suportar queries analíticas complexas.

#### Corrigido:
- **Estabilidade de Datas:** Tratamento de erro para registros sem data informada (*NaTType*) nas notas de versão.
- **Integridade Referencial:** Correção no vínculo entre tarefas e releases no momento da finalização em massa.

## [0.3.0](./v0.3.0/whatsnew.md) - 15/01/2026 
### Ferramentas de Gestão Estratégica
#### Adicionado:
- **Score de Impacto (Business Value):** Introdução de classificação categórica (Baixo, Médio, Alto, Crítico) para cada tarefa técnica.
- **Filtros de Período Dinâmicos:** Painel de controle na Home que permite filtrar KPIs e gráficos por intervalo de datas customizado.
- **Motor de Relatórios PDF:** Nova página de exportação que gera documentos profissionais para Notas de Versão, Performance de Equipe e Atividades por Período.
- **Visualização de Portfólio Refinada:** Histórico individual de desenvolvedores com foco em descrição de valor de negócio e timeline de entregas.

#### Modificado:
- **Service Layer Refactoring:** Centralização da lógica de negócio nos serviços (Task, Dashboard, Report), seguindo padrões de Clean Code.
- **Segurança SQL:** Implementação de parametrização em todas as consultas (prevenção contra SQL Injection).
- **Padronização Visual:** Implementação de herança na classe ReportService para garantir cabeçalhos e rodapés institucionais em todos os documentos.

## [0.2.0](./v0.2.0/whatsnew.md) - 14/01/2026 
### Segurança e Acesso
#### Adicionado:
- **Sistema de Autenticação:** Implementação de tela de login integrada ao banco de dados SQLite.
- **Gestão de Usuários (CRUD):** Interface administrativa para cadastrar, visualizar e remover operadores do sistema.
- **Self-Service de Senha:** Funcionalidade que permite ao usuário logado alterar sua própria senha de acesso.
- **Menu Dinâmico:** O menu lateral agora se adapta ao perfil do usuário (Logado vs. Visitante), exibindo apenas as opções permitidas.

## [0.1.0](./v0.1.0/whatsnew.md) - 11/01/2026 
### Geração de Release Notes e Portfólio Profissional
#### Adicionado:
- **Dashboard Estratégico:** Visão geral de entregas, releases e roadmap futuro.
- **Portfólio da Equipe:** Perfis detalhados com fotos, biografia e histórico de entregas.
- **Gestão de Releases:** Agrupamento de tarefas em versões oficiais com títulos comunicativos.
- **Lançamento de Tarefas:** Cadastro manual de entregas (contingência) com foco no **Impacto de Negócio**.
- **Relatórios em PDF:** Geração automática de Notas de Versão e Relatórios de Performance da Equipe (Consolidado).
- **Backlog Dinâmico:** Roadmap de desenvolvimento lido diretamente de arquivos Markdown.
