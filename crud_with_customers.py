import streamlit as st
import psycopg2
import yaml
import random
import string

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

# Funções para interagir com o banco de dados - Categorias
def create_category(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    # Obter o próximo ID disponível
    cursor.execute("SELECT MAX(category_id) FROM categories")
    max_id = cursor.fetchone()[0]
    new_id = 1 if max_id is None else max_id + 1
    
    cursor.execute("INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s)", 
                  (new_id, name, description))
    conn.commit()
    conn.close()

def read_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category_id, category_name, description FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_category(category_id, name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET category_name = %s, description = %s WHERE category_id = %s", 
                  (name, description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    conn.commit()
    conn.close()

# Funções para interagir com o banco de dados - Clientes
def generate_customer_id():
    # Gera um ID de cliente de 5 letras maiúsculas aleatórias
    return ''.join(random.choices(string.ascii_uppercase, k=5))

def create_customer(company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Gerar um ID de cliente único
    while True:
        customer_id = generate_customer_id()
        cursor.execute("SELECT COUNT(*) FROM customers WHERE customer_id = %s", (customer_id,))
        if cursor.fetchone()[0] == 0:
            break
    
    cursor.execute("""
        INSERT INTO customers 
        (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax))
    
    conn.commit()
    conn.close()
    return customer_id

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
        SET company_name = %s, contact_name = %s, contact_title = %s, address = %s, 
            city = %s, region = %s, postal_code = %s, country = %s, phone = %s, fax = %s
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
st.title("Sistema de Gerenciamento")

# Seleção de entidade
entity = st.sidebar.radio("Selecione a entidade", ["Categorias", "Clientes"])

if entity == "Categorias":
    # Menu de navegação para Categorias
    menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    choice = st.sidebar.selectbox("Menu de Categorias", menu)

    # Criar categoria
    if choice == "Criar":
        st.subheader("Adicionar Nova Categoria")
        with st.form("create_category_form"):
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
        if categories:
            for category in categories:
                st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")
        else:
            st.info("Nenhuma categoria encontrada.")

    # Atualizar categoria
    elif choice == "Atualizar":
        st.subheader("Atualizar Categoria")
        categories = read_categories()
        if categories:
            category_ids = [category[0] for category in categories]
            selected_id = st.selectbox("Selecione o ID da Categoria", category_ids)
            selected_category = next((cat for cat in categories if cat[0] == selected_id), None)
            if selected_category:
                with st.form("update_category_form"):
                    new_name = st.text_input("Novo Nome", value=selected_category[1])
                    new_description = st.text_area("Nova Descrição", value=selected_category[2])
                    submitted = st.form_submit_button("Atualizar")
                    if submitted:
                        update_category(selected_id, new_name, new_description)
                        st.success(f"Categoria ID {selected_id} atualizada com sucesso!")
        else:
            st.info("Nenhuma categoria disponível para atualização.")

    # Deletar categoria
    elif choice == "Deletar":
        st.subheader("Deletar Categoria")
        categories = read_categories()
        if categories:
            category_ids = [category[0] for category in categories]
            selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
            if st.button("Deletar"):
                delete_category(selected_id)
                st.success(f"Categoria ID {selected_id} deletada com sucesso!")
        else:
            st.info("Nenhuma categoria disponível para exclusão.")

elif entity == "Clientes":
    # Menu de navegação para Clientes
    menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    choice = st.sidebar.selectbox("Menu de Clientes", menu)

    # Criar cliente
    if choice == "Criar":
        st.subheader("Adicionar Novo Cliente")
        with st.form("create_customer_form"):
            company_name = st.text_input("Nome da Empresa*", help="Campo obrigatório")
            contact_name = st.text_input("Nome do Contato")
            contact_title = st.text_input("Cargo do Contato")
            address = st.text_input("Endereço")
            city = st.text_input("Cidade")
            region = st.text_input("Região/Estado")
            postal_code = st.text_input("CEP/Código Postal")
            country = st.text_input("País")
            phone = st.text_input("Telefone")
            fax = st.text_input("Fax")
            
            submitted = st.form_submit_button("Adicionar Cliente")
            if submitted:
                if company_name:
                    customer_id = create_customer(company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
                    st.success(f"Cliente '{company_name}' adicionado com sucesso! ID: {customer_id}")
                else:
                    st.error("O nome da empresa é obrigatório.")

    # Ler clientes
    elif choice == "Ler":
        st.subheader("Lista de Clientes")
        customers = read_customers()
        if customers:
            # Criar uma tabela para exibir os clientes
            st.write("Total de clientes:", len(customers))
            
            # Opção para filtrar por país
            countries = sorted(list(set(c[8] for c in customers if c[8])))
            selected_country = st.selectbox("Filtrar por país", ["Todos"] + countries)
            
            filtered_customers = customers if selected_country == "Todos" else [c for c in customers if c[8] == selected_country]
            
            # Exibir clientes em formato de tabela
            if filtered_customers:
                for customer in filtered_customers:
                    with st.expander(f"{customer[0]} - {customer[1]}"):
                        st.write(f"**ID:** {customer[0]}")
                        st.write(f"**Empresa:** {customer[1]}")
                        st.write(f"**Contato:** {customer[2] or 'N/A'}")
                        st.write(f"**Cargo:** {customer[3] or 'N/A'}")
                        st.write(f"**Endereço:** {customer[4] or 'N/A'}")
                        st.write(f"**Cidade:** {customer[5] or 'N/A'}")
                        st.write(f"**Região:** {customer[6] or 'N/A'}")
                        st.write(f"**CEP:** {customer[7] or 'N/A'}")
                        st.write(f"**País:** {customer[8] or 'N/A'}")
                        st.write(f"**Telefone:** {customer[9] or 'N/A'}")
                        st.write(f"**Fax:** {customer[10] or 'N/A'}")
            else:
                st.info(f"Nenhum cliente encontrado para o país: {selected_country}")
        else:
            st.info("Nenhum cliente encontrado.")

    # Atualizar cliente
    elif choice == "Atualizar":
        st.subheader("Atualizar Cliente")
        customers = read_customers()
        if customers:
            customer_ids = [customer[0] for customer in customers]
            selected_id = st.selectbox("Selecione o ID do Cliente", customer_ids)
            selected_customer = next((cust for cust in customers if cust[0] == selected_id), None)
            
            if selected_customer:
                with st.form("update_customer_form"):
                    company_name = st.text_input("Nome da Empresa*", value=selected_customer[1])
                    contact_name = st.text_input("Nome do Contato", value=selected_customer[2] or "")
                    contact_title = st.text_input("Cargo do Contato", value=selected_customer[3] or "")
                    address = st.text_input("Endereço", value=selected_customer[4] or "")
                    city = st.text_input("Cidade", value=selected_customer[5] or "")
                    region = st.text_input("Região/Estado", value=selected_customer[6] or "")
                    postal_code = st.text_input("CEP/Código Postal", value=selected_customer[7] or "")
                    country = st.text_input("País", value=selected_customer[8] or "")
                    phone = st.text_input("Telefone", value=selected_customer[9] or "")
                    fax = st.text_input("Fax", value=selected_customer[10] or "")
                    
                    submitted = st.form_submit_button("Atualizar Cliente")
                    if submitted:
                        if company_name:
                            update_customer(selected_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
                            st.success(f"Cliente ID {selected_id} atualizado com sucesso!")
                        else:
                            st.error("O nome da empresa é obrigatório.")
        else:
            st.info("Nenhum cliente disponível para atualização.")

    # Deletar cliente
    elif choice == "Deletar":
        st.subheader("Deletar Cliente")
        customers = read_customers()
        if customers:
            customer_ids = [(customer[0], customer[1]) for customer in customers]
            selected_id = st.selectbox("Selecione o Cliente para Deletar", 
                                      options=[id[0] for id in customer_ids],
                                      format_func=lambda x: f"{x} - {next((name[1] for name in customer_ids if name[0] == x), '')}")
            
            if st.button("Deletar Cliente"):
                delete_customer(selected_id)
                st.success(f"Cliente ID {selected_id} deletado com sucesso!")
        else:
            st.info("Nenhum cliente disponível para exclusão.")