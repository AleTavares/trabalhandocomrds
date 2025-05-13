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
def create_employees(first_name, last_name, title, hire_date):
    conn = get_connection()
    cursor = conn.cursor()

    # Obter o maior valor atual de employee_id
    cursor.execute("SELECT COALESCE(MAX(employee_id), 0) + 1 FROM employees")
    new_employee_id = cursor.fetchone()[0]

    # Inserir o novo funcionário com o ID gerado
    cursor.execute(
        "INSERT INTO employees (employee_id, first_name, last_name, title, hire_date) VALUES (%s, %s, %s, %s, %s)",
        (new_employee_id, first_name, last_name, title, hire_date)
    )
    conn.commit()
    conn.close()

def read_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_employees(employee_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()

    # Gerar a lista de campos a serem atualizados dinamicamente
    fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values()) + [employee_id]

    # Atualizar o funcionário com os campos fornecidos
    query = f"UPDATE employees SET {fields} WHERE employee_id = %s"
    cursor.execute(query, values)

    conn.commit()
    conn.close()

def delete_employees(employee_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Altere 'id' para 'employee_id' na query
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    
    conn.commit()
    conn.close()


# Interface do Streamlit
st.title("Gerenciamento de employees")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar funcionário
if choice == "Criar":
    st.subheader("Adicionar Novo Funcionário")
    with st.form("create_form"):
        first_name = st.text_input("Primeiro Nome")
        last_name = st.text_input("Último Nome")
        title = st.text_input("Título")
        hire_date = st.date_input("Data de Contratação")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            create_employees(first_name, last_name, title, hire_date)
            st.success(f"Funcionário '{first_name} {last_name}' adicionado com sucesso!")

# Ler funcionários
elif choice == "Ler":
    st.subheader("Lista de Funcionários")
    employees = read_employees()
    for employee in employees:
        st.write(f"ID: {employee[0]} | Nome: {employee[2]} {employee[1]} | Título: {employee[3]} | Data de Contratação: {employee[5]}")

# Atualizar funcionário
elif choice == "Atualizar":
    st.subheader("Atualizar Funcionário")
    employees = read_employees()
    employee_id = [employee[0] for employee in employees]
    selected_id = st.selectbox("Selecione o ID do Funcionário", employee_id)
    selected_employee = next((emp for emp in employees if emp[0] == selected_id), None)
    if selected_employee:
        with st.form("update_form"):
            new_first_name = st.text_input("Novo Primeiro Nome", value=selected_employee[2])
            new_last_name = st.text_input("Novo Último Nome", value=selected_employee[1])
            new_title = st.text_input("Novo Título", value=selected_employee[3])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                update_employees(selected_id, first_name=new_first_name, last_name=new_last_name, title=new_title)
                st.success(f"Funcionário ID {selected_id} atualizado com sucesso!")

# Deletar funcionário
elif choice == "Deletar":
    st.subheader("Deletar Funcionário")
    employees = read_employees()
    employee_id = [employee[0] for employee in employees]
    selected_id = st.selectbox("Selecione o ID do Funcionário para Deletar", employee_id)
    if st.button("Deletar"):
        delete_employees(selected_id)
        st.success(f"Funcionário ID {selected_id} deletado com sucesso!")