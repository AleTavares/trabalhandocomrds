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

# Funções para interagir com a tabela order_details
def create_order_detail(order_id, product_id, unit_price, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount) VALUES (%s, %s, %s, %s, %s)",
        (order_id, product_id, unit_price, quantity, discount)
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
        "UPDATE order_details SET unit_price = %s, quantity = %s, discount = %s WHERE order_id = %s AND product_id = %s",
        (unit_price, quantity, discount, order_id, product_id)
    )
    conn.commit()
    conn.close()

def delete_order_detail(order_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM order_details WHERE order_id = %s AND product_id = %s", 
        (order_id, product_id)
    )
    conn.commit()
    conn.close()
