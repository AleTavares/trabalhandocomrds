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
st.title("Gerenciamento de Categorias")

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
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")