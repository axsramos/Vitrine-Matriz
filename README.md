# Vitrine-Matriz
**Portal de Transparência, Performance e Gestão de Releases.**

<img src="https://img.shields.io/badge/license-MIT-green"><img/>
<img src="https://img.shields.io/badge/version-0.1.0-blue"><img/>
<img src="https://img.shields.io/badge/biuld-2601112012-orange"><img/>

Ver mais em [Changelog](./docs/semver/changelog.md)

---

O **Vitrine Matriz** é uma aplicação desenvolvida em Python e Streamlit projetada para gerenciar o portfólio técnico da equipe de desenvolvimento do **Portal Matriz**, consolidar notas de versão (Releases) e gerar relatórios de impacto de negócio para a diretoria.

---

## 🛠️ Principais Funcionalidades

- **Dashboard Estratégico:** Visão geral de entregas, releases e roadmap futuro.
- **Portfólio da Equipe:** Perfis detalhados com fotos, biografia e histórico de entregas.
- **Gestão de Releases:** Agrupamento de tarefas em versões oficiais com títulos comunicativos.
- **Lançamento de Tarefas:** Cadastro manual de entregas (contingência) com foco no **Impacto de Negócio**.
- **Relatórios em PDF:** Geração automática de Notas de Versão e Relatórios de Performance da Equipe (Consolidado).
- **Backlog Dinâmico:** Roadmap de desenvolvimento lido diretamente de arquivos Markdown.

---

## 🏗️ Arquitetura e Tecnologias

- **Linguagem:** Python 3.12+
- **Framework Web:** [Streamlit](https://docs.streamlit.io/)
- **Banco de Dados:** SQLite (com suporte a auditoria `AudIns`, `AudUpd`, `AudDlt`)
- **Geração de PDF:** [FPDF2](https://fpdf2.github.io/fpdf2/)
- **Manipulação de Dados:** Pandas
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
│   ├── services/         # Lógica de negócio e acesso a dados
│   └── ui/
│       └── pages/        # Telas da aplicação
└── app.py                # Ponto de entrada e orquestração de navegação
```

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

👨‍💻 Desenvolvido por:
Alex Ramos - GitHub: axsramos

Site Profissional: portalsiti.com.br

