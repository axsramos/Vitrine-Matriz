📦 Notas de Versão: v0.4.0
Codinome: Visual Identity & Analytics

Data: 22 de Janeiro de 2026

🚀 Resumo das Novidades
Esta versão foca na experiência do usuário e na inteligência de dados. Implementamos uma identidade visual moderna baseada em estética Cyber-Tech e refatoramos as telas de análise para oferecer uma visão de 360 graus sobre o ciclo de vida das releases e a performance da equipe.

✨ Novas Funcionalidades e Melhorias
1. Identidade Visual Cyber-Tech (UI/UX)
Nova Paleta de Cores: Implementação de tema Dark Mode profundo (#0D0D2B) com acentos em Verde Neon (#00FF01).

Design de Componentes: Uso de degradês dinâmicos em botões de ação e na barra de navegação lateral para destacar a hierarquia visual.

Layout Responsivo de Portfólio: Refatoração da tela de equipe para exibição em grid de duas colunas, otimizando o espaço em resoluções desktop.

2. Dashboard Analítico Evoluído
KPIs de Saúde do Projeto: Novos indicadores de "Tarefas em Atraso" com alerta visual em vermelho e "Taxa de Conclusão Global".

Gráficos Avançados (Altair): Visualização de rosca para distribuição de status e gráfico de barras para carga de trabalho por desenvolvedor.

Header de Release: Destaque automático da última versão publicada no topo do painel de controle.

3. Changelog Inteligente (Notas de Versão)
Visualização por Abas: Separação entre "Histórico Recente" e "Agrupamento Mensal/Anual".

Rastreabilidade de Devs: Exibição explícita de quais desenvolvedores atuaram em cada versão e a quantidade exata de tarefas entregues por release.

Tratamento de Dados (Anti-Crash): Implementação de lógica para lidar com datas nulas (NaTType), garantindo a estabilidade da página.

4. Gestão Administrativa
Promoção de Usuários: Fluxo simplificado na tela de Gerenciamento de Usuários para promover perfis comuns a "Desenvolvedores" com um clique.

Auto-provisionamento em T_Dev: Criação automática do registro técnico ao promover um usuário, mantendo a integridade referencial.

🛠️ Mudanças na Infraestrutura (Bastidores)
Refatoração de Banco de Dados: Migração dos campos de release para a nova nomenclatura padronizada: RelVrs (Versão), RelDat (Data) e RelTtlCmm (Comentário).

Service Layer Expansion: Evolução do DashboardService e ReleaseService para suportar queries complexas com GROUP_CONCAT e JOIN entre tarefas e desenvolvedores.

Segurança e Acesso: Reforço do require_auth com validação de allowed_roles=['admin'] para funções críticas de sistema.

📊 Impacto de Negócio
Engajamento da Equipe: O novo portfólio visual valoriza o trabalho individual e facilita a identificação de especialistas por área.

Controle de Prazos: A visibilidade imediata de tarefas atrasadas no dashboard reduz o tempo de resposta da gestão para gargalos de produtividade.

Comunicação com Stakeholders: As notas de versão agrupadas por mês oferecem uma visão clara do ritmo de inovação da empresa.