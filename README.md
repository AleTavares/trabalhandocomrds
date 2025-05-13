# Gerenciamento de Clientes com Streamlit e PostgreSQL

Este é um aplicativo web simples de gerenciamento de clientes, desenvolvido com **Streamlit** e conectado a um banco de dados **PostgreSQL** (como Amazon RDS ou qualquer outro servidor PostgreSQL). O aplicativo permite criar, ler, atualizar e deletar informações sobre clientes a partir de uma tabela chamada `customers`.

## Funcionalidades

- **Criar Cliente**: Adiciona um novo cliente ao banco de dados.
- **Ler Clientes**: Exibe uma lista de todos os clientes cadastrados.
- **Atualizar Cliente**: Permite atualizar as informações de um cliente específico.
- **Deletar Cliente**: Deleta um cliente pelo seu ID.

## Estrutura da Tabela `customers`

A tabela `customers` possui a seguinte estrutura no banco de dados:

```sql
CREATE TABLE customers (
    customer_id character varying(5) NOT NULL,
    company_name character varying(40) NOT NULL,
    contact_name character varying(30),
    contact_title character varying(30),
    address character varying(60),
    city character varying(15),
    region character varying(15),
    postal_code character varying(10),
    country character varying(15),
    phone character varying(24),
    fax character varying(24)
);

Pré-requisitos
Antes de executar o aplicativo, certifique-se de que você tenha os seguintes pré-requisitos instalados:

Python 3.x: A versão do Python necessária para rodar o código.

Bibliotecas:

streamlit: Para construir a interface web.

psycopg2: Para conectar ao banco de dados PostgreSQL.

pyyaml: Para carregar as credenciais do banco de dados a partir de um arquivo YAML.

Instale as bibliotecas necessárias com o seguinte comando:

pip install streamlit psycopg2 pyyaml

