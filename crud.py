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
    try:
        # Obter o próximo ID disponível
        cursor.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM categories")
        next_id = cursor.fetchone()[0]
        
        # Inserir categoria com ID explícito
        cursor.execute(
            "INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s) RETURNING category_id",
            (next_id, name, description)
        )
        category_id = cursor.fetchone()[0]  # Captura o ID gerado
        conn.commit()
        return category_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Funções CRUD para a tabela customers
def create_customer(company_name, contact_name, contact_title=None, address=None, city=None, region=None, postal_code=None, country=None, phone=None, fax=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Gerar um ID de cliente único de 5 caracteres
        cursor.execute("SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1")
        last_id = cursor.fetchone()
        
        if last_id:
            # Extrair a parte numérica e incrementar
            prefix = ''.join(c for c in last_id[0] if not c.isdigit())
            num = ''.join(c for c in last_id[0] if c.isdigit())
            
            if num:
                next_num = int(num) + 1
                customer_id = f"{prefix}{next_num:03d}"
            else:
                customer_id = f"{prefix}001"
        else:
            # Se não houver clientes, começar com CUST1
            customer_id = "CUST1"
        
        cursor.execute(
            "INSERT INTO customers (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING customer_id",
            (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
        )
        customer_id = cursor.fetchone()[0]
        conn.commit()
        return customer_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def read_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def update_customer(customer_id, company_name=None, contact_name=None, contact_title=None, address=None, city=None, region=None, postal_code=None, country=None, phone=None, fax=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Primeiro, obter os dados atuais do cliente
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        current_data = cursor.fetchone()
        
        if not current_data:
            raise Exception(f"Cliente com ID {customer_id} não encontrado")
        
        # Atualizar apenas os campos que foram fornecidos
        update_data = {
            'company_name': company_name if company_name is not None else current_data[1],
            'contact_name': contact_name if contact_name is not None else current_data[2],
            'contact_title': contact_title if contact_title is not None else current_data[3],
            'address': address if address is not None else current_data[4],
            'city': city if city is not None else current_data[5],
            'region': region if region is not None else current_data[6],
            'postal_code': postal_code if postal_code is not None else current_data[7],
            'country': country if country is not None else current_data[8],
            'phone': phone if phone is not None else current_data[9],
            'fax': fax if fax is not None else current_data[10]
        }
        
        cursor.execute(
            "UPDATE customers SET company_name = %s, contact_name = %s, contact_title = %s, address = %s, city = %s, region = %s, postal_code = %s, country = %s, phone = %s, fax = %s WHERE customer_id = %s",
            (update_data['company_name'], update_data['contact_name'], update_data['contact_title'], update_data['address'], update_data['city'], update_data['region'], update_data['postal_code'], update_data['country'], update_data['phone'], update_data['fax'], customer_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
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
    cursor.execute("UPDATE categories SET category_name = %s, description = %s WHERE category_id = %s", (name, description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Dados")

# Menu de navegação principal
entidade = st.sidebar.selectbox("Selecione a entidade", ["Categorias", "Clientes"])

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Interface principal baseada na entidade selecionada
if entidade == "Categorias":
    # Criar categoria
    if choice == "Criar":
        st.subheader("Adicionar Nova Categoria")
        with st.form("create_category_form"):
            name = st.text_input("Nome da Categoria")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                category_id = create_category(name, description)
                st.success(f"Categoria '{name}' adicionada com sucesso! ID da Categoria: {category_id}")

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
            with st.form("update_category_form"):
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

elif entidade == "Clientes":
    # Criar cliente
    if choice == "Criar":
        st.subheader("Adicionar Novo Cliente")
        with st.form("create_customer_form"):
            company_name = st.text_input("Nome da Empresa")
            contact_name = st.text_input("Nome do Contato")
            contact_title = st.text_input("Cargo do Contato")
            address = st.text_input("Endereço")
            city = st.text_input("Cidade")
            region = st.text_input("Região")
            postal_code = st.text_input("CEP")
            country = st.text_input("País")
            phone = st.text_input("Telefone")
            fax = st.text_input("Fax")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                try:
                    customer_id = create_customer(company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
                    st.success(f"Cliente '{company_name}' adicionado com sucesso! ID do Cliente: {customer_id}")
                except Exception as e:
                    st.error(f"Erro ao adicionar cliente: {str(e)}")

    # Ler clientes
    elif choice == "Ler":
        st.subheader("Lista de Clientes")
        customers = read_customers()
        for customer in customers:
            st.write(f"ID: {customer[0]} | Empresa: {customer[1]} | Contato: {customer[2]} | País: {customer[8]}")
            if st.button(f"Detalhes de {customer[0]}", key=f"details_{customer[0]}"):
                st.write(f"Cargo: {customer[3]}")
                st.write(f"Endereço: {customer[4]}")
                st.write(f"Cidade: {customer[5]}, Região: {customer[6]}, CEP: {customer[7]}")
                st.write(f"Telefone: {customer[9]}, Fax: {customer[10]}")

    # Atualizar cliente
    elif choice == "Atualizar":
        st.subheader("Atualizar Cliente")
        customers = read_customers()
        customer_ids = [customer[0] for customer in customers]
        selected_id = st.selectbox("Selecione o ID do Cliente", customer_ids)
        selected_customer = read_customer_by_id(selected_id)
        
        if selected_customer:
            with st.form("update_customer_form"):
                company_name = st.text_input("Nome da Empresa", value=selected_customer[1])
                contact_name = st.text_input("Nome do Contato", value=selected_customer[2])
                contact_title = st.text_input("Cargo do Contato", value=selected_customer[3] if selected_customer[3] else "")
                address = st.text_input("Endereço", value=selected_customer[4] if selected_customer[4] else "")
                city = st.text_input("Cidade", value=selected_customer[5] if selected_customer[5] else "")
                region = st.text_input("Região", value=selected_customer[6] if selected_customer[6] else "")
                postal_code = st.text_input("CEP", value=selected_customer[7] if selected_customer[7] else "")
                country = st.text_input("País", value=selected_customer[8] if selected_customer[8] else "")
                phone = st.text_input("Telefone", value=selected_customer[9] if selected_customer[9] else "")
                fax = st.text_input("Fax", value=selected_customer[10] if selected_customer[10] else "")
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    try:
                        update_customer(selected_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
                        st.success(f"Cliente ID {selected_id} atualizado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao atualizar cliente: {str(e)}")

    # Deletar cliente
    elif choice == "Deletar":
        st.subheader("Deletar Cliente")
        customers = read_customers()
        customer_ids = [customer[0] for customer in customers]
        selected_id = st.selectbox("Selecione o ID do Cliente para Deletar", customer_ids)
        selected_customer = read_customer_by_id(selected_id)
        
        if selected_customer:
            st.write(f"Empresa: {selected_customer[1]}")
            st.write(f"Contato: {selected_customer[2]}")
            st.write(f"País: {selected_customer[8]}")
            
            if st.button("Confirmar Exclusão"):
                try:
                    delete_customer(selected_id)
                    st.success(f"Cliente ID {selected_id} deletado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao deletar cliente: {str(e)}")