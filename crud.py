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
        dbname=db["dbname"]
    )

# Funções para interagir com o banco de dados
def create_category(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
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
        "UPDATE categories SET category_name = %s, description = %s WHERE category_id = %s",
        (name, description, category_id)
    )
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM categories WHERE category_id = %s",
        (category_id,)
    )
    conn.commit()
    conn.close()

def create_customer(customer_id, name, contact_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (customer_id, name, contact_name) VALUES (%s, %s, %s)",
        (customer_id, name, contact_name),
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

def update_customer(customer_id, name, contact_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name = %s, contact_name = %s WHERE customer_id = %s",
        (name, contact_name, customer_id),
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
st.title("Gerenciamento de Categorias")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar", "Gerenciar Customers"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar categoria
if choice == "Criar":
    st.subheader("Adicionar Nova Categoria")
    with st.form("create_form"):
        name = st.text_input("Nome da Categoria")
        description = st.text_area("Descrição")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_category(name, description)
            st.success(f"Categoria '{name}' adicionada com sucesso!")

# Ler categorias
elif choice == "Ler":
    st.subheader("Lista de Categorias")
    categories = read_categories()
    for category in categories:
        st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")

# Atualizar categoria
elif choice == "Atualizar":
    st.subheader("Atualizar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria", category_ids)
    selected_category = next((cat for cat in categories if cat[0] == selected_id), None)
    if selected_category:
        with st.form("update_form"):
            new_name = st.text_input("Novo Nome", value=selected_category[1])
            new_description = st.text_area("Nova Descrição", value=selected_category[2])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_category(selected_id, new_name, new_description)
                st.success(f"Categoria ID {selected_id} atualizada com sucesso!")

# Deletar categoria
elif choice == "Deletar":
    st.subheader("Deletar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
    if st.button("Deletar"):
        delete_category(selected_id)
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")

# Interface do Streamlit para a tabela customers
elif choice == "Gerenciar Customers":
    st.subheader("Gerenciar Customers")

    # Submenu
    submenu = st.sidebar.selectbox("Ação", ["Criar", "Ler", "Atualizar", "Deletar"])

    if submenu == "Criar":
        with st.form("create_customer_form"):
            customer_id = st.text_input("ID do Cliente")
            name = st.text_input("Nome")
            contact_name = st.text_input("Nome do Contato")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_customer(customer_id, name, contact_name)
                st.success(f"Cliente '{name}' adicionado com sucesso!")

    elif submenu == "Ler":
        customers = read_customers()
        for customer in customers:
            st.write(f"ID: {customer[0]} | Nome: {customer[1]} | Contato: {customer[2]}")

    elif submenu == "Atualizar":
        customers = read_customers()
        customer_ids = [customer[0] for customer in customers]
        selected_id = st.selectbox("Selecione o ID do Cliente", customer_ids)
        selected_customer = next((c for c in customers if c[0] == selected_id), None)
        if selected_customer:
            with st.form("update_customer_form"):
                new_name = st.text_input("Novo Nome", value=selected_customer[1])
                new_contact_name = st.text_input("Novo Nome do Contato", value=selected_customer[2])
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    update_customer(selected_id, new_name, new_contact_name)
                    st.success(f"Cliente ID {selected_id} atualizado com sucesso!")

    elif submenu == "Deletar":
        customers = read_customers()
        customer_ids = [customer[0] for customer in customers]
        selected_id = st.selectbox("Selecione o ID do Cliente para Deletar", customer_ids)
        if st.button("Deletar"):
            delete_customer(selected_id)
            st.success(f"Cliente ID {selected_id} deletado com sucesso!")