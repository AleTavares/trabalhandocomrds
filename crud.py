import streamlit as st
import psycopg2
from psycopg2 import OperationalError

# Configurações do banco de dados
DB_CONFIG = {
    "host": "dbaulaunifaat-instance-1.cfygeg4cig34.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "user": "postgres",
    "password": "aulaUniFAAT",
    "dbname": "northwind"
}

# Função para conectar ao banco de dados
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except OperationalError as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Funções CRUD para produtos
def create_product(product_data):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO products (
                product_name, supplier_id, category_id, quantity_per_unit, 
                unit_price, units_in_stock, units_on_order, reorder_level, discontinued
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING product_id
            """
            cursor.execute(query, (
                product_data['product_name'], 
                product_data['supplier_id'] if product_data['supplier_id'] else None,
                product_data['category_id'] if product_data['category_id'] else None,
                product_data['quantity_per_unit'],
                product_data['unit_price'],
                product_data['units_in_stock'],
                product_data['units_on_order'],
                product_data['reorder_level'],
                product_data['discontinued']
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()
            st.success(f"Produto '{product_data['product_name']}' criado com sucesso! ID: {new_id}")
            return new_id
        except Exception as e:
            conn.rollback()
            st.error(f"Erro ao criar produto: {e}")
        finally:
            conn.close()
    return None

def read_products(search_term=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if search_term:
                query = """
                SELECT product_id, product_name, supplier_id, category_id, 
                       quantity_per_unit, unit_price, units_in_stock, 
                       units_on_order, reorder_level, discontinued 
                FROM products 
                WHERE product_name ILIKE %s
                ORDER BY product_name
                """
                cursor.execute(query, (f"%{search_term}%",))
            else:
                query = """
                SELECT product_id, product_name, supplier_id, category_id, 
                       quantity_per_unit, unit_price, units_in_stock, 
                       units_on_order, reorder_level, discontinued 
                FROM products 
                ORDER BY product_name
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            st.error(f"Erro ao ler produtos: {e}")
            return []
        finally:
            conn.close()
    return []

def read_product(product_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            SELECT product_id, product_name, supplier_id, category_id, 
                   quantity_per_unit, unit_price, units_in_stock, 
                   units_on_order, reorder_level, discontinued 
            FROM products 
            WHERE product_id = %s
            """
            cursor.execute(query, (product_id,))
            return cursor.fetchone()
        except Exception as e:
            st.error(f"Erro ao ler produto: {e}")
            return None
        finally:
            conn.close()
    return None

def update_product(product_id, product_data):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            UPDATE products SET 
                product_name = %s, supplier_id = %s, category_id = %s, 
                quantity_per_unit = %s, unit_price = %s, units_in_stock = %s, 
                units_on_order = %s, reorder_level = %s, discontinued = %s
            WHERE product_id = %s
            """
            cursor.execute(query, (
                product_data['product_name'], 
                product_data['supplier_id'] if product_data['supplier_id'] else None,
                product_data['category_id'] if product_data['category_id'] else None,
                product_data['quantity_per_unit'],
                product_data['unit_price'],
                product_data['units_in_stock'],
                product_data['units_on_order'],
                product_data['reorder_level'],
                product_data['discontinued'],
                product_id
            ))
            conn.commit()
            st.success(f"Produto ID {product_id} atualizado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            st.error(f"Erro ao atualizar produto: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_product(product_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Verificar se o produto existe
            cursor.execute("SELECT product_name FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                product_name = product[0]
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                conn.commit()
                st.success(f"Produto '{product_name}' (ID: {product_id}) deletado com sucesso!")
                return True
            else:
                st.warning(f"Produto com ID {product_id} não encontrado.")
                return False
        except Exception as e:
            conn.rollback()
            st.error(f"Erro ao deletar produto: {e}")
            return False
        finally:
            conn.close()
    return False

# Interface do Streamlit
def main():
    st.set_page_config(page_title="Northwind - Gerenciamento de Produtos", layout="wide")
    
    st.title("📦 Northwind - Gerenciamento de Produtos")
    st.markdown("---")
    
    # Menu de navegação
    menu = ["Adicionar Produto", "Visualizar Produtos", "Editar Produto", "Remover Produto"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    # Adicionar Produto
    if choice == "Adicionar Produto":
        st.subheader("➕ Adicionar Novo Produto")
        
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input("Nome do Produto*", max_chars=40)
                supplier_id = st.number_input("ID do Fornecedor", min_value=0, step=1, value=0)
                category_id = st.number_input("ID da Categoria", min_value=0, step=1, value=0)
                quantity_per_unit = st.text_input("Quantidade por Unidade", max_chars=20)
                
            with col2:
                unit_price = st.number_input("Preço Unitário", min_value=0.0, step=0.01, value=0.0)
                units_in_stock = st.number_input("Unidades em Estoque", min_value=0, step=1, value=0)
                units_on_order = st.number_input("Unidades em Pedido", min_value=0, step=1, value=0)
                reorder_level = st.number_input("Nível de Reabastecimento", min_value=0, step=1, value=0)
                discontinued = st.checkbox("Descontinuado")
            
            submitted = st.form_submit_button("Salvar Produto")
            
            if submitted:
                if not product_name:
                    st.error("O nome do produto é obrigatório!")
                else:
                    product_data = {
                        'product_name': product_name.strip(),
                        'supplier_id': supplier_id if supplier_id > 0 else None,
                        'category_id': category_id if category_id > 0 else None,
                        'quantity_per_unit': quantity_per_unit.strip() if quantity_per_unit else None,
                        'unit_price': unit_price if unit_price > 0 else 0,
                        'units_in_stock': units_in_stock,
                        'units_on_order': units_on_order,
                        'reorder_level': reorder_level,
                        'discontinued': discontinued
                    }
                    create_product(product_data)
    
    # Visualizar Produtos
    elif choice == "Visualizar Produtos":
        st.subheader("🔍 Visualizar Produtos")
        
        search_term = st.text_input("Pesquisar por nome do produto")
        products = read_products(search_term)
        
        if not products:
            st.info("Nenhum produto encontrado.")
        else:
            st.write(f"**Total de produtos:** {len(products)}")
            
            for product in products:
                with st.expander(f"**{product[1]}** (ID: {product[0]})"):
                    cols = st.columns([1, 1, 1])
                    
                    with cols[0]:
                        st.write("**Fornecedor ID:**", product[2] if product[2] else "N/A")
                        st.write("**Categoria ID:**", product[3] if product[3] else "N/A")
                        st.write("**Quantidade por Unidade:**", product[4] if product[4] else "N/A")
                    
                    with cols[1]:
                        st.write("**Preço Unitário:**", f"${product[5]:.2f}" if product[5] else "N/A")
                        st.write("**Em Estoque:**", product[6] if product[6] is not None else "N/A")
                        st.write("**Em Pedido:**", product[7] if product[7] is not None else "N/A")
                    
                    with cols[2]:
                        st.write("**Nível de Reabastecimento:**", product[8] if product[8] is not None else "N/A")
                        st.write("**Status:**", "❌ Descontinuado" if product[9] else "✅ Ativo")
    
    # Editar Produto
    elif choice == "Editar Produto":
        st.subheader("✏️ Editar Produto")
        
        products = read_products()
        if not products:
            st.info("Nenhum produto cadastrado para editar.")
        else:
            # Criar um dicionário para o seletor {ID: Nome}
            product_options = {p[0]: p[1] for p in products}
            selected_id = st.selectbox(
                "Selecione o produto para editar",
                options=list(product_options.keys()),
                format_func=lambda x: f"{product_options[x]} (ID: {x})"
            )
            
            product = read_product(selected_id)
            if product:
                with st.form("edit_product_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        product_name = st.text_input("Nome do Produto*", value=product[1], max_chars=40)
                        supplier_id = st.number_input(
                            "ID do Fornecedor", 
                            min_value=0, 
                            step=1, 
                            value=product[2] if product[2] else 0
                        )
                        category_id = st.number_input(
                            "ID da Categoria", 
                            min_value=0, 
                            step=1, 
                            value=product[3] if product[3] else 0
                        )
                        quantity_per_unit = st.text_input(
                            "Quantidade por Unidade", 
                            value=product[4] if product[4] else "", 
                            max_chars=20
                        )
                    
                    with col2:
                        unit_price = st.number_input(
                            "Preço Unitário", 
                            min_value=0.0, 
                            step=0.01, 
                            value=float(product[5]) if product[5] else 0.0
                        )
                        units_in_stock = st.number_input(
                            "Unidades em Estoque", 
                            min_value=0, 
                            step=1, 
                            value=product[6] if product[6] is not None else 0
                        )
                        units_on_order = st.number_input(
                            "Unidades em Pedido", 
                            min_value=0, 
                            step=1, 
                            value=product[7] if product[7] is not None else 0
                        )
                        reorder_level = st.number_input(
                            "Nível de Reabastecimento", 
                            min_value=0, 
                            step=1, 
                            value=product[8] if product[8] is not None else 0
                        )
                        discontinued = st.checkbox(
                            "Descontinuado", 
                            value=True if product[9] else False
                        )
                    
                    submitted = st.form_submit_button("Atualizar Produto")
                    
                    if submitted:
                        if not product_name:
                            st.error("O nome do produto é obrigatório!")
                        else:
                            product_data = {
                                'product_name': product_name.strip(),
                                'supplier_id': supplier_id if supplier_id > 0 else None,
                                'category_id': category_id if category_id > 0 else None,
                                'quantity_per_unit': quantity_per_unit.strip() if quantity_per_unit else None,
                                'unit_price': unit_price,
                                'units_in_stock': units_in_stock,
                                'units_on_order': units_on_order,
                                'reorder_level': reorder_level,
                                'discontinued': discontinued
                            }
                            if update_product(selected_id, product_data):
                                st.experimental_rerun()
    
    # Remover Produto
    elif choice == "Remover Produto":
        st.subheader("🗑️ Remover Produto")
        
        products = read_products()
        if not products:
            st.info("Nenhum produto cadastrado para remover.")
        else:
            # Criar um dicionário para o seletor {ID: Nome}
            product_options = {p[0]: p[1] for p in products}
            selected_id = st.selectbox(
                "Selecione o produto para remover",
                options=list(product_options.keys()),
                format_func=lambda x: f"{product_options[x]} (ID: {x})"
            )
            
            product = read_product(selected_id)
            if product:
                st.warning("Você está prestes a remover permanentemente este produto:")
                st.write(f"**ID:** {product[0]}")
                st.write(f"**Nome:** {product[1]}")
                st.write(f"**Status:** {'Descontinuado' if product[9] else 'Ativo'}")
                
                confirm = st.checkbox("Confirmar exclusão")
                if confirm:
                    if st.button("Remover Produto", type="primary"):
                        if delete_product(selected_id):
                            st.experimental_rerun()

if __name__ == "__main__":
    main()