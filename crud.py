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
    try:
        conn = psycopg2.connect(
            host=db["host"],
            port=db["port"],
            user=db["user"],
            password=db["password"],
            dbname=db["dbname"]
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Funções para interagir com o banco de dados
def create_category(name, description):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao criar categoria: {e}")
        finally:
            conn.close()

def read_categories():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            st.error(f"Erro ao ler categorias: {e}")
            return []
        finally:
            conn.close()

def update_category(category_id, name, description):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE categories SET name = %s, description = %s WHERE id = %s", (name, description, category_id))
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao atualizar categoria: {e}")
        finally:
            conn.close()

def delete_category(category_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao deletar categoria: {e}")
        finally:
            conn.close()

# Interface do Streamlit para categorias
st.title("Gerenciamento de Categorias")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu, key="menu_categories")

# Criar categoria
if choice == "Criar":
    st.subheader("Adicionar Nova Categoria")
    with st.form("create_form_category"):
        name = st.text_input("Nome da Categoria", key="create_name_category")
        description = st.text_area("Descrição", key="create_description_category")
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
    selected_id = st.selectbox("Selecione o ID da Categoria", category_ids, key="update_select_category")
    selected_category = next((cat for cat in categories if cat[0] == selected_id), None)
    if selected_category:
        with st.form("update_form_category"):
            new_name = st.text_input("Novo Nome", value=selected_category[1], key="update_name_category")
            new_description = st.text_area("Nova Descrição", value=selected_category[2], key="update_description_category")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_category(selected_id, new_name, new_description)
                st.success(f"Categoria ID {selected_id} atualizada com sucesso!")

# Deletar categoria
elif choice == "Deletar":
    st.subheader("Deletar Categoria")
    categories = read_categories()
    category_ids = [category[0] for category in categories]
    selected_id = st.selectbox("Selecione o ID da Categoria para Deletar", category_ids, key="delete_select_category")
    if st.button("Deletar"):
        delete_category(selected_id)
        st.success(f"Categoria ID {selected_id} deletada com sucesso!")

# Funções para interagir com a tabela territories
def create_territory(description, region_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO territories (territory_description, region_id) VALUES (%s, %s)", (description, region_id))
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao criar território: {e}")
        finally:
            conn.close()

def read_territories():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM territories")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            st.error(f"Erro ao ler territórios: {e}")
            return []
        finally:
            conn.close()

def update_territory(territory_id, description, region_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE territories SET territory_description = %s, region_id = %s WHERE territory_id = %s", (description, region_id, territory_id))
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao atualizar território: {e}")
        finally:
            conn.close()

def delete_territory(territory_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM territories WHERE territory_id = %s", (territory_id,))
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao deletar território: {e}")
        finally:
            conn.close()

# Interface do Streamlit para territórios
st.title("Gerenciamento de Territórios")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu, key="menu_territories")

# Criar território
if choice == "Criar":
    st.subheader("Adicionar Novo Território")
    with st.form("create_form_territory"):
        description = st.text_area("Descrição do Território", key="create_description_territory")
        region_id = st.number_input("ID da Região", min_value=1, key="create_region_id_territory")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_territory(description, region_id)
            st.success(f"Território '{description}' adicionado com sucesso!")

# Ler territórios
elif choice == "Ler":
    st.subheader("Lista de Territórios")
    territories = read_territories()
    for territory in territories:
        st.write(f"ID: {territory[0]} | Descrição: {territory[1]} | ID da Região: {territory[2]}")

# Atualizar território
elif choice == "Atualizar":
    st.subheader("Atualizar Território")
    territories = read_territories()
    territory_ids = [territory[0] for territory in territories]
    selected_id = st.selectbox("Selecione o ID do Território", territory_ids, key="update_select_territory")
    selected_territory = next((ter for ter in territories if ter[0] == selected_id), None)
    if selected_territory:
        with st.form("update_form_territory"):
            new_description = st.text_area("Nova Descrição", value=selected_territory[1], key="update_description_territory")
            new_region_id = st.number_input("Novo ID da Região", value=selected_territory[2], min_value=1, key="update_region_id_territory")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_territory(selected_id, new_description, new_region_id)
                st.success(f"Território ID {selected_id} atualizado com sucesso!")

# Deletar território
elif choice == "Deletar":
    st.subheader("Deletar Território")
    territories = read_territories()
    territory_ids = [territory[0] for territory in territories]
    selected_id = st.selectbox("Selecione o ID do Território para Deletar", territory_ids, key="delete_select_territory")
    if st.button("Deletar"):
        delete_territory(selected_id)
        st.success(f"Território ID {selected_id} deletado com sucesso!")