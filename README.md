# Vitrine-Matriz
Geração de Release Notes e Portfólio Profissional

<img src="https://img.shields.io/badge/license-MIT-green"><img/>
<img src="https://img.shields.io/badge/version-0.0.1-blue"><img/>
<img src="https://img.shields.io/badge/biuld-2601111120-orange"><img/>

Ver mais em [Changelog](./docs/semver/changelog.md)

---

O Vitrine Matriz é uma plataforma centralizadora para gestão de transparência técnica e valorização profissional. O projeto automatiza a geração de Release Notes da aplicação Portal Matriz e cria um Portfólio Dinâmico para os desenvolvedores, integrando-se diretamente ao gerenciador de tarefas Bitrix24.

📌 Objetivos
Release Notes: Transformar tarefas concluídas no Bitrix24 em notas de versão públicas e organizadas.

Portfólio Dev: Exibir o histórico de contribuições e o impacto técnico de cada desenvolvedor da equipe.

Automação: Reduzir o trabalho manual no momento da publicação (deploy no IIS).

🛠️ Stack Tecnológica
Linguagem: Python 3.x

Interface Web: Streamlit

Banco de Dados: SQLite

Integração: Bitrix24 REST API

📂 Estrutura do Projeto

```Plaintext
vitrine_matriz/
├── data/               # Banco de dados SQLite (.db)
├── src/
│   ├── app.py          # Arquivo principal Streamlit
│   ├── database.py     # Lógica de persistência e modelos
│   ├── bitrix_api.py   # Conexão e extração de dados do Bitrix24
│   └── components/     # Componentes visuais (cards, layouts)
├── requirements.txt    # Dependências do projeto
└── README.md
```

🔧 Configuração Inicial
1. Clone o repositório:
```Bash
git clone https://github.com/axsramos/vitrine-matriz.git
```

2. Crie um ambiente virtual e instale as dependências:
```Bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
Execute a aplicação:
```

3. Execute a aplicação:
```Bash
streamlit run src/app.py
Fontes e Referências Técnicas
```
