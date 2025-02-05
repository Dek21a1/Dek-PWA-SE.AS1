import sqlite3 as sql
import sanitise_verify as sv



def insert_details(username, email, password):
    encode_password = sv.check_PSWRD(password)
    encrypted_password = sv.encrypt_PSWRD(encode_password)
    if sv.check_identical(encode_password, encrypted_password):
        quickcon("commit", 'user_info', 'INSERT INTO users (username,email,password) VALUES (?,?,?)', (username,email,encrypted_password))
        return True
    else:
        return "Password does not match"


def retrieve_details(email, password):
    encode_password = sv.check_PSWRD(password)
    details = quickcon("fetchone", 'user_info', 'SELECT password FROM users WHERE email=(?)', (email,))
    for detail in details:
        if sv.check_identical(encode_password, detail):
            return True
        else:
            return False
        

def get_user(email):
    details = quickcon("fetchone", 'user_info', 'SELECT username FROM users WHERE email=(?)', (email,))
    return details[0]

def get_log(team):
    if team == None:
        return False
    else:
        for a in team:
            devlog = quickcon("fetchall", 'log_data', 'SELECT id, timestamp, log_info, log_title, log_subtitle FROM devlog WHERE team=(?)', (a,))
        return devlog

def get_teams(user):
    teams = quickcon("fetchall", 'teams', 'SELECT team FROM teams WHERE users=(?)', (user,))
    for team in teams:
        return team
    
def update_session(email, secret_key):
    quickcon("commit", 'user_info', 'UPDATE users SET current_session=(?) WHERE email=(?)', (secret_key, email))

def reset_session(email):
    quickcon("commit", 'user_info', 'UPDATE users SET current_session=(?) WHERE email=(?)', ('no data', email))

def perm_level(email):
    level = quickcon("fetchall", 'teams', 'SELECT clearance, team FROM teams WHERE users=(?)', (email,))
    return level



def quickcon(type, db, command, var):
    if type == 'fetchone':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        val = cur.execute(f"{command}",(var)).fetchone()
        con.close()
        return val
    elif type == 'fetchall':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        val = cur.execute(f"{command}",(var)).fetchall()
        con.close()
        return val
    elif type == 'commit':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        cur.execute(f"{command}",(var))
        con.commit()
        con.close()