# Gerenciamento de Categorias com Streamlit e AWS RDS

Este projeto foi desenvolvido para os **alunos da UniFAAT** como parte das aulas de **Implementação de Software**. O objetivo é ensinar como conectar o Python a um banco de dados **AWS RDS** e demonstrar como criar uma aplicação interativa utilizando o framework **Streamlit** para realizar operações CRUD (Create, Read, Update, Delete) em uma tabela chamada `categories`.

---

## Funcionalidades

1. **Criar Categoria**: Adicione novas categorias com nome e descrição.
2. **Ler Categorias**: Visualize todas as categorias cadastradas no banco de dados.
3. **Atualizar Categoria**: Atualize o nome e a descrição de uma categoria existente.
4. **Deletar Categoria**: Exclua uma categoria pelo ID.

---

## Pré-requisitos

1. **Python 3.8+** instalado.
2. **Bibliotecas necessárias**:
   - `streamlit`
   - `psycopg2-binary`
   - `pyyaml`

   Instale as dependências com o comando:
   ```bash
   pip install streamlit psycopg2-binary pyyaml
   ```

3. **Banco de Dados AWS RDS**:
   - Um banco de dados PostgreSQL configurado no AWS RDS.
   - Certifique-se de que o IP da sua máquina está autorizado no grupo de segurança do RDS.

4. **Arquivo de Configuração (`config.yml`)**:
   - Crie um arquivo `config.yml` no mesmo diretório do código com as credenciais do banco de dados. Exemplo:
     ```yaml
     database:
       host: "your-rds-endpoint.amazonaws.com"
       port: 5432
       user: "your-username"
       password: "your-password"
       dbname: "your-database-name"
     ```

---

## Estrutura do Repositório

A estrutura do repositório é a seguinte:

```
AulaRDS/
│
├── crud.py          # Código principal da aplicação Streamlit
├── config.yml       # Arquivo de configuração com as credenciais do banco de dados
├── Readme.md        # Documentação do projeto
├── requirements.txt # Lista de dependências do projeto
└── northwind.sql    # Script SQL para criar a tabela e popular o banco de dados
```

---

## Como Utilizar o Repositório

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/AleTavares/trabalhandocomrds.git
   cd trabalhandocomrds
   ```

2. **Configure o banco de dados**:
   - Certifique-se de que o banco de dados PostgreSQL no AWS RDS está configurado.
   - Execute o script `northwind.sql` no banco de dados para criar a tabela `categories` e outros objetos necessários.

3. **Configure o arquivo `config.yml`**:
   - Insira as credenciais do banco de dados no arquivo `config.yml`.

4. **Instale as dependências**:
   - Utilize o arquivo `requirements.txt` para instalar as dependências:
     ```bash
     pip install -r requirements.txt
     ```

5. **Execute a aplicação**:
   - Inicie o Streamlit com o comando:
     ```bash
     streamlit run crud.py
     ```

6. **Acesse a aplicação**:
   - Abra o navegador e acesse o endereço exibido pelo Streamlit (geralmente `http://localhost:8501`).

---

## Observações

- **Segurança**: Não compartilhe o arquivo `config.yml` publicamente, pois ele contém credenciais sensíveis.
- **Permissões no RDS**: Certifique-se de que o usuário do banco de dados possui permissões para realizar operações CRUD na tabela `categories`.
- **Tabela `categories`**:
  Certifique-se de que a tabela `categories` existe no banco de dados com a seguinte estrutura:
  ```sql
  CREATE TABLE categories (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description TEXT
  );
  ```

---

## Desafio

Além das funcionalidades implementadas, este repositório inclui um arquivo chamado [`DESAFIO.md`](./DESAFIO.md), que contém uma proposta de atividade prática para aprofundar os conhecimentos adquiridos. O desafio envolve a criação de novas funcionalidades ou melhorias na aplicação, incentivando o aprendizado prático.

Certifique-se de ler o arquivo e tentar resolver o desafio para consolidar os conceitos apresentados no projeto.

---

## Próximos Passos

- Adicionar autenticação para proteger a aplicação.
- Melhorar a interface do usuário com mais validações e feedback.
- Implementar paginação para a listagem de categorias.

---

## Licença

Este projeto é apenas para fins educacionais e foi desenvolvido para os alunos da UniFAAT. Sinta-se à vontade para utilizá-lo e modificá-lo conforme necessário.

## README

Este é um projeto Streamlit para gerenciamento de funcionários armazenados em um banco de dados PostgreSQL no Amazon RDS (Relational Database Service).

**Visão Geral:**

A aplicação oferece uma interface web interativa para realizar as operações básicas de CRUD (Criar, Ler, Atualizar e Deletar) em uma tabela de funcionários. As credenciais de conexão com o banco de dados são carregadas de um arquivo de configuração YAML (`config.yml`).

**Pré-requisitos:**

* **Python 3.6+:** Certifique-se de ter o Python instalado em seu sistema.
* **Bibliotecas Python:** As seguintes bibliotecas são necessárias e podem ser instaladas usando o pip:
    ```bash
    pip install streamlit psycopg2 pyyaml
    ```
* **Arquivo de Configuração `config.yml`:** Um arquivo YAML chamado `config.yml` deve estar presente no mesmo diretório do script Python, contendo as informações de conexão com o seu banco de dados RDS PostgreSQL. O formato esperado do arquivo é:

    ```yaml
    database:
      host: "your_rds_host"
      port: 5432
      user: "your_rds_user"
      password: "your_rds_password"
      dbname: "your_rds_dbname"
    ```

    Substitua os valores entre as aspas pelas suas credenciais reais do RDS.

* **Banco de Dados PostgreSQL no AWS RDS:** Você precisa ter uma instância do PostgreSQL rodando no AWS RDS e uma tabela chamada `employees` configurada com as seguintes colunas (mínimo):
    * `employee_id` (INTEGER PRIMARY KEY)
    * `first_name` (VARCHAR)
    * `last_name` (VARCHAR)
    * `title` (VARCHAR)
    * `hire_date` (DATE)

**Como Executar a Aplicação:**

1. **Salve o código Python:** Salve o código Python fornecido em um arquivo chamado `app.py` (ou outro nome de sua preferência).
2. **Crie o arquivo `config.yml`:** Crie um arquivo chamado `config.yml` no mesmo diretório de `app.py` e preencha com as suas credenciais do RDS conforme o formato especificado nos pré-requisitos.
3. **Abra o terminal:** Navegue até o diretório onde você salvou os arquivos.
4. **Execute o Streamlit:** Rode o seguinte comando no seu terminal:
    ```bash
    streamlit run app.py
    ```
5. **Acesse no navegador:** O Streamlit irá abrir automaticamente uma nova aba no seu navegador com a interface da aplicação. Se não abrir, procure no terminal o endereço local (geralmente `http://localhost:8501`).

**Funcionalidades:**

A aplicação oferece as seguintes funcionalidades através de um menu de navegação na barra lateral:

* **Criar:** Permite adicionar um novo funcionário ao banco de dados, solicitando o primeiro nome, último nome, título e data de contratação. O `employee_id` é gerado automaticamente.
* **Ler:** Exibe uma lista de todos os funcionários cadastrados no banco de dados, mostrando o ID, nome completo, título e data de contratação.
* **Atualizar:** Permite selecionar um funcionário pelo ID e atualizar seu primeiro nome, último nome e título.
* **Deletar:** Permite selecionar um funcionário pelo ID e removê-lo do banco de dados.

**Observações:**

* **Segurança:** As credenciais do banco de dados são armazenadas em um arquivo YAML local. Em um ambiente de produção, é altamente recomendável utilizar métodos mais seguros para gerenciar credenciais, como variáveis de ambiente ou um serviço de gerenciamento de segredos.
* **Tratamento de Erros:** O código fornecido possui um tratamento básico de sucesso nas operações. Em uma aplicação mais robusta, seria importante adicionar tratamento de erros para falhas de conexão com o banco de dados ou outras exceções.
* **Validação de Dados:** A aplicação não implementa validação de dados nos formulários. Adicionar validação para garantir a integridade dos dados inseridos seria um aprimoramento importante.