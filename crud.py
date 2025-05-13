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
    cursor.execute("UPDATE categories SET name = %s, description = %s WHERE id = %s", (name, description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()

# Interface do Streamlit
'''st.title("Gerenciamento de Categorias")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
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
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")'''



def create_customer(name, title, address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, title, address, city, region, postal_code, country, phone, fax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                   (name, title, address, city, region, postal_code, country, phone, fax))
    conn.commit()
    conn.close()

def read_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_customer(customer_id, name, title, address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = %s, title = %s, address = %s, city = %s, region = %s, postal_code = %s, country = %s, phone = %s, fax = %s WHERE id = %s", 
                   (name, title, address, city, region, postal_code, country, phone, fax, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
    conn.commit()
    conn.close()


st.title("Gerenciamento de Clientes")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar clientes
if choice == "Criar":
    st.subheader("Adicionar Novo Cliente")
    with st.form("create_form"):
        name = st.text_input("Nome do Cliente")
        title = st.text_area("Título")
        address = st.text_area("Endereço")
        city = st.text_input("Cidade")
        region = st.text_input("Região")
        postal_code = st.text_input("Código Postal")
        country = st.text_input("País")
        phone = st.text_input("Telefone")
        fax = st.text_input("Fax")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_customer(name, title, address, city, region, postal_code, country, phone, fax)
            st.success(f"Cliente '{name}' adicionado com sucesso!")

# Ler clientes
elif choice == "Ler":
    st.subheader("Lista de Clientes")
    customers = read_customers()
    for customer in customers:
        st.write(f"ID: {customer[0]} | Nome: {customer[1]} | Descrição: {customer[2]}")

# Atualizar clientes
elif choice == "Atualizar":
    st.subheader("Atualizar Clientes")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o ID do Cliente", customer_ids)
    selected_customer = next((cat for cat in customers if cat[0] == selected_id), None)
    if selected_customer:
        with st.form("update_form"):
            new_name = st.text_input("Novo Nome", value=selected_customer[1])
            new_title = st.text_area("Novo Título", value=selected_customer[2])
            new_address = st.text_area("Novo Endereço", value=selected_customer[3])
            new_city = st.text_input("Nova Cidade", value=selected_customer[4])
            new_region = st.text_input("Nova Região", value=selected_customer[5])
            new_postal_code = st.text_input("Novo Código Postal", value=selected_customer[6])
            new_country = st.text_input("Novo País", value=selected_customer[7])
            new_phone = st.text_input("Novo Telefone", value=selected_customer[8])
            new_fax = st.text_input("Novo Fax", value=selected_customer[9])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_customer(selected_id, new_name, new_title, new_address, new_city, new_region, new_postal_code, new_country, new_phone, new_fax)
                st.success(f"Cliente ID {selected_id} atualizado com sucesso!")

# Deletar cliente
elif choice == "Deletar":
    st.subheader("Deletar Cliente")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o ID do Cliente para Deletar", customer_ids)
    if st.button("Deletar"):
        delete_customer(selected_id)
        st.success(f"Cliente ID {selected_id} deletado com sucesso!")