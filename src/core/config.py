import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Caminho base do projeto (onde está o app.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Caminho das páginas definido no .env ou padrão
# Exemplo no .env: PAGES_DIR=src/ui/pages/
PAGES_DIR = os.getenv("PAGES_DIR", "src/ui/pages/")

def get_page(page_name: str) -> str:
    """
    Retorna o caminho relativo da página para o Streamlit.
    Exemplo: get_page("01_Gerar_Release.py") -> "src/ui/pages/01_Gerar_Release.py"
    """
    return f"{PAGES_DIR}{page_name}"