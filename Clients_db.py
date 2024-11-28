import psycopg2
from config import host, database, user, password


conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

def create_database(conn):
    with conn.cursor() as cur:
        # Удаление таблиц для нового заполнения
        cur.execute("""
        DROP TABLE IF EXISTS phones;
        DROP TABLE IF EXISTS clients;
        """)

        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
        """)

        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id),
            phone_number VARCHAR(20)
        );
        """)
        
        conn.commit()


def add_client(first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING client_id",
                    (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        print(client_id)
        conn.commit()
        return client_id

def add_phone(client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones (client_id, phone_number) 
            VALUES (%s, %s);
        """, (client_id, phone))
        conn.commit()



def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id = %s AND phone_number = %s",
                    (client_id, phone_number))
        conn.commit()



def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM clients WHERE client_id = %s;", (client_id,))
        conn.commit()


def update_client(client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("UPDATE clients SET first_name = %s WHERE client_id = %s;", (first_name, client_id))
        if last_name:
            cur.execute("UPDATE clients SET last_name = %s WHERE client_id = %s;", (last_name, client_id))
        if email:
            cur.execute("UPDATE clients SET email = %s WHERE client_id = %s;", (email, client_id))
        conn.commit()


def find_client(first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM clients 
            WHERE first_name LIKE %s OR 
            last_name LIKE %s OR 
            email LIKE %s;
        """,(first_name,last_name,email))
        clients = cur.fetchall()
        return clients


def select(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT *
                    FROM clients;
                """)
        print(cur.fetchall())
