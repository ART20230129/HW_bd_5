import psycopg2


def create_db(conn):
    ''' 1. Функция, создающая структуру БД (таблицы)'''
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE  number_telefon, customer_data CASCADE;
    """)
# Создание таблицы с даными клиента

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_data(
        client_id INTEGER UNIQUE PRIMARY KEY,
        client_name VARCHAR(35) NOT NULL,
        client_last_name VARCHAR(35) NOT NULL,
        client_email VARCHAR(35) NOT NULL
    );
    """)

# Создание таблицы с номерами телефонов клиентов

    cur.execute("""
    CREATE TABLE IF NOT EXISTS number_telefon(
        number_tel_id SERIAL PRIMARY KEY,
        client_phonenumber VARCHAR(15),
        client_id INTEGER REFERENCES customer_data(client_id)
    );
    """)

def add_client(conn, client_id, client_name, client_last_name, client_email, phones=None):
    ''' 2. Функция, позволяющая добавить нового клиента '''

# Добавляем данные клиента

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customer_data(client_id, client_name, client_last_name, client_email)
            VALUES(%s, %s, %s, %s);
    """, (client_id, client_name, client_last_name, client_email))
    conn.commit()

##    cur.execute("""
##        SELECT * FROM customer_data;
##    """)
##    print(cur.fetchall())


# Добавляем телефонный номер клиента

    cur.execute("""
        INSERT INTO number_telefon(client_phonenumber, client_id) VALUES(%s, %s);
    """, (phones, client_id))
    conn.commit()

##    cur.execute("""
##        SELECT * FROM number_telefon;
##    """)
##    print(cur.fetchall())


def add_phone(conn, client_id, phone):
    ''' 3. Функция, позволяющая добавить телефон для существующего клиента '''
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO number_telefon(client_id, client_phonenumber) VALUES(%s, %s);
    """, (client_id, phone))
    conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    ''' 4. Функция, позволяющая изменить данные о клиенте '''

# Меняем данные клиента
    cur = conn.cursor()
    cur.execute("""
        UPDATE customer_data SET client_name=%s, client_last_name=%s, client_email=%s WHERE client_id=%s;
    """, (first_name, last_name, email, client_id,))
    conn.commit()

# меняем телефон клиента
    cur = conn.cursor()
    cur.execute("""
        UPDATE number_telefon SET client_phonenumber=%s WHERE client_id=%s;
    """, (phones, client_id,))
    conn.commit()

def delete_phone(conn, client_id, phone):
    '''5. Функция, позволяющая удалить телефон для существующего клиента '''
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM number_telefon WHERE client_id=%s AND client_phonenumber=%s;
    """, (client_id, phone))
    conn.commit()


def delete_client(conn, client_id):
    '''6. Функция, позволяющая удалить существующего клиента '''
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM number_telefon WHERE client_id=%s;
    """, (client_id,))
    conn.commit()

    cur.execute("""
        DELETE FROM customer_data WHERE client_id=%s;
    """, (client_id,))
    conn.commit()

def find_client(conn):
    '''7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону. '''
    while True:
        input_number = input("Введите комманду для поиска клиента: \n"
                            " 1 - имя клиента, 2 - фамилия клиента, 3 - email, 4 - номер телефона \n"
                            " q - выход \n")
        print()
        if input_number == '1':
            input_name = input("Введите имя клиента\n ")
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM customer_data cd
                JOIN number_telefon nt ON cd.client_id=nt.client_id
                WHERE client_name=%s;
            """, (input_name,))
            print(cur.fetchall())
            print()

        elif input_number == '2':
            input_last_name = input("Введите фамилию клиента\n ")
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM customer_data cd
                JOIN number_telefon nt ON cd.client_id=nt.client_id
                WHERE client_last_name=%s;
            """, (input_last_name,))
            print(cur.fetchall())
            print()

        elif input_number == '3':
            input_client_email = input("Введите email клиента\n ")
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM customer_data cd
                JOIN number_telefon nt ON cd.client_id=nt.client_id
                WHERE client_email=%s;
            """, (input_client_email,))
            print(cur.fetchall())
            print()

        elif input_number == '4':
            input_client_phonenumber = input("Введите номер телефона клиента\n ")
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM customer_data cd
                JOIN number_telefon nt ON cd.client_id=nt.client_id
                WHERE client_phonenumber=%s;
            """, (input_client_phonenumber,))
            print(cur.fetchall())
            print()

        elif input_number == "q":
            print("До свидания!")
            print()
            break

        else:
            print('Неверная команда, введите от 1 до 4\n')
            continue




with psycopg2.connect(database="test7", user="postgres", password="password") as conn:
    create_db(conn)
    add_client(conn, 1, 'Иван', 'Иванов', 'wert@mm.com', '89998887766')
    add_client(conn, 2, 'Петр', 'Петров', 'wart@mm.com', '89998887755')
    add_client(conn, 3, 'Сидор', 'Сидоров', 'wуrt@mm.com', '89998887744')
    add_client(conn, 4, 'Буратино', 'Карлович', 'bur@bb.com' )
    add_client(conn, 5, 'Карабас', 'Барабас', 'karbar@bb.com', '89993222233' )
    add_phone(conn, 3, "89998887711")
    add_phone(conn, 3, "89998887722")
    add_phone(conn, 4, "89998887700")
    change_client(conn, 1, 'Ив', 'Монтан', 'ivaa@iv.com', '89997775533')
    delete_phone(conn, 3, '89998887711')
    delete_client(conn, 2)
    find_client(conn)

conn.close