import sqlite3 as sql
import sanitise_verify as sv



def insert_details(username, email, password):
    encode_password = sv.check_PSWRD(password)
    encrypted_password = sv.encrypt_PSWRD(encode_password)
    if sv.check_identical(encode_password, encrypted_password):
        con = sql.connect(".database/user_info.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)",(username,email,encrypted_password))
        con.commit()
        con.close()
        return True
    else:
        return "Password does not match"


def retrieve_details(email, password):
    encode_password = sv.check_PSWRD(password)
    con = sql.connect(".database/user_info.db")
    cur = con.cursor()
    details = cur.execute("SELECT password FROM users WHERE email=(?)",(email,)).fetchone()
    con.close()
    for detail in details:
        if sv.check_identical(encode_password, detail):
            return True
        else:
            return False