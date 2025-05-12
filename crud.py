import streamlit as st
import psycopg2
import yaml


# Função para carregar as credenciais do arquivo YAML
def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)


# Função para conectar ao banco de dados RDS
def get_connection():
    config = load_config()
    db = config["database"]
    return psycopg2.connect(
        host=db["host"],
        port=db["port"],
        user=db["user"],
        password=db["password"],
        dbname=db["dbname"],
    )


# Funções para interagir com o banco de dados
def create_category(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (name, description) VALUES (%s, %s)",
        (name, description),
    )
    conn.commit()
    conn.close()


def read_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_category(category_id, name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categories SET name = %s, description = %s WHERE id = %s",
        (name, description, category_id),
    )
    conn.commit()
    conn.close()


def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()


# funç~oes para interação da tabela customers
def create_customer(customer_id, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (customer_id, fax) VALUES (%s, %s)", (customer_id, fax)
    )
    conn.commit()
    conn.close()


def read_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_customer(customer_id, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET fax = %s WHERE customer_id = %s", (fax, customer_id)
    )
    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    conn.close()


# Interface do Streamlit
st.title("Gerenciamento de Clientes")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar cliente
if choice == "Criar":
    st.subheader("Adicionar novo cliente")
    with st.form("create_form"):
        customer_id = st.text_input("Cliente ID")
        fax = st.text_input("Fax")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_customer(customer_id, fax)
            st.success(f"Cliente '{customer_id}' adicionado com sucesso!")

# Ler clientes
elif choice == "Ler":
    st.subheader("Lista de clientes")
    customers = read_customers()
    for customer in customers:
        st.write(f"ID: {customer[0]} | Fax: {customer[1]}")

# Atualizar cliente
elif choice == "Atualizar":
    st.subheader("Atualizar cliente")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o ID do cliente", customer_ids)
    selected_customer = next((c for c in customers if c[0] == selected_id), None)
    if selected_customer:
        with st.form("update_form"):
            new_fax = st.text_input("Novo Fax", value=selected_customer[1])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_customer(selected_id, new_fax)
                st.success(f"Cliente ID {selected_id} atualizado com sucesso!")

# Deletar cliente
elif choice == "Deletar":
    st.subheader("Deletar Customer")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o ID do cliente para deletar", customer_ids)
    if st.button("Deletar"):
        delete_customer(selected_id)
        st.success(f"Cliente ID {selected_id} deletado com sucesso!")
