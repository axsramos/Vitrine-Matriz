# 🚀 O que há de novo na Versão 0.6.0

**Codinome:** *Speranza* | **Data:** 04/02/2026

Esta é uma das atualizações mais importantes da história do **Vitrine de Matriz**. Focamos em reescrever o "motor" do sistema para garantir que ele seja rápido, seguro e escalável, além de renovar a experiência de uso diário.

---

### ✨ Destaques Principais

#### 1. Segurança de Verdade 🔐

A segurança deixou de ser básica. Implementamos criptografia de ponta a ponta para as senhas (usando **Bcrypt**).

* **Antes:** Senhas visíveis no banco de dados.
* **Agora:** Hash criptográfico irreversível. Ninguém, nem mesmo o administrador, consegue ler a sua senha.

#### 2. Performance: "Adeus, Lentidão" ⚡

Removemos componentes pesados (Pandas) do núcleo de processamento. O sistema agora utiliza estruturas nativas do Python.

* **Resultado:** O carregamento das páginas, especialmente o Dashboard e as Listas de Tarefas, está significativamente mais rápido e consome menos memória do servidor.

#### 3. Nova Gestão de Tarefas 📝

A tela de **Cadastrar Tarefa** foi totalmente redesenhada pensando na sua produtividade.

* **Abas Organizadas:** Separamos o cadastro ("Nova Tarefa") da execução ("Minhas Pendências").
* **Ações em Lote:** Agora você pode selecionar múltiplas tarefas na sua lista e clicar em **"🏁 Concluir"** ou **"🗑️ Excluir"** de uma só vez.
* **Datas Inteligentes:** O campo de prazo agora usa um calendário visual intuitivo e robusto.

---

### 🎨 Melhorias Visuais e de Navegação

* **🏠 Nova Página Inicial:** Ao entrar, você é recebido por uma *Landing Page* limpa, com a identidade visual da aplicação e atalhos rápidos para Login ou Dashboard.
* **🛡️ Menu Inteligente:** O menu lateral agora sabe exatamente quem você é. Se você é um Desenvolvedor, vê suas ferramentas; se é Gerente, vê os relatórios. Nada de links quebrados ou telas de "Acesso Negado".
* **📊 Gráficos Precisos:** Corrigimos os gráficos do Dashboard que, por vezes, não exibiam corretamente as categorias de texto.

---

### 🛠️ Para Desenvolvedores (Técnico)

* **Refatoração MVC/Service:** A arquitetura agora segue estritamente a separação de responsabilidades. A UI não fala com o Banco; ela fala com o Serviço, que fala com o Modelo.
* **Tipagem Forte:** Substituímos strings soltas por `Enums` (`TaskStatus`, `TaskTip`, `UserRole`), garantindo integridade dos dados e facilitando a manutenção.
* **Fix de Update:** Corrigido um bug crítico no ORM que apagava dados obrigatórios (como Título) ao atualizar apenas o Status de uma tarefa. Implementamos o padrão *Read-Modify-Write*.

---

### 🐛 Correções de Bugs

* Corrigido erro que impedia a edição de datas na grid de tarefas (`StreamlitAPIException`).
* Corrigido falha silenciosa ao tentar concluir tarefas sem carregar o objeto completo.
* Ajustado o mapeamento de campos entre a tela e o banco (`TrfSit` vs `TrfStt`).

---

### 🔮 O que vem por aí?

Com a base (Core) estabilizada nesta versão 0.6.0, estamos prontos para focar 100% em novas funcionalidades de **Inteligência de Dados** e **Automação de Relatórios** nas próximas sprints.

*Equipe Vitrine de Matriz*