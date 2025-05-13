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

# Funções para interagir com o banco de dados (agora interagindo com a tabela 'customers')
def create_customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO customers (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax))
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
    cursor.execute("""
        UPDATE customers
        SET company_name = %s, contact_name = %s, contact_title = %s, address = %s, city = %s, region = %s, postal_code = %s, country = %s, phone = %s, fax = %s
        WHERE customer_id = %s
    """, (company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax, customer_id))
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
    st.subheader("Adicionar Novo Cliente")
    with st.form("create_form"):
        customer_id = st.text_input("ID do Cliente")
        company_name = st.text_input("Nome da Empresa")
        contact_name = st.text_input("Nome do Contato")
        contact_title = st.text_input("Título do Contato")
        address = st.text_area("Endereço")
        city = st.text_input("Cidade")
        region = st.text_input("Região")
        postal_code = st.text_input("Código Postal")
        country = st.text_input("País")
        phone = st.text_input("Telefone")
        fax = st.text_input("Fax")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_customer(customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
            st.success(f"Cliente '{company_name}' adicionado com sucesso!")

# Ler clientes
elif choice == "Ler":
    st.subheader("Lista de Clientes")
    customers = read_customers()
    for customer in customers:
        st.write(f"ID: {customer[0]} | Empresa: {customer[1]} | Contato: {customer[2]} | Título: {customer[3]}")

# Atualizar cliente
elif choice == "Atualizar":
    st.subheader("Atualizar Cliente")
    customers = read_customers()
    customer_ids = [customer[0] for customer in customers]
    selected_id = st.selectbox("Selecione o ID do Cliente", customer_ids)
    selected_customer = next((cust for cust in customers if cust[0] == selected_id), None)
    if selected_customer:
        with st.form("update_form"):
            new_company_name = st.text_input("Novo Nome da Empresa", value=selected_customer[1])
            new_contact_name = st.text_input("Novo Nome do Contato", value=selected_customer[2])
            new_contact_title = st.text_input("Novo Título do Contato", value=selected_customer[3])
            new_address = st.text_area("Novo Endereço", value=selected_customer[4])
            new_city = st.text_input("Nova Cidade", value=selected_customer[5])
            new_region = st.text_input("Nova Região", value=selected_customer[6])
            new_postal_code = st.text_input("Novo Código Postal", value=selected_customer[7])
            new_country = st.text_input("Novo País", value=selected_customer[8])
            new_phone = st.text_input("Novo Telefone", value=selected_customer[9])
            new_fax = st.text_input("Novo Fax", value=selected_customer[10])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_customer(selected_id, new_company_name, new_contact_name, new_contact_title, new_address, new_city, new_region, new_postal_code, new_country, new_phone, new_fax)
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