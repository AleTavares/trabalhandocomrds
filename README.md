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

## Funcionalidade Adicionada

Implementação das operações CRUD para a tabela `products`, permitindo criar, listar, atualizar e remover produtos.
