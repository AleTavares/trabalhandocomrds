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

# Funções CRUD para Categories
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

# Funções CRUD para Shippers
def create_shipper(company_name, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shippers (company_name, phone) VALUES (%s, %s)", (company_name, phone))
    conn.commit()
    conn.close()

def read_shippers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shippers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_shipper(shipper_id, company_name, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE shippers SET company_name = %s, phone = %s WHERE shipper_id = %s", (company_name, phone, shipper_id))
    conn.commit()
    conn.close()

def delete_shipper(shipper_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shippers WHERE shipper_id = %s", (shipper_id,))
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Sistema de Gerenciamento")

main_menu = ["Categorias", "Shippers"]
main_choice = st.sidebar.selectbox("Selecione a Tabela", main_menu)

if main_choice == "Categorias":
    st.header("Gerenciamento de Categorias")
    menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    choice = st.sidebar.selectbox("Ação", menu)

    if choice == "Criar":
        st.subheader("Adicionar Nova Categoria")
        with st.form("create_form"):
            name = st.text_input("Nome da Categoria")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_category(name, description)
                st.success(f"Categoria '{name}' adicionada com sucesso!")

    elif choice == "Ler":
        st.subheader("Lista de Categorias")
        categories = read_categories()
        for category in categories:
            st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")

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

    elif choice == "Deletar":
        st.subheader("Deletar Categoria")
        categories = read_categories()
        category_ids = [category[0] for category in categories]
        selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
        if st.button("Deletar"):
            delete_category(selected_id)
            st.success(f"Categoria ID {selected_id} deletada com sucesso!")

elif main_choice == "Shippers":
    st.header("Gerenciamento de Shippers")
    menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    choice = st.sidebar.selectbox("Ação", menu)

    if choice == "Criar":
        st.subheader("Adicionar Novo Shipper")
        with st.form("create_shipper_form"):
            company_name = st.text_input("Nome da Empresa")
            phone = st.text_input("Telefone")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_shipper(company_name, phone)
                st.success(f"Shipper '{company_name}' adicionado com sucesso!")

    elif choice == "Ler":
        st.subheader("Lista de Shippers")
        shippers = read_shippers()
        for shipper in shippers:
            st.write(f"ID: {shipper[0]} | Empresa: {shipper[1]} | Telefone: {shipper[2]}")

    elif choice == "Atualizar":
        st.subheader("Atualizar Shipper")
        shippers = read_shippers()
        shipper_ids = [shipper[0] for shipper in shippers]
        selected_id = st.selectbox("Selecione o ID do Shipper", shipper_ids)
        selected_shipper = next((s for s in shippers if s[0] == selected_id), None)
        if selected_shipper:
            with st.form("update_shipper_form"):
                new_name = st.text_input("Novo Nome da Empresa", value=selected_shipper[1])
                new_phone = st.text_input("Novo Telefone", value=selected_shipper[2])
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    update_shipper(selected_id, new_name, new_phone)
                    st.success(f"Shipper ID {selected_id} atualizado com sucesso!")

    elif choice == "Deletar":
        st.subheader("Deletar Shipper")
        shippers = read_shippers()
        shipper_ids = [shipper[0] for shipper in shippers]
        selected_id = st.selectbox("Selecione o ID do Shipper para Deletar", shipper_ids)
        if st.button("Deletar"):
            delete_shipper(selected_id)
            st.success(f"Shipper ID {selected_id} deletado com sucesso!")
