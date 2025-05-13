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

# Funções para interagir com a tabela order_details
def create_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (order_id, product_id, unit_price, quantity, discount),
    )
    conn.commit()
    conn.close()

def read_order_details():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_details")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE order_details
        SET unit_price = %s, quantity = %s, discount = %s
        WHERE order_id = %s AND product_id = %s
        """,
        (unit_price, quantity, discount, order_id, product_id),
    )
    conn.commit()
    conn.close()

def delete_order_detail(order_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM order_details WHERE order_id = %s AND product_id = %s",
        (order_id, product_id),
    )
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Categorias")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar", "Order Details"]
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

# Interface do Streamlit para order_details
elif choice == "Order Details":
    st.subheader("Gerenciamento de Order Details")
    action = st.selectbox("Escolha a ação", ["Criar", "Ler", "Atualizar", "Deletar"])

    if action == "Criar":
        with st.form("create_order_detail_form"):
            order_id = st.number_input("Order ID", min_value=1, step=1)
            product_id = st.number_input("Product ID", min_value=1, step=1)
            unit_price = st.number_input("Unit Price", min_value=0.0, step=0.01)
            quantity = st.number_input("Quantity", min_value=1, step=1)
            discount = st.number_input("Discount", min_value=0.0, step=0.01)
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                create_order_detail(order_id, product_id, unit_price, quantity, discount)
                st.success("Order Detail adicionado com sucesso!")

    elif action == "Ler":
        st.subheader("Lista de Order Details")
        order_details = read_order_details()
        for detail in order_details:
            st.write(
                f"Order ID: {detail[0]} | Product ID: {detail[1]} | Unit Price: {detail[2]} | Quantity: {detail[3]} | Discount: {detail[4]}"
            )

    elif action == "Atualizar":
        st.subheader("Atualizar Order Detail")
        order_details = read_order_details()
        order_ids = [(detail[0], detail[1]) for detail in order_details]
        selected_order = st.selectbox("Selecione o Order ID e Product ID", order_ids)
        if selected_order:
            selected_detail = next(
                (detail for detail in order_details if (detail[0], detail[1]) == selected_order), None
            )
            if selected_detail:
                with st.form("update_order_detail_form"):
                    unit_price = st.number_input("Unit Price", value=selected_detail[2], step=0.01)
                    quantity = st.number_input("Quantity", value=selected_detail[3], step=1)
                    discount = st.number_input("Discount", value=selected_detail[4], step=0.01)
                    submitted = st.form_submit_button("Atualizar")
                    if submitted:
                        update_order_detail(
                            selected_order[0], selected_order[1], unit_price, quantity, discount
                        )
                        st.success("Order Detail atualizado com sucesso!")

    elif action == "Deletar":
        st.subheader("Deletar Order Detail")
        order_details = read_order_details()
        order_ids = [(detail[0], detail[1]) for detail in order_details]
        selected_order = st.selectbox("Selecione o Order ID e Product ID para deletar", order_ids)
        if st.button("Deletar"):
            delete_order_detail(selected_order[0], selected_order[1])
            st.success("Order Detail deletado com sucesso!")
