# Desafio: Contribuindo com o Projeto - Pull Request

Bem-vindo ao desafio de contribuição! O objetivo deste desafio é que você, aluno da **UniFAAT**, pratique o uso de **Git** e **GitHub** para colaborar com um projeto real. Você deverá escolher uma das tabelas do banco de dados descritas no arquivo `northwind.sql` e implementar uma funcionalidade CRUD para ela no código existente.

---

## O Desafio

1. Escolha **uma tabela** do arquivo `northwind.sql` (exceto a tabela `categories`, que já está implementada).
2. Implemente as operações CRUD (Create, Read, Update, Delete) para a tabela escolhida no arquivo `crud.py`.
3. Atualize o arquivo `Readme.md` para incluir a descrição da funcionalidade que você implementou.
4. Faça um **Pull Request** no repositório para que sua contribuição seja revisada e integrada ao projeto.

---

## Pré-requisitos

Antes de começar, certifique-se de que você possui:

1. **Git instalado**: Verifique se o Git está instalado na sua máquina. Caso não esteja, instale-o a partir do site oficial: [https://git-scm.com/](https://git-scm.com/).
2. **Conta no GitHub**: Crie uma conta no GitHub, caso ainda não tenha.
3. **Python 3.8+ instalado**: Certifique-se de que o Python está instalado na sua máquina.
4. **Bibliotecas necessárias**:
   - Instale as dependências do projeto com o comando:
     ```bash
     pip install -r requirements.txt
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

## Como Participar

### 1. Faça o Fork do Repositório

1. Acesse o repositório original no GitHub.
2. Clique no botão **Fork** no canto superior direito para criar uma cópia do repositório na sua conta.

### 2. Clone o Repositório Forkado

1. No seu repositório forkado, clique no botão **Code** e copie o link HTTPS.
2. No terminal, execute:
   ```bash
   git clone <url-do-seu-fork>
   cd AulaRDS
   ```

### 3. Configure o Banco de Dados

1. Certifique-se de que o banco de dados PostgreSQL no AWS RDS está configurado.
2. Execute o script `northwind.sql` no banco de dados para criar as tabelas necessárias.

### 4. Configure o Arquivo `config.yml`

1. Insira as credenciais do banco de dados no arquivo `config.yml`:
   ```yaml
   database:
     host: "your-rds-endpoint.amazonaws.com"
     port: 5432
     user: "your-username"
     password: "your-password"
     dbname: "your-database-name"
   ```

### 5. Crie uma Branch para a Tabela Escolhida

1. No terminal, crie uma nova branch para a tabela que você escolheu:
   ```bash
   git checkout -b feature/<nome-da-tabela>
   ```

### 6. Implemente as Operações CRUD

1. Adicione as funções no arquivo `crud.py` para a tabela escolhida.
2. Teste sua implementação localmente.

### 7. Atualize o Readme

1. Inclua uma descrição da funcionalidade que você implementou no arquivo `Readme.md`.

### 8. Envie as Alterações

1. Adicione as alterações ao Git:
   ```bash
   git add .
   git commit -m "Implementação CRUD para a tabela <nome-da-tabela>"
   git push origin feature/<nome-da-tabela>
   ```

### 9. Abra um Pull Request

1. Acesse o repositório original no GitHub.
2. Clique no botão **Compare & Pull Request**.
3. Preencha o título e a descrição do Pull Request, explicando as mudanças realizadas.
4. **Inclua na descrição do Pull Request o seu RA e o seu nome completo.**
5. Envie o Pull Request.

---

## Exemplo de Implementação

Se você escolher a tabela `customers`, sua implementação no arquivo `crud.py` pode incluir funções como:

```python
def create_customer(customer_id, name, contact_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (customer_id, name, contact_name) VALUES (%s, %s, %s)", (customer_id, name, contact_name))
    conn.commit()
    conn.close()

def read_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_customer(customer_id, name, contact_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = %s, contact_name = %s WHERE customer_id = %s", (name, contact_name, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    conn.close()
```

---

## Dicas

- Leia o código existente para entender o padrão utilizado.
- Teste sua implementação localmente antes de enviar o Pull Request.
- Certifique-se de que o arquivo `config.yml` está configurado corretamente para acessar o banco de dados.

---

## Conclusão

Este desafio é uma oportunidade para você praticar habilidades importantes, como:
- Conexão com bancos de dados em Python.
- Uso de Git e GitHub para colaboração.
- Implementação de funcionalidades em um projeto real.

Estamos ansiosos para ver sua contribuição! 🚀