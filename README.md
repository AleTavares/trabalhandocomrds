# Gerenciamento de Categorias e Customers com Streamlit e AWS RDS

Este projeto foi desenvolvido para os **alunos da UniFAAT** como parte das aulas de **Implementação de Software**. O objetivo é ensinar como conectar o Python a um banco de dados **AWS RDS** e demonstrar como criar uma aplicação interativa utilizando o framework **Streamlit** para realizar operações CRUD (Create, Read, Update, Delete) em duas tabelas: `categories` e `customers`.

---

## Funcionalidades Principais

### 1. Tabela **categories**

* **Criar Categoria**: Adicione novas categorias com nome e descrição.
* **Ler Categorias**: Visualize todas as categorias cadastradas em formato de tabela interativa.
* **Atualizar Categoria**: Atualize o nome e a descrição de uma categoria existente.
* **Deletar Categoria**: Exclua uma categoria pelo ID.

### 2. Tabela **customers** *(Nova)*

* **Criar Customer**: Insira um cliente com todos os campos:

  * `customer_id` (VARCHAR(5))
  * `company_name` (VARCHAR(40))
  * `contact_name` (VARCHAR(30))
  * `contact_title` (VARCHAR(30))
  * `address` (VARCHAR(60))
  * `city` (VARCHAR(15))
  * `region` (VARCHAR(15))
  * `postal_code` (VARCHAR(10))
  * `country` (VARCHAR(15))
  * `phone` (VARCHAR(24))
  * `fax` (VARCHAR(24))
* **Ler Customers**: Exibe todos os registros da tabela `customers` em uma tabela interativa `st.dataframe`, com colunas mapeadas para cada atributo.
* **Atualizar Customer**: Selecione o `customer_id` e altere qualquer um dos campos acima, mantendo consistência dos dados.
* **Deletar Customer**: Remova um cliente existente através do seu `customer_id`.

---

## Pré-requisitos

1. **Python 3.8+** instalado.

2. **Bibliotecas necessárias**:

   * `streamlit`
   * `psycopg2-binary`
   * `pyyaml`
   * `pandas`

   Instale as dependências com o comando:

   ```bash
   pip install streamlit psycopg2-binary pyyaml pandas
   ```

3. **Banco de Dados AWS RDS**:

   * Um banco de dados PostgreSQL configurado no AWS RDS.
   * Autorize o IP da sua máquina no grupo de segurança do RDS.

4. **Arquivo de Configuração (`config.yml`)**:

   * Crie um arquivo `config.yml` no mesmo diretório do código com as credenciais do banco de dados. Exemplo:

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

```
AulaRDS/
│
├── crud_app.py       # Código principal da aplicação Streamlit (categories + customers)
├── config.yml        # Credenciais do banco de dados
├── README.md         # Documentação do projeto
├── requirements.txt  # Lista de dependências do projeto
└── northwind.sql     # Script SQL para criar tabelas e popular o banco de dados
```

---

## Como Utilizar

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/AleTavares/trabalhandocomrds.git
   cd trabalhandocomrds
   ```

2. **Configure o banco de dados**:

   * No AWS RDS, execute o script `northwind.sql` para criar as tabelas `categories` e `customers`.

3. **Configure o arquivo `config.yml`**:

   * Preencha as credenciais do seu banco.

4. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a aplicação**:

   ```bash
   streamlit run crud_app.py
   ```

6. **Acesse a interface**:

   * Abra o navegador no endereço exibido pelo Streamlit (ex: `http://localhost:8501`).

---

## Observações

* **Segurança**: Nunca compartilhe o `config.yml` publicamente.
* **Permissões**: O usuário do banco deve ter direitos CRUD nas tabelas.
* **Tabelas SQL**:

  ```sql
  CREATE TABLE categories (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description TEXT
  );

  CREATE TABLE customers (
      customer_id VARCHAR(5) PRIMARY KEY,
      company_name VARCHAR(40) NOT NULL,
      contact_name VARCHAR(30),
      contact_title VARCHAR(30),
      address VARCHAR(60),
      city VARCHAR(15),
      region VARCHAR(15),
      postal_code VARCHAR(10),
      country VARCHAR(15),
      phone VARCHAR(24),
      fax VARCHAR(24)
  );
  ```

---

## Próximos Passos

* Autenticação de usuários para acesso restrito.
* Validações mais robustas nos formulários.
* Filtros e paginação nas tabelas.

---

## Licença

Este projeto é para fins educacionais, desenvolvido para alunos da UniFAAT. Fique à vontade para usar e adaptar conforme necessário.
