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
            """CREATE TABLE IF NOT EXISTS phone(
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
                phone VARCHAR(20) UNIQUE
            );"""
        )
        conn.commit()


def add_client(
    conn: connection, first_name: str, last_name: str, email: str, phones=None
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO clients (first_name, last_name, email) VALUES
                (%s, %s, %s) RETURNING client_id;
            """,
            (first_name, last_name, email),
        )
        client_id = cur.fetchone()[0]

        if phones:
            for phone in phones:
                cur.execute(
                    """
                        INSERT INTO phone(client_id, phone) VALUES
                        (%s, %s);
                    """,
                    (client_id, phone),
                )

        conn.commit()

        print(f"Клиент {first_name} {last_name} добавлен , ID клиента {client_id}")


def add_phone(conn: connection, client_id: int, phone: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO phone(client_id, phone) VALUES
            (%s, %s);
            """,
            (client_id, phone),
        )
        conn.commit()
        print(f"Телефон {phone} добавлен для клиента {client_id}")


def add_phones(conn: connection, client_id: int, phones: list) -> None:
    with conn.cursor() as cur:

        if phones:
            for phone in phones:
                cur.execute(
                    """
                    INSERT INTO phone(client_id, phone) VALUES (%s, %s);
                    """,
                    (client_id, phone),
                )
                print(f"Телефон {phone} добавлен для клиента {client_id}")
            conn.commit()
        else:
            print(f"Для клиента {client_id} нет телефонов")


def change_client(
    conn: connection,
    client_id,
    first_name=None,
    last_name=None,
    email=None,
    phones=None,
    replace_phone=False,
) -> None:
    with conn.cursor() as cur:
        # Обновляем основные данные клиента
        cur.execute(
            """
            UPDATE clients SET first_name = %s, last_name = %s, email = %s WHERE client_id = %s;
            """,
            (first_name, last_name, email, client_id),
        )

        if phones:
            if replace_phone:
                cur.execute("""DELETE FROM phone WHERE client_id = %s;""", (client_id,))
                print(f"Телефоны клиента {client_id} удалены")

            for phone in phones:
                cur.execute(
                    """INSERT INTO phone(client_id, phone) VALUES (%s, %s);""",
                    (client_id, phone),
                )
                print(f"Телефон {phone} добавлен для клиента {client_id}")

        conn.commit()
        print(f"Клиент {first_name} {last_name} изменен, ID клиента {client_id}")


def delete_phone(conn: connection, client_id: int, phone: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM phone WHERE client_id=%s AND phone=%s; 
            """,
            (client_id, phone),
        )
        conn.commit()
        print(f"Телефон {phone} удален")


def delete_client(conn: connection, client_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phone WHERE client_id=%s;""", (client_id,))
        cur.execute("""DELETE FROM clients WHERE client_id=%s;""", (client_id,))
        conn.commit()
        print(f"Клиент {client_id} удален")


def find_client(
    conn: connection,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    phone: str = None,
) -> None:
    with conn.cursor() as cur:
        query = """
        SELECT DISTINCT c.client_id, c.first_name, c.last_name, c.email, 
                STRING_AGG(p.phone, ',') as phones
        FROM clients c
        LEFT JOIN phone p ON c.client_id = p.client_id
        WHERE 1=1
        """

        params = []

        if first_name:
            query += "AND c.first_name ILIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            query += "AND c.last_name ILIKE %s"
            params.append(f"%{last_name}%")
        if email:
            query += "AND c.email ILIKE %s"
            params.append(f"%{email}%")
        if phone:
            query += "AND p.phone ILIKE %s"
            params.append(f"%{phone}%")

        query += "GROUP BY c.client_id, c.first_name, c.last_name, c.email"

        cur.execute(query, params)
        results = cur.fetchall()

        if results:
            print(f"Найдено клиентов: {len(results)}")
            for result in results:
                print(
                    f"ID: {result[0]}, Имя: {result[1]}, Фамилия: {result[2]}, Email: {result[3]}, Телефоны: {result[4]}"
                )
        else:
            print("Клиенты не найдены")


def main():
    with psycopg2.connect(
        database="netology_db", user="postgres", password="1234", client_encoding="utf8"
    ) as conn:
        # create_db(conn)
        # add_client(conn, 'Gleb', 'Testovich', 'gleb_test@mail.ru')
        # add_client(conn, 'Alesia', 'Testovicha', 'alesia_test@mail.ru', ['89997271122'])
        # add_client(conn, 'Test', 'Testovik', 'testovik_test@mail.ru', ['8921743231', '89234382131', '8921843231'])
        # add_phone(conn, 1, '89116567372')
        # change_client(conn, 1, 'Gleb', 'Testovich', 'gleb_test@mail.ru', ['89116567372'], replace_phone=True)
        # delete_client(conn, 1)
        # delete_phone(conn, 1, '89116567372')
        find_client(conn, "Alesia", "Testovich", "alesia_test@mail.ru", "89997271122")


if __name__ == "__main__":
    main()
