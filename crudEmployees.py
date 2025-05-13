import streamlit as st
import psycopg2
import yaml
import logging

# Configuração do logger
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Função para carregar as credenciais do arquivo YAML
def load_config():
    try:
        with open("config.yml", "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo de configuração: {e}")
        raise

# Função para conectar ao banco de dados RDS
def get_connection():
    try:
        config = load_config()
        db = config["database"]
        return psycopg2.connect(
            host=db["host"],
            port=db["port"],
            user=db["user"],
            password=db["password"],
            dbname=db["dbname"]
        )
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise

# Funções para interagir com a tabela employees
def create_employee(last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees (
                last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path))
        conn.commit()
        logger.info(f"Funcionário '{first_name} {last_name}' criado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar funcionário: {e}")
        raise
    finally:
        conn.close()

def read_employees():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        logger.info("Funcionários lidos com sucesso.")
        return rows
    except Exception as e:
        logger.error(f"Erro ao ler funcionários: {e}")
        raise
    finally:
        conn.close()

def update_employee(employee_id, last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE employees
            SET last_name = %s, first_name = %s, title = %s, title_of_courtesy = %s, birth_date = %s, hire_date = %s, address = %s, city = %s, region = %s, postal_code = %s, country = %s, home_phone = %s, extension = %s, photo = %s, notes = %s, reports_to = %s, photo_path = %s
            WHERE employee_id = %s
            """,
            (last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path, employee_id)
        )
        conn.commit()
        logger.info(f"Funcionário ID {employee_id} atualizado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao atualizar funcionário ID {employee_id}: {e}")
        raise
    finally:
        conn.close()

def delete_employee(employee_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
        conn.commit()
        logger.info(f"Funcionário ID {employee_id} deletado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao deletar funcionário ID {employee_id}: {e}")
        raise
    finally:
        conn.close()

def validate_reports_to(reports_to):
    """Valida se o valor de reports_to existe na tabela employees."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM employees WHERE employee_id = %s", (reports_to,))
        return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"Erro ao validar reports_to: {e}")
        raise
    finally:
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
        title = st.text_input("Título")
        title_of_courtesy = st.text_input("Título de Cortesia")
        birth_date = st.date_input("Data de Nascimento")
        hire_date = st.date_input("Data de Contratação")
        address = st.text_input("Endereço")
        city = st.text_input("Cidade")
        region = st.text_input("Região")
        postal_code = st.text_input("CEP")
        country = st.text_input("País")
        home_phone = st.text_input("Telefone Residencial")
        extension = st.text_input("Ramal")
        photo = st.text_area("Foto (base64 ou URL)")
        notes = st.text_area("Notas")
        reports_to = st.text_input("Reporta-se a (ID)")
        photo_path = st.text_input("Caminho da Foto")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            try:
                # Validar comprimento dos campos
                if len(postal_code) > 4:
                    raise ValueError("O CEP deve ter no máximo 4 caracteres.")
                if len(extension) > 4:
                    raise ValueError("O Ramal deve ter no máximo 4 caracteres.")
                if len(country) > 15:
                    raise ValueError("O País deve ter no máximo 15 caracteres.")

                # Tratar campo reports_to vazio
                reports_to = int(reports_to) if reports_to.isdigit() else None

                # Validar se reports_to existe, se fornecido
                if reports_to and not validate_reports_to(reports_to):
                    raise ValueError(f"O ID de 'Reporta-se a' ({reports_to}) não existe na tabela de funcionários.")

                create_employee(last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path)
                st.success(f"Funcionário '{first_name} {last_name}' adicionado com sucesso!")
            except ValueError as ve:
                logger.info(f"Erro de validação: {ve}")
                st.error(f"Erro de Validação: {str(ve)}")
            except Exception as e:
                logger.error(f"Erro ao adicionar funcionário: {e}")
                st.error(f"Erro: {str(e)}")

# Adicionar funcionalidade para criar um funcionário com ID 1111 para teste
if st.sidebar.button("Criar Funcionário Teste (ID 1111)"):
    try:
        create_employee(
            "Teste", "Funcionário", "Gerente", "Sr.", "1980-01-01", "2020-01-01",
            "Endereço Teste", "Cidade Teste", "Região Teste", "1000", "País Teste",
            "123456789", "1234", "Foto Teste", "Notas Teste", None, "Foto.bmp"
        )
        st.sidebar.success("Funcionário de teste com ID 1111 criado com sucesso!")
    except Exception as e:
        st.sidebar.error(f"Erro ao criar funcionário de teste: {e}")

# Ler funcionários
elif choice == "Ler":
    st.subheader("Lista de Funcionários")
    try:
        employees = read_employees()
        for employee in employees:
            st.write(f"ID: {employee[0]} | Nome: {employee[2]} {employee[1]} | Título: {employee[3]} | Cidade: {employee[8]}")
    except Exception as e:
        st.error("Erro ao carregar a lista de funcionários.")
        logger.error(f"Erro ao carregar a lista de funcionários: {e}")

# Atualizar funcionário
elif choice == "Atualizar":
    st.subheader("Atualizar Funcionário")
    try:
        employees = read_employees()
        employee_ids = [employee[0] for employee in employees]
        selected_id = st.selectbox("Selecione o ID do Funcionário", employee_ids)
        selected_employee = next((emp for emp in employees if emp[0] == selected_id), None)
        if selected_employee:
            with st.form("update_form"):
                last_name = st.text_input("Sobrenome", value=selected_employee[1])
                first_name = st.text_input("Nome", value=selected_employee[2])
                title = st.text_input("Título", value=selected_employee[3])
                title_of_courtesy = st.text_input("Título de Cortesia", value=selected_employee[4])
                birth_date = st.date_input("Data de Nascimento", value=selected_employee[5])
                hire_date = st.date_input("Data de Contratação", value=selected_employee[6])
                address = st.text_input("Endereço", value=selected_employee[7])
                city = st.text_input("Cidade", value=selected_employee[8])
                region = st.text_input("Região", value=selected_employee[9])
                postal_code = st.text_input("CEP", value=selected_employee[10])
                country = st.text_input("País", value=selected_employee[11])
                home_phone = st.text_input("Telefone Residencial", value=selected_employee[12])
                extension = st.text_input("Ramal", value=selected_employee[13])
                photo = st.text_area("Foto (base64 ou URL)", value=selected_employee[14])
                notes = st.text_area("Notas", value=selected_employee[15])
                reports_to = st.text_input("Reporta-se a (ID)", value=selected_employee[16])
                photo_path = st.text_input("Caminho da Foto", value=selected_employee[17])
                submitted = st.form_submit_button("Atualizar")
                if submitted:
                    try:
                        update_employee(selected_id, last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path)
                        st.success(f"Funcionário ID {selected_id} atualizado com sucesso!")
                    except Exception as e:
                        logger.error(f"Erro ao atualizar funcionário ID {selected_id}: {e}")
                        st.error(f"Erro: {str(e)}")
    except Exception as e:
        logger.error(f"Erro ao carregar funcionários para atualização: {e}")
        st.error("Erro ao carregar funcionários para atualização.")

# Deletar funcionário
elif choice == "Deletar":
    st.subheader("Deletar Funcionário")
    try:
        employees = read_employees()
        employee_ids = [employee[0] for employee in employees]
        selected_id = st.selectbox("Selecione o ID do Funcionário para Deletar", employee_ids)
        if st.button("Deletar"):
            try:
                delete_employee(selected_id)
                st.success(f"Funcionário ID {selected_id} deletado com sucesso!")
            except Exception as e:
                logger.error(f"Erro ao deletar funcionário ID {selected_id}: {e}")
                st.error(f"Erro: {str(e)}")
    except Exception as e:
        logger.error(f"Erro ao carregar funcionários para exclusão: {e}")
        st.error("Erro ao carregar funcionários para exclusão.")
