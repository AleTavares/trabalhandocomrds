import streamlit as st
from crud_order_details import create_order_detail, read_order_details, update_order_detail, delete_order_detail

# Interface do Streamlit
st.title("Gerenciamento de Detalhes do Pedido")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar detalhe do pedido
if choice == "Criar":
    st.subheader("Adicionar Novo Detalhe de Pedido")
    with st.form("create_form"):
        order_id = st.number_input("ID do Pedido", min_value=1, step=1)
        product_id = st.number_input("ID do Produto", min_value=1, step=1)
        unit_price = st.number_input("Preço Unitário", min_value=0.01, step=0.01)
        quantity = st.number_input("Quantidade", min_value=1, step=1)
        discount = st.number_input("Desconto", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_order_detail(order_id, product_id, unit_price, quantity, discount)
            st.success(f"Detalhe do Pedido para o Pedido ID {order_id} adicionado com sucesso!")

# Ler detalhes do pedido
elif choice == "Ler":
    st.subheader("Lista de Detalhes do Pedido")
    order_details = read_order_details()
    for detail in order_details:
        st.write(f"Pedido ID: {detail[0]} | Produto ID: {detail[1]} | Preço Unitário: {detail[2]} | Quantidade: {detail[3]} | Desconto: {detail[4]}")

# Atualizar detalhe do pedido
elif choice == "Atualizar":
    st.subheader("Atualizar Detalhe de Pedido")
    order_details = read_order_details()
    order_ids = list(set([detail[0] for detail in order_details]))
    product_ids = list(set([detail[1] for detail in order_details]))
    selected_order_id = st.selectbox("Selecione o ID do Pedido", order_ids)
    selected_product_id = st.selectbox("Selecione o ID do Produto", product_ids)
    
    selected_detail = next((det for det in order_details if det[0] == selected_order_id and det[1] == selected_product_id), None)
    if selected_detail:
        with st.form("update_form"):
            new_unit_price = st.number_input("Novo Preço Unitário", value=selected_detail[2], min_value=0.01, step=0.01)
            new_quantity = st.number_input("Nova Quantidade", value=selected_detail[3], min_value=1, step=1)
            new_discount = st.number_input("Novo Desconto", value=selected_detail[4], min_value=0.0, step=0.01)
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_order_detail(selected_order_id, selected_product_id, new_unit_price, new_quantity, new_discount)
                st.success(f"Detalhe do Pedido (ID {selected_order_id}, Produto {selected_product_id}) atualizado com sucesso!")

# Deletar detalhe do pedido
elif choice == "Deletar":
    st.subheader("Deletar Detalhe de Pedido")
    order_details = read_order_details()
    order_ids = list(set([detail[0] for detail in order_details]))
    product_ids = list(set([detail[1] for detail in order_details]))
    selected_order_id = st.selectbox("Selecione o ID do Pedido", order_ids)
    selected_product_id = st.selectbox("Selecione o ID do Produto", product_ids)
    if st.button("Deletar"):
        delete_order_detail(selected_order_id, selected_product_id)
        st.success(f"Detalhe do Pedido (ID {selected_order_id}, Produto {selected_product_id}) deletado com sucesso!")
