import sqlite3
import cryptography.fernet as fernet


keyfile = "notes.txt"
try:
    with open(keyfile, "rb") as f:
        key = f.read()
except:
    key = fernet.Fernet.generate_key()
    with open(keyfile, "wb") as f:
        f.write(key)
f = fernet.Fernet(key)


def encrypt(string):
    return f.encrypt(string.encode()).decode()

    
def decrypt(string):
    return f.decrypt(string.encode()).decode()
    


def database():

    conn = sqlite3.connect("password_vault.db")

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id varchar PRIMARY KEY,
                    user_name text,  
                    password text
                    )""")

                    
    cursor.execute("""CREATE TABLE IF NOT EXISTS users_data(
                    id INTEGER PRIMARY KEY,
                    platform text,
                    user_name text,  
                    password text,
                    time text,
                    user_id varchar,
                    FOREIGN KEY (user_id) REFERENCES supplier_groups (user_id) 
                    )""")

    conn.commit()

    conn.close()

def sign_up(new_username, new_password):

    conn = sqlite3.connect("password_vault.db")
    
    cursor = conn.cursor()
    sql = "SELECT user_name FROM users WHERE user_name=?"
    result = cursor.execute(sql, (new_username,)).fetchone()
    if result:
        result = 0
    else:
        new_user_id = 'A1'
        sql = "SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1"
        last_id = cursor.execute(sql).fetchone()
        if last_id:
            last_row_id = last_id[0]
            char = ord(last_row_id[0])
            number = int(last_row_id[1:])
            if 0 < number < 100:
                number += 1
            else:
                number = 1
                if 64 < char < 91:
                    char += 1
                else:
                    char = 65
            new_user_id = chr(char) + str(number)
        data = [new_user_id, new_username, encrypt(new_password)]
        sql = """INSERT INTO users(user_id,user_name,password)
        VALUES (?,?,?)"""
        cursor.execute(sql, data)
        result = 1

    conn.commit()
    
    conn.close()
    return result


def login(username, password):
    conn = sqlite3.connect("password_vault.db")
    
    cursor = conn.cursor()
    query = "SELECT user_id,user_name,password FROM users WHERE user_name = ?"
    cursor.execute(query, (username,))
    request = cursor.fetchone()
    if request:
        if decrypt(request[2]) == password:
            user_id = request[0]
            query = "SELECT * FROM users_data WHERE user_id= ?"
            cursor.execute(query, (user_id,))
            data = cursor.fetchall()
            request = [request[0], request[1], data]
        else:
            request = 0
    else:
        request = 0

    conn.commit()
    
    conn.close()

    return request


def insert(data):
    platform = encrypt(data[0])
    print(platform)
    username = encrypt(data[1])
    password = encrypt(data[2])
    data.pop(0)
    data.insert(0, platform)
    data.pop(1)
    data.insert(1, username)
    data.pop(2)
    data.insert(2, password)
    
    conn = sqlite3.connect("password_vault.db")
    
    cursor = conn.cursor()
    sql = """INSERT INTO users_data(platform,user_name,password,time,user_id)
     VALUES (?,?,?,?,?)"""
    cursor.execute(sql, data)
    last_row_id = cursor.lastrowid

    conn.commit()

    conn.close()
    return last_row_id


def update(data):
    platform = encrypt(data[0])
    username = encrypt(data[1])
    password = encrypt(data[2])
    data.pop(0)
    data.insert(0, platform)
    data.pop(1)
    data.insert(1, username)
    data.pop(2)
    data.insert(2, password)
    
    conn = sqlite3.connect("password_vault.db")

    cursor = conn.cursor()
    sql = "UPDATE users_data SET platform=?,user_name=?,password=?,time=?,user_id=? WHERE id=?"
    cursor.execute(sql, data)

    conn.commit()

    conn.close()


def delete(row_id):
    conn = sqlite3.connect("password_vault.db")

    cursor = conn.cursor()
    sql = "DELETE FROM users_data WHERE id IN ({})".format(', '.join('?' * len(row_id)))
    cursor.execute(sql, row_id)

    conn.commit()

    conn.close()


def delete_user_data(user_id):
    conn = sqlite3.connect("password_vault.db")

    cursor = conn.cursor()
    sql = "DELETE FROM users_data WHERE user_id=?"
    cursor.execute(sql, (user_id,))

    conn.commit()

    conn.close()


def get_password(row_id, user_id):
    conn = sqlite3.connect("password_vault.db")

    cursor = conn.cursor()
    sql = "SELECT password FROM users_data WHERE id = ? AND user_id = ?"
    requested_password = cursor.execute(sql, (row_id, user_id)).fetchone()[0]

    conn.commit()

    conn.close()
    
    return decrypt(requested_password)
