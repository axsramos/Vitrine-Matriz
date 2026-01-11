# Vitrine-Matriz  
Geração de Release Notes e Portfólio Profissional  

## Representação do Projeto

```Plaintext
vitrine_matriz/
├── .env                # Variáveis de ambiente (API Keys, Webhooks)
├── .gitignore          # Ignorar venv, .db e .env
├── requirements.txt    # Dependências (streamlit, pandas, requests)
├── data/
│   └── database.db     # O arquivo SQLite
├── src/
│   ├── app.py          # Entry point (Onde o Streamlit inicia)
│   ├── core/           # Configurações centrais e conexão DB (O "Model" base)
│   │   ├── config.py
│   │   └── database.py
│   ├── services/       # Lógica de negócio e integrações (Equivalente ao Controller)
│   │   ├── bitrix_service.py
│   │   └── release_service.py
│   ├── ui/             # Páginas e Componentes (O "View")
│   │   ├── components/ # Elementos reutilizáveis (cards, headers)
│   │   └── pages/      # Subpáginas (Release Notes, Portfólio)
│   └── utils/          # Funções auxiliares (formatação de data, etc)
└── assets/             # CSS customizado e imagens (logo da empresa)
```

---

## Dependências

As bibliotecas fundamentais para iniciar:

```Plaintext
streamlit
pandas
python-dotenv
requests
```

