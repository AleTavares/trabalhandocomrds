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

# Funções para interagir com o banco de dados para a tabela category
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

# Funções para interagir com o banco de dados para a tabela region
def create_region(region_description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO region (region_description) VALUES (%s)", (region_description,))
    conn.commit()
    conn.close()

def read_regions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM region")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_region(region_id, region_description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE region SET region_description = %s WHERE region_id = %s", (region_description, region_id))
    conn.commit()
    conn.close()

def delete_region(region_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM region WHERE region_id = %s", (region_id,))
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Categorias e Regiões")

# Menu de navegação
menu = ["Gerenciar Categorias", "Gerenciar Regiões"]
choice = st.sidebar.selectbox("Escolha o CRUD", menu)

# Opção de CRUD para Categorias
if choice == "Gerenciar Categorias":
    sub_menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    category_choice = st.sidebar.selectbox("Escolha a ação", sub_menu)

    # Criar categoria
    if category_choice == "Criar":
        st.subheader("Adicionar Nova Categoria")
        with st.form("create_category_form"):
            name = st.text_input("Nome da Categoria")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_category(name, description)
                st.success(f"Categoria '{name}' adicionada com sucesso!")

    # Ler categorias
    elif category_choice == "Ler":
        st.subheader("Lista de Categorias")
        categories = read_categories()
        for category in categories:
            st.write(f"ID: {category[0]} | Nome: {category[1]} | Descrição: {category[2]}")

    # Atualizar categoria
    elif category_choice == "Atualizar":
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
    elif category_choice == "Deletar":
        st.subheader("Deletar Categoria")
        categories = read_categories()
        category_ids = [category[0] for category in categories]
        selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids)
        if st.button("Deletar"):
            delete_category(selected_id)
            st.success(f"Categoria ID {selected_id} deletada com sucesso!")

# Opção de CRUD para Regiões
elif choice == "Gerenciar Regiões":
    sub_menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    region_choice = st.sidebar.selectbox("Escolha a ação", sub_menu)

    # Criar região
    if region_choice == "Criar":
        st.subheader("Adicionar Nova Região")
        with st.form("create_region_form"):
            region_description = st.text_input("Descrição da Região")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_region(region_description)
                st.success(f"Região '{region_description}' adicionada com sucesso!")

    # Ler regiões
    elif region_choice == "Ler":
        st.subheader("Lista de Regiões")
        regions = read_regions()
        for region in regions:
            st.write(f"ID: {region[0]} | Descrição: {region[1]}")

    # Atualizar região
    elif region_choice == "Atualizar":
        st.subheader("Atualizar Região")
        regions = read_regions()
        region_ids = [region[0] for region in regions]
        selected_id = st.selectbox("Selecione o ID da Região", region_ids)
        selected_region = next((reg for reg in regions if reg[0] == selected_id), None)
        if selected_region:
            with st.form("update_region_form"):
                new_description = st.text_input("Nova Descrição", value=selected_region[1])
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    update_region(selected_id, new_description)
                    st.success(f"Região ID {selected_id} atualizada com sucesso!")

    # Deletar região
    elif region_choice == "Deletar":
        st.subheader("Deletar Região")
        regions = read_regions()
        region_ids = [region[0] for region in regions]
        selected_id = st.selectbox("Selecione o ID da Região para Deletar", region_ids)
        if st.button("Deletar"):
            delete_region(selected_id)
            st.success(f"Região ID {selected_id} deletada com sucesso!")
