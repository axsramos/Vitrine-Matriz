# 🚀 Notas de Versão: v1.0.0

Seja bem-vindo à primeira versão oficial do nosso portal de transparência! Esta ferramenta foi criada para aproximar você do nosso processo de desenvolvimento, dando visibilidade total ao talento da nossa equipe e à evolução do nosso software.

### 🌟 Destaques desta Versão
**Portfólio Interativo da Equipe:** Agora você pode conhecer quem está por trás de cada linha de código. Cada desenvolvedor possui um perfil com sua especialidade e histórico de conquistas.

**Notas de Versão Simplificadas:** Chega de termos técnicos complexos. Agora, cada atualização do sistema vem acompanhada de um resumo do Impacto de Negócio, explicando exatamente o que mudou para o usuário final.

**Relatórios Oficiais em um Clique:** Precisa de um documento para uma reunião? Geramos relatórios em PDF profissionais com o resumo das entregas e performance da equipe instantaneamente.

**Painel de Transparência (Home):** Uma visão rápida de quantas melhorias foram implementadas e o que já está planejado para o futuro próximo.

---

# 🚀 Notas de Versão: v2.0.0

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

---

# 🚀 Notas de Versão: v3.0.0

## 🚀 Resumo das Novidades
Esta versão consolida as ferramentas de gestão estratégica, permitindo que a liderança visualize não apenas "o que" foi feito, mas o valor real entregue ao negócio através de métricas de impacto e relatórios automatizados.

## ✨ Novas Funcionalidades (Management Features)
**Score de Impacto (Business Value):** Introdução de classificação categórica (Baixo, Médio, Alto, Crítico) para cada tarefa técnica.

**Filtros de Período Dinâmicos:** Painel de controle na Home que permite filtrar KPIs e gráficos por intervalo de datas customizado.

**Motor de Relatórios PDF:** Nova página de exportação que gera documentos profissionais para Notas de Versão, Performance de Equipe e Atividades por Período.

**Visualização de Portfólio Refinada:** Histórico individual de desenvolvedores com foco em descrição de valor de negócio e timeline de entregas.

## 🛡️ Melhorias de Infraestrutura e Refatoração
**Service Layer Refactoring:** Centralização da lógica de negócio nos serviços (Task, Dashboard, Report), seguindo padrões de Clean Code.

**Segurança SQL:** Implementação de parametrização em todas as consultas (prevenção contra SQL Injection).

**Padronização Visual:** Implementação de herança na classe ReportService para garantir cabeçalhos e rodapés institucionais em todos os documentos.

## 📊 Impacto de Negócio
**Tomada de Decisão:** Facilita a identificação de Quick Wins e tarefas críticas através do gráfico de distribuição de impacto.

**Transparência:** Relatórios em PDF prontos para envio a stakeholders e diretoria.

**Auditoria:** Registro completo de quem realizou a entrega e qual o impacto gerado.

---

# 🚀 Notas de Versão: v4.0.0

## 🚀 Resumo das Novidades
A versão 0.4.0 transforma o Vitrine-Matriz em uma ferramenta de alta performance visual. Saímos de uma interface puramente funcional para um ambiente "Cyber-Tech" que facilita a leitura de dados críticos, permitindo que a gestão identifique gargalos em segundos através do novo Dashboard Analítico.

## ✨ Principais Destaques

**🎨 Identidade Cyber-Tech:** Uma experiência imersiva com Dark Mode e Verde Neon. O novo design não é apenas estético, mas funcional: os degradês e contrastes foram pensados para destacar botões de ação e alertas de atraso.

**📊 Dashboard de Comando:**
Agora é possível visualizar a carga de trabalho de toda a equipe em um gráfico de barras dinâmico e acompanhar a saúde das entregas via indicadores de "Atraso Crítico".

**📑 Changelog Estratégico:**
As notas de versão agora contam quem trabalhou em quê. Ao abrir uma versão, você visualiza a lista de desenvolvedores envolvidos e o volume de tarefas entregues naquela data.

**👥 Gestão de Time Simplificada:**
Administradores podem agora transformar qualquer usuário em um "Desenvolvedor" do portfólio com apenas um clique, automatizando a criação de registros na tabela técnica.

## 🛡️ Infraestrutura e Dados
- **Padronização SQL:** Migração dos campos de release para `RelVrs`, `RelDat` e `RelTtlCmm`.
- **Performance:** Consultas agregadas via SQL (JOINs e Group By) reduzindo o processamento no cliente.
- **UI Responsiva:** Cards de equipe e dashboards adaptáveis para diferentes resoluções.

## 📊 Impacto de Negócio
**Frequência de Release:** A facilidade em visualizar o histórico mensal incentiva entregas contínuas e documentadas.
**Visibilidade de Especialistas:** O novo portfólio em grid facilita a busca por responsáveis técnicos dentro da equipe.

---

# 🚀 Notas de Versão: v5.0.0
**Título:** Central de Relatórios e Estabilização de Interface

## 🛠️ O que há de novo?
**Central de Relatórios Dedicada:** Implementação de uma nova área para geração de documentos oficiais em PDF, separada da tela de consulta para melhor performance.

**Relatórios em PDF Estilizados:** Novos modelos de exportação (Geral e Mensal) com layout corporativo, utilizando desenho direto em PDF para garantir compatibilidade total em ambientes Windows/Laragon.

**Filtros de Referência:** Adicionada a capacidade de filtrar releases por período (Data Inicial e Final) antes da geração do relatório.

**Navegação Inteligente:** Refatoração do motor de rotas (navigation.py) para suportar redirecionamentos seguros para a tela de Login e organização dinâmica do menu lateral.

## 🐛 Correções e Melhorias
**Estabilidade de PDF:** Substituição da renderização HTML por métodos nativos do FPDF para evitar erros de tags não suportadas (como <span> e <div>).

**Performance de Consulta:** Otimização da função get_release_details para alimentar tanto a interface quanto os relatórios com os mesmos dados validados.

**UX/UI:** Padronização visual dos botões de ação e cards de informação seguindo a identidade visual do projeto.
