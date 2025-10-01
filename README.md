Web Scraping de Imóveis com Selenium (Estudo)

Este projeto foi criado como exercício de estudo para praticar automação de navegação na web usando Python + Selenium.
A ideia foi acessar o sistema da Embraesp (geoembraesp.com.br), realizar login, aplicar filtros, navegar entre imóveis e coletar dados detalhados das fichas de cada empreendimento, salvando tudo em um CSV.

🚀 O que o script faz

    - Faz login no sistema com usuário e senha.
    - Abre o modal de busca de imóveis.
    - Pesquisa por uma zona de valor (ex: AEROPORTO).
    - Captura a lista de imóveis carregados na lateral.
    - Coleta dados em cada página 
    - Percorre também as fichas e fases disponíveis para capturar informações extras.
    - Salva todos os dados em um arquivo CSV com o nome da zona pesquisada.

📦 Tecnologias usadas

   - Python 3
   - Selenium
   - ChromeDriver
   - CSV para exportação

⚙️ Como rodar o projeto

1. Clone o repositório
    ```
    git clone https://github.com/kelson-gs/web-scraping-python.git
    cd web-scraping-python
    ```
3. Instale as dependências
    ```
    pip install -r requirements.txt
    ```
5. Configure suas credenciais

    No código, altere estas linhas para o seu usuário e senha válidos:
    ```
    username_input.send_keys("email")
    password_input.send_keys("senha")
    ```
6. Rode o script
   ```
    python main.py
   ```
📂 Saída dos dados

Um arquivo CSV será criado na raiz do projeto com o nome da zona pesquisada.
Exemplo:

    AEROPORTO.csv
