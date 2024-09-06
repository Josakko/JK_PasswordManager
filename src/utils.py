from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib
import os

#!######### VERSION #########!#
VERSION = "v7.0.0"
#!######### VERSION #########!#


PROTOCOL = "https://"
GITHUB_API_DOMAIN = "api.github.com/"
GITHUB_REPO = "Josakko/JK_PasswordManager/"
GITHUB_RELEASE_API = PROTOCOL + GITHUB_API_DOMAIN + "repos/" + GITHUB_REPO + "releases/latest"

DB_FILE = "password_vault.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT,
    user_name TEXT,
    password TEXT,
    time TEXT NOT NULL,  -- DATETIME DEFAULT CURRENT_TIMESTAMP
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

"""


def hash(string: str, salt: str="") -> str:
    data = string.encode() + salt.encode()

    algorithm = hashlib.sha512()
    algorithm.update(data)
    return algorithm.hexdigest()


def generate_key_with_password(password: str, username: str) -> str:
    salt = base64.urlsafe_b64encode(f"{password}{username}".encode())

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def generate_key(string: str, salt: str="") -> str:
    salt = base64.urlsafe_b64encode(salt.encode())

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )

    return base64.urlsafe_b64encode(kdf.derive(string.encode()))


def encrypt(data: str, f: Fernet) -> str:
    return f.encrypt(data.encode()).decode()


def encrypt_key(data: str, key: str) -> str:
    return Fernet(key).encrypt(data.encode()).decode()


def decrypt(data: str, f: Fernet) -> str:
    return f.decrypt(data.encode()).decode()


def decrypt_key(data: str, key: str) -> str:
    return Fernet(key).decrypt(data.encode()).decode()


def decrypt_credentials(encrypted_data, f):
    data = []
    for row in encrypted_data:
        platform_decrypted = decrypt(row[1], f)
        username_decrypted = decrypt(row[2], f)
        password_decrypted = decrypt(row[3], f)
        decrypted_data = row[:1] + (platform_decrypted, username_decrypted, password_decrypted,) + row[4:]
        data.append(decrypted_data)

    return data


def get_key_from_fernet(f: Fernet):
    return base64.urlsafe_b64encode(f._signing_key + f._encryption_key).decode()


# major.minor.revision.stream (optional, if not set defaults to Release)
def parse_version(version: str):
    segments = version.strip("v").split(".", 4)

    tmp = []
    for i in segments:
        try:
            tmp.append(int(i))
        except ValueError:
            tmp.append(i)

    segments = tmp

    if len(segments) < 3:
        while len(segments) != 3:
            segments.append(0)

    if len(segments) == 3:
        segments.append("Release")

    return segments


