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
        dbname=db["dbname"],
    )


# Funções para interagir com o banco de dados
def create_category(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (name, description) VALUES (%s, %s)",
        (name, description),
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
        "UPDATE categories SET name = %s, description = %s WHERE id = %s",
        (name, description, category_id),
    )
    conn.commit()
    conn.close()


def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()


# funç~oes para interação da tabela customers
def create_employee_territory(employee_id, territory_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employee_territories (employee_id, territory_id) VALUES (%s, %s)",
        (employee_id, territory_id),
    )
    conn.commit()
    conn.close()


def read_employee_territories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_territories")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_employee_territory(employee_id, old_territory_id, new_territory_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employee_territories SET territory_id = %s WHERE employee_id = %s AND territory_id = %s",
        (new_territory_id, employee_id, old_territory_id),
    )
    conn.commit()
    conn.close()


def delete_employee_territory(employee_id, territory_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM employee_territories WHERE employee_id = %s AND territory_id = %s",
        (employee_id, territory_id),
    )
    conn.commit()
    conn.close()


# Interface do Streamlit
st.title("Gerenciamento de Employee Territories")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar employee territory
if choice == "Criar":
    st.subheader("Adicionar novo Employee Territory")
    with st.form("create_form"):
        employee_id = st.number_input("Employee ID", min_value=1, step=1)
        territory_id = st.text_input("Territory ID")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_employee_territory(employee_id, territory_id)
            st.success(
                f"Employee Territory ({employee_id}, {territory_id}) adicionado com sucesso!"
            )

# Ler employee territory
elif choice == "Ler":
    st.subheader("Lista de Employee Territories")
    territories = read_employee_territories()
    for et in territories:
        st.write(f"Employee ID: {et[0]} | Territory ID: {et[1]}")

# Atualizar employee territory
elif choice == "Atualizar":
    st.subheader("Atualizar Employee Territory")
    territories = read_employee_territories()
    if territories:
        options = [(et[0], et[1]) for et in territories]
        selected = st.selectbox(
            "Selecione o par (Employee ID, Territory ID)",
            options,
            format_func=lambda x: f"Employee ID: {x[0]}, Territory ID: {x[1]}",
        )
        new_territory_id = st.text_input("Novo Territory ID")
        if st.button("Atualizar"):
            update_employee_territory(selected[0], selected[1], new_territory_id)
            st.success(
                f"Employee Territory ({selected[0]}, {selected[1]}) atualizado para Territory ID {new_territory_id}!"
            )
    else:
        st.info("Nenhum registro encontrado.")

# Deletar employee territory
elif choice == "Deletar":
    st.subheader("Deletar Employee Territory")
    territories = read_employee_territories()
    if territories:
        options = [(et[0], et[1]) for et in territories]
        selected = st.selectbox(
            "Selecione o par (Employee ID, Territory ID) para deletar",
            options,
            format_func=lambda x: f"Employee ID: {x[0]}, Territory ID: {x[1]}",
        )
        if st.button("Deletar"):
            delete_employee_territory(selected[0], selected[1])
            st.success(
                f"Employee Territory ({selected[0]}, {selected[1]}) deletado com sucesso!"
            )
    else:
        st.info("Nenhum registro encontrado.")
