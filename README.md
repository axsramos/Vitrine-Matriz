# Vitrine-Matriz
**Portal de Transparência, Performance e Gestão de Releases.**

<img src="https://img.shields.io/badge/license-MIT-green"><img/>
<img src="https://img.shields.io/badge/version-5.0.0-blue"><img/>
<img src="https://img.shields.io/badge/build-202601270748-orange"><img/>

Ver mais em [Changelog](./docs/semver/changelog.md)

---

O **Vitrine Matriz** é uma aplicação desenvolvida em Python e Streamlit projetada para gerenciar o portfólio técnico da equipe de desenvolvimento do **Portal Matriz**, consolidar notas de versão (Releases) e gerar relatórios executivos para a diretoria.

---

## 🛠️ Principais Funcionalidades

- **Dashboard Estratégico:** Visão geral de entregas, releases e roadmap futuro.
- **Portfólio da Equipe:** Perfis detalhados com fotos, biografia e histórico de entregas.
- **Gestão de Releases:** Agrupamento de tarefas em versões oficiais com títulos comunicativos e sugestão automática de versão.
- **Central de Relatórios:** Módulo dedicado para geração de documentos oficiais (Geral e Mensal) em PDF com filtros de período.
- **Navegação Dinâmica:** Sistema de rotas inteligente com controle de acesso por perfil (Admin/User).
- **Backlog Dinâmico:** Roadmap de desenvolvimento lido diretamente de arquivos Markdown.

---

## 💻 Tecnologias Utilizadas

- **Linguagem:** [Python 3.12+](https://www.python.org/)
- **Interface:** [Streamlit](https://streamlit.io/)
- **Banco de Dados:** SQLite (com Mixins para persistência)
- **Motor de PDF:** [FPDF2](https://fpdf2.github.io/fpdf2/) (Suporte a renderização direta e HTML)
- **Manipulação de Dados:** Pandas
- **Ambiente de Desenvolvimento:** Laragon (Windows)
- **Editor:** VS Code

---

📂 Estrutura do Projeto

```Plaintext
Vitrine-Matriz/
├── .venv/                # Ambiente virtual Python
├── assets/
│   └── uploads/          # Fotos de perfil dos desenvolvedores
├── data/
│   └── backlog.md        # Planejamento de versões futuras
├── migrations/
│   └── 01_schema_v1_baseline.sql # Script de criação do banco
├── src/
│   ├── core/             # Conexão DB, Configurações e Mixins
│   ├── models/           # Classes de domínio (ORM-like)
│   ├── reports/
│   │   └── templates/    # Templates HTML para geração de PDFs
│   ├── services/         # Lógica de negócio e acesso a dados
│   └── ui/
│       ├── navigation.py # Orquestrador de menus e rotas
│       └── pages/        # Telas da aplicação (Dashboard, Relatórios, etc.)
└── app.py                # Ponto de entrada da aplicação
---

🔧 Configuração Inicial
1. Clone o repositório:
```Bash
git clone [https://github.com/axsramos/Vitrine-Matriz.git](https://github.com/axsramos/Vitrine-Matriz.git)
cd Vitrine-Matriz
```

2. Crie um ambiente virtual e instale as dependências:
```Bash
python -m venv .venv
source .venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Instalar e atualizar base de dados 
```Bash
python run_migrations.py
```

4. Carregar dados de exemplo **opcional**
```Bash
python seed_db.py
```

5. Execute a aplicação:
```Bash
streamlit run app.py
```

© 2026 Vitrine-Matriz - Desenvolvido para gestão ágil e transparência técnica.

👨‍💻 Desenvolvido por:
Alex Ramos - GitHub: axsramos
