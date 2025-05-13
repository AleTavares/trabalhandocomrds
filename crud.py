import streamlit as st
import psycopg2
import yaml

# Função para carregar as credenciais do arquivo YAML
def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

# Função para conectar ao banco de dados RDS
def get_connection():
    try:
        config = load_config()
        db = config["database"]
        conn = psycopg2.connect(
            host=db["host"],
            port=db["port"],
            user=db["user"],
            password=db["password"],
            dbname=db["dbname"]
        )
        return conn
    except psycopg2.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        raise
    except Exception as e:
        st.error(f"Erro ao carregar configurações: {str(e)}")
        raise

# Funções para interagir com o banco de dados
def create_category(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    # Get the next available category_id
    cursor.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM categories")
    next_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            "INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s)", 
            (next_id, name, description)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao criar categoria: {str(e)}")
        conn.rollback()
        return False
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
    cursor.execute("UPDATE categories SET name = %s, description = %s WHERE id = %s", (name, description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()

# Funções para gerenciar transportadoras (shippers)
def create_shipper(company_name, phone):
    if not company_name.strip():
        st.error("O nome da empresa não pode estar vazio")
        return False
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shippers (company_name, phone) VALUES (%s, %s) RETURNING shipper_id",
                (company_name, phone)
            )
            shipper_id = cursor.fetchone()[0]
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Erro ao criar transportadora: {str(e)}")
        return False

def read_shippers():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT shipper_id, company_name, phone FROM shippers")
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Erro ao ler transportadoras: {str(e)}")
        return []

def update_shipper(shipper_id, company_name, phone):
    if not company_name.strip():
        st.error("O nome da empresa não pode estar vazio")
        return False
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE shippers SET company_name = %s, phone = %s WHERE shipper_id = %s",
                (company_name, phone, shipper_id)
            )
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Erro ao atualizar transportadora: {str(e)}")
        return False

def delete_shipper(shipper_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM shippers WHERE shipper_id = %s", (shipper_id,))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Erro ao deletar transportadora: {str(e)}")
        return False

# Interface do Streamlit
st.title("Gerenciamento de Categorias e Transportadoras")

# Menu de navegação
menu = ["Categorias - Criar", "Categorias - Ler", "Categorias - Atualizar", "Categorias - Deletar",
        "Transportadoras - Criar", "Transportadoras - Ler", "Transportadoras - Atualizar", "Transportadoras - Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar categoria
if choice == "Categorias - Criar":
    st.subheader("Adicionar Nova Categoria")
    with st.form("create_form"):
        name = st.text_input("Nome da Categoria")
        description = st.text_area("Descrição")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_category(name, description)
            st.success(f"Categoria '{name}' adicionada com sucesso!")

# Ler categorias
elif choice == "Categorias - Ler":
    st.subheader("Lista de Categorias")
    categories = read_categories()
    for category in categories:
        st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")

# Atualizar categoria
elif choice == "Categorias - Atualizar":
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
elif choice == "Categorias - Deletar":
    st.subheader("Deletar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
    if st.button("Deletar"):
        delete_category(selected_id)
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")

# Interface para Transportadoras
if choice == "Transportadoras - Criar":
    st.subheader("Adicionar Nova Transportadora")
    with st.form("create_shipper_form"):
        company_name = st.text_input("Nome da Empresa")
        phone = st.text_input("Telefone")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            if create_shipper(company_name, phone):
                st.success(f"Transportadora '{company_name}' adicionada com sucesso!")

elif choice == "Transportadoras - Ler":
    st.subheader("Lista de Transportadoras")
    shippers = read_shippers()
    for shipper in shippers:
        st.write(f"ID: {shipper[0]} | Empresa: {shipper[1]} | Telefone: {shipper[2]}")

elif choice == "Transportadoras - Atualizar":
    st.subheader("Atualizar Transportadora")
    shippers = read_shippers()
    shipper_ids = [shipper[0] for shipper in shippers]
    selected_id = st.selectbox("Selecione o ID da Transportadora", shipper_ids)
    selected_shipper = next((ship for ship in shippers if ship[0] == selected_id), None)
    
    if selected_shipper:
        with st.form("update_shipper_form"):
            new_name = st.text_input("Novo Nome da Empresa", value=selected_shipper[1])
            new_phone = st.text_input("Novo Telefone", value=selected_shipper[2])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                if update_shipper(selected_id, new_name, new_phone):
                    st.success(f"Transportadora ID {selected_id} atualizada com sucesso!")

elif choice == "Transportadoras - Deletar":
    st.subheader("Deletar Transportadora")
    shippers = read_shippers()
    shipper_ids = [shipper[0] for shipper in shippers]
    selected_id = st.selectbox("Selecione o ID da Transportadora para Deletar", shipper_ids)
    if st.button("Deletar"):
        if delete_shipper(selected_id):
            st.success(f"Transportadora ID {selected_id} deletada com sucesso!")