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

# Funções para interagir com o banco de dados (Tabela Categories)
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
    cursor.execute("UPDATE categories SET name = %s, description = %s WHERE id = %s", (name, description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()

# Funções CRUD para a tabela customers
def create_customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO customers (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
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

def update_customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE customers SET company_name = %s, contact_name = %s, contact_title = %s, address = %s, city = %s, 
           region = %s, postal_code = %s, country = %s, phone = %s, fax = %s WHERE customer_id = %s""",
        (company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax, customer_id)
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
st.title("Gerenciamento de Dados")

# Menu de navegação
menu = ["Criar Categoria", "Ler Categorias", "Atualizar Categoria", "Deletar Categoria",
        "Criar Cliente", "Ler Clientes", "Atualizar Cliente", "Deletar Cliente"]
choice = st.sidebar.selectbox("Menu", menu, key="menu_selectbox")

# Criar categoria
if choice == "Criar Categoria":
    st.subheader("Adicionar Nova Categoria")
    with st.form("create_form"):
        name = st.text_input("Nome da Categoria")
        description = st.text_area("Descrição")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_category(name, description)
            st.success(f"Categoria '{name}' adicionada com sucesso!")

# Ler categorias
elif choice == "Ler Categorias":
    st.subheader("Lista de Categorias")
    categories = read_categories()
    for category in categories:
        st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")

# Atualizar categoria
elif choice == "Atualizar Categoria":
    st.subheader("Atualizar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria", category_ids, key="update_category_selectbox")
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
elif choice == "Deletar Categoria":
    st.subheader("Deletar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids, key="delete_category_selectbox")
    if st.button("Deletar"):
        delete_category(selected_id)
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")

# Criar um novo cliente
elif choice == "Criar Cliente":
    st.subheader("Adicionar Novo Cliente")
    with st.form("create_customer_form"):
        customer_id = st.text_input("Customer ID")
        company_name = st.text_input("Company Name")
        contact_name = st.text_input("Contact Name")
        contact_title = st.text_input("Contact Title")
        address = st.text_input("Address")
        city = st.text_input("City")
        region = st.text_input("Region")
        postal_code = st.text_input("Postal Code")
        country = st.text_input("Country")
        phone = st.text_input("Phone")
        fax = st.text_input("Fax")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
            st.success(f"Cliente '{customer_id}' adicionado com sucesso!")

# Ler clientes
elif choice == "Ler Clientes":
    st.subheader("Lista de Clientes")
    customers = read_customers()
    for customer in customers:
        st.write(f"ID: {customer[0]} | Empresa: {customer[1]} | Contato: {customer[2]} | Cidade: {customer[5]}")

# Atualizar cliente
elif choice == "Atualizar Cliente":
    st.subheader("Atualizar Cliente")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o Customer ID", customer_ids, key="update_customer_selectbox")
    selected_customer = next((cust for cust in customers if cust[0] == selected_id), None)
    if selected_customer:
        with st.form("update_customer_form"):
            company_name = st.text_input("Company Name", value=selected_customer[1])
            contact_name = st.text_input("Contact Name", value=selected_customer[2])
            contact_title = st.text_input("Contact Title", value=selected_customer[3])
            address = st.text_input("Address", value=selected_customer[4])
            city = st.text_input("City", value=selected_customer[5])
            region = st.text_input("Region", value=selected_customer[6])
            postal_code = st.text_input("Postal Code", value=selected_customer[7])
            country = st.text_input("Country", value=selected_customer[8])
            phone = st.text_input("Phone", value=selected_customer[9])
            fax = st.text_input("Fax", value=selected_customer[10])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_customer(selected_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
                st.success(f"Cliente '{selected_id}' atualizado com sucesso!")

# Deletar cliente
elif choice == "Deletar Cliente":
    st.subheader("Deletar Cliente")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o Customer ID para Deletar", customer_ids, key="delete_customer_selectbox")
    if st.button("Deletar"):
        delete_customer(selected_id)
        st.success(f"Cliente '{selected_id}' deletado com sucesso!")