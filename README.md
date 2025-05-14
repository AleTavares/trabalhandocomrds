# Gerenciamento de Territórios com Streamlit e AWS RDS

Este projeto foi desenvolvido para demonstrar como conectar o Python a um banco de dados AWS RDS e criar uma aplicação interativa utilizando o framework Streamlit. O objetivo é facilitar a realização de operações CRUD (Create, Read, Update, Delete) em uma tabela chamada **territories**.

## Funcionalidades

* **Criar Território:** Adicione novos territórios com identificador, descrição e região.
* **Ler Territórios:** Visualize todos os territórios cadastrados no banco de dados.
* **Atualizar Território:** Atualize as informações de um território existente.
* **Deletar Território:** Exclua um território pelo ID.

## Pré-requisitos

* Python 3.8+ instalado.

### Bibliotecas necessárias:

* **streamlit** - Criação da interface web.
* **psycopg2-binary** - Conexão com o banco de dados PostgreSQL.
* **pyyaml** - Leitura das configurações do arquivo `config.yml`.

Instale as dependências com o comando:

```bash
pip install streamlit psycopg2-binary pyyaml
```

### Banco de Dados AWS RDS:

* Um banco de dados PostgreSQL configurado no AWS RDS.
* Certifique-se de que o IP da sua máquina está autorizado no grupo de segurança do RDS.

### Arquivo de Configuração (`config.yml`):

Crie um arquivo `config.yml` no mesmo diretório do código com as credenciais do banco de dados. Exemplo:

```yaml
database:
  host: "your-rds-endpoint.amazonaws.com"
  port: 5432
  user: "your-username"
  password: "your-password"
  dbname: "your-database-name"
```

## Estrutura do Repositório

```
TerritoriesProject/
│
├── crud.py          # Código principal da aplicação Streamlit
├── config.yml       # Arquivo de configuração com as credenciais do banco de dados
├── README.md        # Documentação do projeto
├── requirements.txt # Lista de dependências do projeto
└── northwind.sql  # Script SQL para criar a tabela e popular o banco de dados
```

## Como Utilizar o Repositório

### 1. Clone o repositório:

```bash
git clone https://github.com/SeuUsuario/territories-project.git
cd territories-project
```

### 2. Configure o banco de dados:

Certifique-se de que o banco de dados PostgreSQL no AWS RDS está configurado.
Execute o script `territories.sql` no banco de dados para criar a tabela **territories**:

```sql
CREATE TABLE territories (
    territory_id character varying(20) NOT NULL,
    territory_description character varying(60) NOT NULL,
    region_id smallint NOT NULL
);
```

### 3. Configure o arquivo `config.yml`:

Insira as credenciais do banco de dados no arquivo `config.yml`.

### 4. Instale as dependências:

Utilize o arquivo `requirements.txt` para instalar as dependências:

```bash
pip install -r requirements.txt
```

### 5. Execute a aplicação:

Inicie o Streamlit com o comando:

```bash
streamlit run crud.py
```

### 6. Acesse a aplicação:
Abra o navegador e acesse o endereço exibido pelo Streamlit (geralmente `http://localhost:8501`).

## Observações Importantes

* **Segurança:** Não compartilhe o arquivo `config.yml` publicamente, pois ele contém credenciais sensíveis.
* **Permissões no RDS:** Certifique-se de que o usuário do banco de dados possui permissões para realizar operações CRUD na tabela **territories**.

## Próximos Passos

* Adicionar autenticação para proteger a aplicação.
* Melhorar a interface do usuário com mais validações e feedback.
* Implementar paginação para a listagem de territórios.