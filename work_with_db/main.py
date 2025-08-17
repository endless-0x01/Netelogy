from typing import Optional
import psycopg2
from psycopg2.extensions import connection, cursor


def create_db(conn: connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );"""
        )

        cur.execute(
            '''CREATE TABLE IF NOT EXISTS phone(
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
                phone VARCHAR(20) UNIQUE
            );'''
        )
        conn.commit()

def add_client(conn: connection, first_name: str, last_name: str, email: str, phones=None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO clients (first_name, last_name, email) VALUES
                (%s, %s, %s) RETURNING client_id;
            ''', (first_name, last_name, email)
        )
        client_id = cur.fetchone()[0]

        if phones:
            for phone in phones:
                cur.execute(
                    '''
                        INSERT INTO phone(client_id, phone) VALUES
                        (%s, %s);
                    ''', (client_id, phone)
                )

        conn.commit()


        print(f'Клиент {first_name} {last_name} добавлен , ID клиента {client_id}')

def add_phone(conn: connection, client_id, phone: list)-> None:
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO phone(client_id, phone) VALUES
            (%s, %s);
            ''', (client_id, phone)
        )
        conn.commit()


def change_client(conn: connection, client_id, first_name=None, last_name=None, email=None, phone=None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            '''
            UPDATE clients SET first_name = %s, last_name = %s, email = %s WHERE client_id = %s;
            ''', (first_name, last_name, email, client_id)
        )
        conn.commit()
        
        if phone:
            cur.execute(
                '''
                UPDATE phone SET phone = %s WHERE client_id = %s;
                ''', (phone, client_id)
            )
        conn.commit()
        
        print(f'Клиент {first_name} {last_name} изменен, ID клиента {client_id}')

def main():
    with psycopg2.connect(
        database="netology_db", user="postgres", password="1234", client_encoding="utf8"
    ) as conn:
        # create_db(conn)
        # add_client(conn, 'Gleb', 'Testovich', 'gleb_test@mail.ru')
        # add_client(conn, 'Alesia', 'Testovicha', 'alesia_test@mail.ru', ['89997271122'])
        # add_client(conn, 'Test', 'Testovik', 'testovik_test@mail.ru', ['8921743231', '89234382131', '8921843231'])
        # add_phone(conn, 1, '89116567372')
        change_client(conn, 1, 'Gleb', 'Testovich', 'gleb_test@mail.ru', '89116567372')

if __name__ == "__main__":
    main()
