import re
import html
import bcrypt

def check_PSWRD(password: str)  -> bytes:
    if not issubclass(type(password), str):
        raise TypeError("expected string")
    if len(password) < 6:
        raise ValueError("too short, below 6 characters")
    if not len(re.findall(r"[a-z]", password) + re.findall(r"[A-Z]", password)) >= 1:
        raise ValueError("incorrect amount of alpha characters")
    if not len(re.findall(r"[0-9]", password)) >= 1:
        raise ValueError("incorrect amount of numeric characters")
    return password.encode()


def encrypt_PSWRD(enc_password: bytes) -> bytes:
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(enc_password, salt)
    return encrypted_password

def check_identical(password: bytes, encrypted_password: bytes) -> bool:
    return bcrypt.checkpw(password, encrypted_password)