import sqlite3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64



def generate_key(password: str, username: str):
    salt = base64.urlsafe_b64encode(f"{password}{username}".encode())

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))



def encrypt(string: str, f: object=None, key: str=None) -> (str, Exception):
    if f: 
        return f.encrypt(string.encode()).decode()
    elif key: 
        return Fernet(key).encrypt(string.encode()).decode()
    else: 
        raise Exception("Key or Fernet instance is required")

    
def decrypt(string: str, f: object=None, key: str=None) -> (str, Exception):
    if f: 
        return f.decrypt(string.encode()).decode()
    elif key: 
        return Fernet(key).decrypt(string.encode()).decode()
    else: 
        raise Exception("Key or Fernet instance is required")



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
        new_user_id = "A1"
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

        key = encrypt(Fernet.generate_key().decode(), f=Fernet(generate_key(new_password, new_username)))

        data = [new_user_id, new_username, key]
        sql = """INSERT INTO users(user_id, user_name, password)
        VALUES (?, ?, ?)"""
        cursor.execute(sql, data)
        result = 1

    conn.commit()
    
    conn.close()
    return result


def login(username, password):
    password_key = generate_key(password, username)
    password_f = Fernet(password_key)

    conn = sqlite3.connect("password_vault.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    if not rows:
        return 0
    
    for row in rows:
        try: key = decrypt(row[2], f=password_f)
        except: continue
        
        user_id = row[0]
        cursor.execute("SELECT * FROM users_data WHERE user_id = ?", (user_id, ))
        data = cursor.fetchall()

        conn.commit()
        conn.close()

        #f = Fernet(key)

        return [row[0], row[1], data, Fernet(key)]


def insert(data, f):
    platform = encrypt(data[0], f)
    username = encrypt(data[1], f)
    password = encrypt(data[2], f)
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


def update(data, f):
    platform = encrypt(data[0], f)
    username = encrypt(data[1], f)
    password = encrypt(data[2], f)
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
    sql = "DELETE FROM users_data WHERE id IN ({})".format(", ".join("?" * len(row_id)))
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


def get_password(row_id, user_id, f):
    conn = sqlite3.connect("password_vault.db")

    cursor = conn.cursor()
    sql = "SELECT password FROM users_data WHERE id = ? AND user_id = ?"
    requested_password = cursor.execute(sql, (row_id, user_id)).fetchone()[0]

    conn.commit()

    conn.close()
    
    return decrypt(requested_password, f=f)
