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
