import streamlit as st
import psycopg2
import yaml

# Função para carregar as credenciais do arquivo YAML
def load_config():
    try:
        with open("config.yml", "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Erro ao carregar configuração: {e}")
        return None

# Função para conectar ao banco de dados RDS com tratamento de erro
def get_connection():
    config = load_config()
    if not config:
        return None
    try:
        db = config["database"]
        conn = psycopg2.connect(
            host=db["host"],
            port=db["port"],
            user=db["user"],
            password=db["password"],
            dbname=db["dbname"]
        )
        return conn
    except psycopg2.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Funções para interagir com o banco de dados
def create_territory(territory_id, territory_description, region_id):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO territories (territory_id, territory_description, region_id) VALUES (%s, %s, %s)",
                               (territory_id, territory_description, region_id))
                conn.commit()
                st.success(f"Território '{territory_description}' adicionado com sucesso!")
        except psycopg2.Error as e:
            st.error(f"Erro ao inserir território: {e}")
        finally:
            conn.close()

def read_territories():
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT territory_id, territory_description, region_id FROM territories")
                rows = cursor.fetchall()
                return rows
        except psycopg2.Error as e:
            st.error(f"Erro ao buscar territórios: {e}")
            return []
        finally:
            conn.close()
    return []

def update_territory(territory_id, new_description, new_region_id):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE territories SET territory_description = %s, region_id = %s WHERE territory_id = %s",
                               (new_description, new_region_id, territory_id))
                conn.commit()
                st.success(f"Território ID {territory_id} atualizado com sucesso!")
        except psycopg2.Error as e:
            st.error(f"Erro ao atualizar território: {e}")
        finally:
            conn.close()

def delete_territory(territory_id):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM territories WHERE territory_id = %s", (territory_id,))
                conn.commit()
                st.success(f"Território ID {territory_id} deletado com sucesso!")
        except psycopg2.Error as e:
            st.error(f"Erro ao deletar território: {e}")
        finally:
            conn.close()

# Interface do Streamlit
st.title("Gerenciamento de Territórios")

# Menu de navegação
menu = ["Criar", "Ler", "Atualizar", "Deletar"]
choice = st.sidebar.selectbox("Menu", menu)

# Criar território
if choice == "Criar":
    st.subheader("Adicionar Novo Território")
    with st.form("create_form"):
        territory_id = st.text_input("ID do Território")
        territory_description = st.text_input("Descrição do Território")
        region_id = st.number_input("ID da Região", min_value=1, step=1)
        submitted = st.form_submit_button("Adicionar")
        if submitted and territory_id and territory_description and region_id:
            create_territory(territory_id, territory_description, region_id)

# Ler territórios
elif choice == "Ler":
    st.subheader("Lista de Territórios")
    territories = read_territories()
    if territories:
        for territory in territories:
            st.write(f"🆔 {territory[0]} | 🌍 {territory[1]} | 📌 Região ID: {territory[2]}")
    else:
        st.info("Nenhum território encontrado.")

# Atualizar território
elif choice == "Atualizar":
    st.subheader("Atualizar Território")
    territories = read_territories()
    if territories:
        territory_ids = [territory[0] for territory in territories]
        selected_id = st.selectbox("Selecione o ID do Território", territory_ids)
        selected_territory = next((territory for territory in territories if territory[0] == selected_id), None)
        
        if selected_territory:
            with st.form("update_form"):
                new_description = st.text_input("Nova Descrição", value=selected_territory[1])
                new_region_id = st.number_input("Novo ID da Região", min_value=1, step=1, value=selected_territory[2])
                submitted = st.form_submit_button("Atualizar")
                if submitted and new_description and new_region_id:
                    update_territory(selected_id, new_description, new_region_id)

# Deletar território
elif choice == "Deletar":
    st.subheader("Deletar Território")
    territories = read_territories()
    if territories:
        territory_ids = [territory[0] for territory in territories]
        selected_id = st.selectbox("Selecione o ID do Território para Deletar", territory_ids)
        if selected_id and st.button("Deletar"):
            delete_territory(selected_id)
    else:
        st.info("Nenhum território disponível para deletar.")