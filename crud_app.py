import streamlit as st
import psycopg2
import yaml
import pandas as pd

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

# --- CRUD de Categories ---
def create_category(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (name, description) VALUES (%s, %s)",
        (name, description)
    )
    conn.commit()
    conn.close()


def read_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM categories ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_category(category_id, name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categories SET name = %s, description = %s WHERE id = %s",
        (name, description, category_id)
    )
    conn.commit()
    conn.close()


def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM categories WHERE id = %s",
        (category_id,)
    )
    conn.commit()
    conn.close()

# --- CRUD de Customers ---
def create_customer(customer_id, company_name, contact_name, contact_title,
                    address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO customers (
            customer_id, company_name, contact_name, contact_title,
            address, city, region, postal_code, country, phone, fax
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        (customer_id, company_name, contact_name, contact_title,
         address, city, region, postal_code, country, phone, fax)
    )
    conn.commit()
    conn.close()


def read_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT customer_id, company_name, contact_name, contact_title,"
        " address, city, region, postal_code, country, phone, fax"
        " FROM customers ORDER BY customer_id"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_customer(customer_id, company_name, contact_name, contact_title,
                    address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE customers SET
            company_name = %s,
            contact_name = %s,
            contact_title = %s,
            address = %s,
            city = %s,
            region = %s,
            postal_code = %s,
            country = %s,
            phone = %s,
            fax = %s
           WHERE customer_id = %s''',
        (company_name, contact_name, contact_title,
         address, city, region, postal_code, country, phone, fax,
         customer_id)
    )
    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM customers WHERE customer_id = %s",
        (customer_id,)
    )
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Dados e Clientes")

# Seleciona entidade e operação
entity = st.sidebar.selectbox("Entidade", ["Categorias", "Customers"])
action = st.sidebar.selectbox("Ação", ["Criar", "Ler", "Atualizar", "Deletar"])

# Lógica de CRUD para Categories
if entity == "Categorias":
    if action == "Criar":
        st.subheader("Adicionar Nova Categoria")
        with st.form("create_category_form"):
            name = st.text_input("Nome da Categoria")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_category(name, description)
                st.success(f"Categoria '{name}' adicionada com sucesso!")

    elif action == "Ler":
        st.subheader("Lista de Categorias")
        categories = read_categories()
        if categories:
            df = pd.DataFrame(categories, columns=["ID", "Nome", "Descrição"]);
            st.dataframe(df)
        else:
            st.info("Nenhuma categoria encontrada.")

    elif action == "Atualizar":
        st.subheader("Atualizar Categoria")
        categories = read_categories()
        category_ids = [cat[0] for cat in categories]
        selected_id = st.selectbox("Selecione o ID da Categoria", category_ids)
        selected = next((c for c in categories if c[0] == selected_id), None)
        if selected:
            with st.form("update_category_form"):
                new_name = st.text_input("Novo Nome", value=selected[1])
                new_description = st.text_area("Nova Descrição", value=selected[2])
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    update_category(selected_id, new_name, new_description)
                    st.success(f"Categoria ID {selected_id} atualizada com sucesso!")

    elif action == "Deletar":
        st.subheader("Deletar Categoria")
        categories = read_categories()
        category_ids = [cat[0] for cat in categories]
        selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
        if st.button("Deletar Categoria"):
            delete_category(selected_id)
            st.success(f"Categoria ID {selected_id} deletada com sucesso!")

# Lógica de CRUD para Customers
elif entity == "Customers":
    if action == "Criar":
        st.subheader("Adicionar Novo Customer")
        with st.form("create_customer_form"):
            cid = st.text_input("Customer ID (5 chars)")
            company = st.text_input("Company Name")
            contact = st.text_input("Contact Name")
            title = st.text_input("Contact Title")
            address = st.text_input("Address")
            city = st.text_input("City")
            region = st.text_input("Region")
            postal = st.text_input("Postal Code")
            country = st.text_input("Country")
            phone = st.text_input("Phone")
            fax = st.text_input("Fax")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_customer(cid, company, contact, title, address,
                                city, region, postal, country, phone, fax)
                st.success("Customer inserido com sucesso!")

    elif action == "Ler":
        st.subheader("Lista de Customers")
        customers = read_customers()
        if customers:
            df = pd.DataFrame(
                customers,
                columns=[
                    "Customer ID", "Company Name", "Contact Name", "Contact Title",
                    "Address", "City", "Region", "Postal Code", "Country", "Phone", "Fax"
                ]
            )
            st.dataframe(df)
        else:
            st.info("Nenhum customer encontrado.")

    elif action == "Atualizar":
        st.subheader("Atualizar Customer")
        customers = read_customers()
        customer_ids = [c[0] for c in customers]
        selected_id = st.selectbox("Selecione o Customer ID", customer_ids)
        selected = next((c for c in customers if c[0] == selected_id), None)
        if selected:
            with st.form("update_customer_form"):
                new_company = st.text_input("Company Name", value=selected[1])
                new_contact = st.text_input("Contact Name", value=selected[2])
                new_title = st.text_input("Contact Title", value=selected[3])
                new_address = st.text_input("Address", value=selected[4])
                new_city = st.text_input("City", value=selected[5])
                new_region = st.text_input("Region", value=selected[6])
                new_postal = st.text_input("Postal Code", value=selected[7])
                new_country = st.text_input("Country", value=selected[8])
                new_phone = st.text_input("Phone", value=selected[9])
                new_fax = st.text_input("Fax", value=selected[10])
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    update_customer(selected_id, new_company, new_contact,
                                    new_title, new_address, new_city,
                                    new_region, new_postal, new_country,
                                    new_phone, new_fax)
                    st.success(f"Customer ID {selected_id} atualizado com sucesso!")

    elif action == "Deletar":
        st.subheader("Deletar Customer")
        customers = read_customers()
        customer_ids = [c[0] for c in customers]
        selected_id = st.selectbox("Selecione o Customer ID para Deletar", customer_ids)
        if st.button("Deletar Customer"):
            delete_customer(selected_id)
            st.success(f"Customer ID {selected_id} deletado com sucesso!")
