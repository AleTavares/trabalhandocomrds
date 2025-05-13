import streamlit as st
import psycopg2
import yaml
import os

# Função para carregar as credenciais do arquivo YAML
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
    with open(config_path, "r") as file:
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

# Funções CRUD para a tabela employees
def create_employee(employee_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees (last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, region, postal_code, country, home_phone, extension, notes, reports_to, photo_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING employee_id
    """, (
        employee_data["last_name"], employee_data["first_name"], employee_data["title"], employee_data["title_of_courtesy"],
        employee_data["birth_date"], employee_data["hire_date"], employee_data["address"], employee_data["region"],
        employee_data["postal_code"], employee_data["country"], employee_data["home_phone"], employee_data["extension"],
        employee_data["notes"], employee_data["reports_to"], employee_data["photo_path"]
    ))
    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return new_id

def read_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_employee(employee_id, updated_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees
        SET last_name = %s, first_name = %s, title = %s, title_of_courtesy = %s, birth_date = %s, hire_date = %s,
            address = %s, region = %s, postal_code = %s, country = %s, home_phone = %s, extension = %s, notes = %s,
            reports_to = %s, photo_path = %s
        WHERE employee_id = %s
    """, (
        updated_data["last_name"], updated_data["first_name"], updated_data["title"], updated_data["title_of_courtesy"],
        updated_data["birth_date"], updated_data["hire_date"], updated_data["address"], updated_data["region"],
        updated_data["postal_code"], updated_data["country"], updated_data["home_phone"], updated_data["extension"],
        updated_data["notes"], updated_data["reports_to"], updated_data["photo_path"], employee_id
    ))
    conn.commit()
    conn.close()

def delete_employee(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Funcionários")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar funcionário
if choice == "Criar":
    st.subheader("Adicionar Novo Funcionário")
    with st.form("create_form"):
        last_name = st.text_input("Sobrenome")
        first_name = st.text_input("Nome")
        title = st.text_input("Título (máx. 4 caracteres)")
        title_of_courtesy = st.text_input("Título de Cortesia")
        birth_date = st.date_input("Data de Nascimento")
        hire_date = st.date_input("Data de Contratação")
        address = st.text_area("Endereço")
        region = st.text_input("Região")
        postal_code = st.text_input("Código Postal")
        country = st.text_input("País")
        home_phone = st.text_input("Telefone Residencial")
        extension = st.text_input("Ramal (máx. 4 caracteres)")
        notes = st.text_area("Notas")
        reports_to = st.number_input("Reporta-se a (ID)", min_value=0, step=1)
        photo_path = st.text_input("Caminho da Foto")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            if not last_name.strip() or not first_name.strip():
                st.error("Os campos 'Sobrenome' e 'Nome' são obrigatórios.")
            elif len(title) > 4:
                st.error("O campo 'Título' deve ter no máximo 4 caracteres.")
            elif len(extension) > 4:
                st.error("O campo 'Ramal' deve ter no máximo 4 caracteres.")
            else:
                employee_data = {
                    "last_name": last_name,
                    "first_name": first_name,
                    "title": title,
                    "title_of_courtesy": title_of_courtesy,
                    "birth_date": birth_date,
                    "hire_date": hire_date,
                    "address": address,
                    "region": region,
                    "postal_code": postal_code,
                    "country": country,
                    "home_phone": home_phone,
                    "extension": extension,
                    "notes": notes,
                    "reports_to": reports_to,
                    "photo_path": photo_path
                }
                new_id = create_employee(employee_data)
                st.success(f"Funcionário '{first_name} {last_name}' adicionado com sucesso! ID: {new_id}")

# Ler funcionários
elif choice == "Ler":
    st.subheader("Lista de Funcionários")
    employees = read_employees()
    for employee in employees:
        st.write(f"ID: {employee[0]} | Nome: {employee[2]} {employee[1]} | Título: {employee[3]}")

# Atualizar funcionário
elif choice == "Atualizar":
    st.subheader("Atualizar Funcionário")
    employees = read_employees()
    employee_ids = [employee[0] for employee in employees]
    selected_id = st.selectbox("Selecione o ID do Funcionário", employee_ids)
    selected_employee = next((emp for emp in employees if emp[0] == selected_id), None)
    if selected_employee:
        with st.form("update_form"):
            new_last_name = st.text_input("Novo Sobrenome", value=selected_employee[1])
            new_first_name = st.text_input("Novo Nome", value=selected_employee[2])
            new_title = st.text_input("Novo Título (máx. 4 caracteres)", value=selected_employee[3])
            new_title_of_courtesy = st.text_input("Novo Título de Cortesia", value=selected_employee[4])
            new_birth_date = st.date_input("Nova Data de Nascimento", value=selected_employee[5])
            new_hire_date = st.date_input("Nova Data de Contratação", value=selected_employee[6])
            new_address = st.text_area("Novo Endereço", value=selected_employee[7])
            new_region = st.text_input("Nova Região", value=selected_employee[8])
            new_postal_code = st.text_input("Novo Código Postal", value=selected_employee[9])
            new_country = st.text_input("Novo País", value=selected_employee[10])
            new_home_phone = st.text_input("Novo Telefone Residencial", value=selected_employee[11])
            new_extension = st.text_input("Novo Ramal (máx. 4 caracteres)", value=selected_employee[12])
            new_notes = st.text_area("Novas Notas", value=selected_employee[13])
            new_reports_to = st.number_input("Novo Reporta-se a (ID)", min_value=0, step=1, value=selected_employee[14])
            new_photo_path = st.text_input("Novo Caminho da Foto", value=selected_employee[15])
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                if len(new_title) > 4:
                    st.error("O campo 'Novo Título' deve ter no máximo 4 caracteres.")
                elif len(new_extension) > 4:
                    st.error("O campo 'Novo Ramal' deve ter no máximo 4 caracteres.")
                else:
                    updated_data = {
                        "last_name": new_last_name,
                        "first_name": new_first_name,
                        "title": new_title,
                        "title_of_courtesy": new_title_of_courtesy,
                        "birth_date": new_birth_date,
                        "hire_date": new_hire_date,
                        "address": new_address,
                        "region": new_region,
                        "postal_code": new_postal_code,
                        "country": new_country,
                        "home_phone": new_home_phone,
                        "extension": new_extension,
                        "notes": new_notes,
                        "reports_to": new_reports_to,
                        "photo_path": new_photo_path
                    }
                    update_employee(selected_id, updated_data)
                    st.success(f"Funcionário ID {selected_id} atualizado com sucesso!")

# Deletar funcionário
elif choice == "Deletar":
    st.subheader("Deletar Funcionário")
    employees = read_employees()
    employee_ids = [employee[0] for employee in employees]
    selected_id = st.selectbox("Selecione o ID do Funcionário para Deletar", employee_ids)
    if st.button("Deletar"):
        delete_employee(selected_id)
        st.success(f"Funcionário ID {selected_id} deletado com sucesso!")
