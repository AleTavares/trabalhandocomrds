import streamlit as st
import psycopg2
import yaml

# Função para carregar as credenciais do arquivo YAML
def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

# Função para conectar ao banco de dados RDS
def get_connection():
    config = load_config()["database"]
    return psycopg2.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        dbname=config["dbname"]
    )

# Funções CRUD para a tabela order_details
def create_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount) VALUES (%s, %s, %s, %s, %s)",
        (order_id, product_id, unit_price, quantity, discount)
    )
    conn.commit()
    cursor.close()
    conn.close()

def read_order_details():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_details")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def update_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE order_details SET unit_price = %s, quantity = %s, discount = %s WHERE order_id = %s AND product_id = %s",
        (unit_price, quantity, discount, order_id, product_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_order_detail(order_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_details WHERE order_id = %s AND product_id = %s", (order_id, product_id))
    conn.commit()
    cursor.close()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Detalhes de Pedidos")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar um novo detalhe de pedido
if choice == "Criar":
    st.subheader("Adicionar Novo Detalhe de Pedido")
    with st.form("create_form"):
        order_id = st.number_input("ID do Pedido", min_value=1)
        product_id = st.number_input("ID do Produto", min_value=1)
        unit_price = st.number_input("Preço Unitário", min_value=0.01)
        quantity = st.number_input("Quantidade", min_value=1)
        discount = st.number_input("Desconto", min_value=0.0, max_value=1.0)
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_order_detail(order_id, product_id, unit_price, quantity, discount)
            st.success("Detalhe do pedido adicionado com sucesso!")

# Ler detalhes de pedidos
elif choice == "Ler":
    st.subheader("Lista de Detalhes de Pedidos")
    order_details = read_order_details()
    for detail in order_details:
        st.write(f"Pedido ID: {detail[0]} | Produto ID: {detail[1]} | Preço: {detail[2]} | Quantidade: {detail[3]} | Desconto: {detail[4]}")

# Atualizar detalhes de pedidos
elif choice == "Atualizar":
    st.subheader("Atualizar Detalhe de Pedido")
    order_details = read_order_details()
    order_ids = list(set([detail[0] for detail in order_details]))  # Lista única de pedidos
    selected_order_id = st.selectbox("Selecione o ID do Pedido", order_ids)
    product_ids = [detail[1] for detail in order_details if detail[0] == selected_order_id]
    selected_product_id = st.selectbox("Selecione o ID do Produto", product_ids)

    selected_detail = next((detail for detail in order_details if detail[0] == selected_order_id and detail[1] == selected_product_id), None)
    if selected_detail:
        with st.form("update_form"):
            new_unit_price = st.number_input("Novo Preço Unitário", value=selected_detail[2])
            new_quantity = st.number_input("Nova Quantidade", value=selected_detail[3])
            new_discount = st.number_input("Novo Desconto", value=selected_detail[4], min_value=0.0, max_value=1.0)
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_order_detail(selected_order_id, selected_product_id, new_unit_price, new_quantity, new_discount)
                st.success("Detalhe do pedido atualizado com sucesso!")

# Deletar detalhes de pedidos
elif choice == "Deletar":
    st.subheader("Deletar Detalhe de Pedido")
    order_details = read_order_details()
    order_ids = list(set([detail[0] for detail in order_details]))
    selected_order_id = st.selectbox("Selecione o ID do Pedido", order_ids)
    product_ids = [detail[1] for detail in order_details if detail[0] == selected_order_id]
    selected_product_id = st.selectbox("Selecione o ID do Produto", product_ids)

    if st.button("Deletar"):
        delete_order_detail(selected_order_id, selected_product_id)
        st.success("Detalhe do pedido deletado com sucesso!")