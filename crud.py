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
    cursor.execute("INSERT INTO categories (category_name, description) VALUES (%s, %s)", (name, description))
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
    cursor.execute("UPDATE categories SET category_name = %s, description = %s WHERE category_id = %s", (name, description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    conn.commit()
    conn.close()
    
# Tabela Region
def create_region(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO region (region_description) VALUES (%s)", (name))
    conn.commit()
    conn.close()

def read_regions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM region")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_region(region_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE region SET region_description = %s WHERE region_id = %s", (name, region_id))
    conn.commit()
    conn.close()

def delete_region(region_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM region WHERE region_id = %s", ( region_id))
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Categorias")

# Menu de navegação
menuCat = ["Criar categoria", "Ler categorias", "Atualizar categoria", "Deletar categoria"]
choiceCat = st.sidebar.selectbox("Menu categoria", menuCat)

# Criar categoria
if choiceCat == "Criar categoria":
    st.subheader("Adicionar Nova Categoria")
    with st.form("create_form"):
        name = st.text_input("Nome da Categoria")
        description = st.text_area("Descrição")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_category(name, description)
            st.success(f"Categoria '{name}' adicionada com sucesso!")

# Ler categorias
elif choiceCat == "Ler categorias":
    st.subheader("Lista de Categorias")
    categories = read_categories()
    for category in categories:
        st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")

# Atualizar categoria
elif choiceCat == "Atualizar categoria":
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
elif choiceCat == "Deletar categoria":
    st.subheader("Deletar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
    if st.button("Deletar"):
        delete_category(selected_id)
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")

menuReg = ["Criar região", "Ler regiões", "Atualizar região", "Deletar região"]
choiceReg = st.sidebar.selectbox("Menu região", menuReg)
# Criar região
if choiceReg == "Criar região":
    st.subheader("Adicionar Nova Região")
    with st.form("create_form"):
        name = st.text_input("Nome da Região")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_region(name)
            st.success(f"Região '{name}' adicionada com sucesso!")

# Ler regiões
elif choiceReg == "Ler regiões":
    st.subheader("Lista de Regiões")
    regions = read_regions()
    for region in regions:
        st.write(f"ID: {region[0]} | Nome: {region[1]}")

# Atualizar região
elif choiceReg == "Atualizar região":
    st.subheader("Atualizar Região")
    regions = read_regions()
    region_ids = [region[0] for region in regions]
    selected_id = st.selectbox("Selecione o ID da Região", region_ids)
    selected_region = next((cat for cat in regions if cat[0] == selected_id), None)
    if selected_region:
        with st.form("update_form"):
            new_name = st.text_input("Novo Nome", value=selected_region[1])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_region(selected_id, new_name)
                st.success(f"Região ID {selected_id} atualizada com sucesso!")

# Deletar região
elif choiceReg == "Deletar região":
    st.subheader("Deletar Categoria")
    regions = read_regions()
    region_ids = [region[0] for region in regions]
    selected_id = st.selectbox("Selecione o ID da Região para Deletar", region_ids)
    if st.button("Deletar"):
        delete_region(selected_id)
        st.success(f"Região ID {selected_id} deletada com sucesso!")
