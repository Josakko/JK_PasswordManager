import sqlite3
from cryptography.fernet import Fernet
from utils import *

class Database:
    def __init__(self):
        self.db = sqlite3.connect(DB_FILE)
        self.f: Fernet = None

    def init_db(self):
        cursor = self.db.cursor()
        cursor.executescript(SCHEMA)

        self.db.commit()
        cursor.close()


    def sign_up(self, new_username, new_password):
        username = hash(new_username, new_username)

        cursor = self.db.cursor()
        user = cursor.execute("SELECT user_name FROM users WHERE user_name = ?", (username, )).fetchone()

        if user:
            result = False
        else:
            key = encrypt_key(Fernet.generate_key().decode(), generate_key_with_password(new_password, username))
            cursor.execute("INSERT INTO users(user_name, password) VALUES (?, ?)", (username, key))
            result = True

        self.db.commit()
        cursor.close()
        return result


    def login(self, username, password):
        cursor = self.db.cursor()

        username_hash = hash(username, username)
        password_key = generate_key_with_password(password, username_hash)
        password_f = Fernet(password_key)

        
        user = cursor.execute("SELECT * FROM users WHERE user_name = ?", (username_hash)).fetchall()

        if not user:
            return None
        
        try: key = decrypt(user[2], password_f)
        except: return False
        
        data = cursor.execute("SELECT * FROM users_data WHERE user_id = ?", (user[0], )).fetchall()
        cursor.close()
        
        return [user[0], username, data, Fernet(key)]


    def insert(self, data: list, f):
        platform = encrypt(data[0], f)
        username = encrypt(data[1], f)
        password = encrypt(data[2], f)
        data.pop(0)
        data.insert(0, platform)
        data.pop(1)
        data.insert(1, username)
        data.pop(2)
        data.insert(2, password)

        cursor = self.db.cursor()
        cursor.execute("INSERT INTO user_data(platform, user_name, password, time, user_id) VALUES (?, ?, ?, ?, ?)", data)
        last_row_id = cursor.lastrowid

        self.db.commit()
        cursor.close()
        return last_row_id # self.db.execute("SELECT last_insert_rowid()").fetchone()[0]


    def update(self, data, f):
        platform = encrypt(data[0], f)
        username = encrypt(data[1], f)
        password = encrypt(data[2], f)
        data.pop(0)
        data.insert(0, platform)
        data.pop(1)
        data.insert(1, username)
        data.pop(2)
        data.insert(2, password)
        


        cursor = self.db.cursor()
        sql = "UPDATE users_data SET platform=?,user_name=?,password=?,time=?,user_id=? WHERE id=?"
        cursor.execute("UPDATE users_data SET platform = ?, user_name = ?, password = ?, time = ?, user_id = ? WHERE id = ?", data)

        self.db.commit()
        cursor.close()


    def delete(self, row_id):
        cursor = self.db.cursor()

        sql = "DELETE FROM users_data WHERE id IN ({})".format(", ".join("?" * len(row_id)))
        cursor.execute(sql, row_id)

        self.db.commit()
        cursor.close()


    def delete_user_data(self, user_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM users_data WHERE user_id = ?", (user_id,))

        self.db.commit()
        cursor.close()


    def get_password(self, row_id, user_id, f):
        cursor = self.db.cursor()
        password = cursor.execute("SELECT password FROM users_data WHERE id = ? AND user_id = ?", (row_id, user_id)).fetchone()[0]

        cursor.close()
        return decrypt(password, f)

