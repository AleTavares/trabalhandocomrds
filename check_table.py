import psycopg2
import yaml

def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

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

def check_table_structure():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar a estrutura da tabela categories
        cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'categories'
        ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print("Estrutura da tabela 'categories':")
        for column in columns:
            print(f"Coluna: {column[0]}, Tipo: {column[1]}, Nullable: {column[2]}, Default: {column[3]}")
        
        # Verificar se há sequência associada à tabela
        cursor.execute("""
        SELECT pg_get_serial_sequence('categories', 'category_id');
        """)
        sequence = cursor.fetchone()
        print(f"\nSequência para category_id: {sequence[0] if sequence[0] else 'Nenhuma'}")
        
    except Exception as e:
        print(f"Erro ao verificar a estrutura da tabela: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_table_structure()