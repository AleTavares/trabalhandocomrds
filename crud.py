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
def create_category(category_id, name, description):
    conn = get_connection()
    cursor = conn.cursor()

    # Inserir a nova categoria com o ID fornecido
    cursor.execute(
        "INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s)",
        (category_id, name, description)
    )
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
    cursor.execute(
        "UPDATE categories SET name = %s, description = %s WHERE category_id = %s",
        (name, description, category_id)
    )
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM categories WHERE category_id = %s",
        (category_id,)
    )
    conn.commit()
    conn.close()

# Função para criar um registro em order_details
def create_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (order_id, product_id, unit_price, quantity, discount)
    )
    conn.commit()
    conn.close()

# Função para ler todos os registros de order_details
def read_order_details():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_details")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Função para atualizar um registro em order_details
def update_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE order_details
        SET unit_price = %s, quantity = %s, discount = %s
        WHERE order_id = %s AND product_id = %s
        """,
        (unit_price, quantity, discount, order_id, product_id)
    )
    conn.commit()
    conn.close()

# Função para deletar um registro de order_details
def delete_order_detail(order_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM order_details WHERE order_id = %s AND product_id = %s",
        (order_id, product_id)
    )
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Dados")

# Seleção de Tabela
table_choice = st.sidebar.selectbox("Selecione a Tabela", ["Categorias", "Order Details"])

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Gerenciamento de Categorias
if table_choice == "Categorias":
    st.header("Gerenciamento de Categorias")

    if choice == "Criar":
        st.subheader("Adicionar Nova Categoria")
        with st.form("create_category_form"):
            category_id = st.number_input("ID da Categoria", min_value=1, step=1)
            name = st.text_input("Nome da Categoria")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_category(category_id, name, description)
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
            with st.form("update_category_form"):
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

# Gerenciamento de Order Details
elif table_choice == "Order Details":
    st.header("Gerenciamento de Order Details")

    if choice == "Criar":
        st.subheader("Adicionar Novo Order Detail")
        with st.form("create_order_detail_form"):
            order_id = st.number_input("Order ID", min_value=1, step=1)
            product_id = st.number_input("Product ID", min_value=1, step=1)
            unit_price = st.number_input("Unit Price", min_value=0.0, step=0.01)
            quantity = st.number_input("Quantity", min_value=1, step=1)
            discount = st.number_input("Discount", min_value=0.0, step=0.01)
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_order_detail(order_id, product_id, unit_price, quantity, discount)
                st.success(f"Order Detail (Order ID: {order_id}, Product ID: {product_id}) adicionado com sucesso!")

    elif choice == "Ler":
        st.subheader("Lista de Order Details")
        order_details = read_order_details()
        for detail in order_details:
            st.write(f"Order ID: {detail[0]} | Product ID: {detail[1]} | Unit Price: {detail[2]} | Quantity: {detail[3]} | Discount: {detail[4]}")

    elif choice == "Atualizar":
        st.subheader("Atualizar Order Detail")
        order_details = read_order_details()
        order_ids = [(detail[0], detail[1]) for detail in order_details]
        selected_order = st.selectbox("Selecione o Order ID e Product ID", order_ids)
        selected_detail = next((detail for detail in order_details if (detail[0], detail[1]) == selected_order), None)
        if selected_detail:
            with st.form("update_order_detail_form"):
                new_unit_price = st.number_input("Novo Unit Price", value=selected_detail[2], step=0.01)
                new_quantity = st.number_input("Nova Quantity", value=selected_detail[3], step=1)
                new_discount = st.number_input("Novo Discount", value=selected_detail[4], step=0.01)
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    update_order_detail(selected_detail[0], selected_detail[1], new_unit_price, new_quantity, new_discount)
                    st.success(f"Order Detail (Order ID: {selected_detail[0]}, Product ID: {selected_detail[1]}) atualizado com sucesso!")

    elif choice == "Deletar":
        st.subheader("Deletar Order Detail")
        order_details = read_order_details()
        order_ids = [(detail[0], detail[1]) for detail in order_details]
        selected_order = st.selectbox("Selecione o Order ID e Product ID para Deletar", order_ids)
        if st.button("Deletar"):
            delete_order_detail(selected_order[0], selected_order[1])
            st.success(f"Order Detail (Order ID: {selected_order[0]}, Product ID: {selected_order[1]}) deletado com sucesso!")