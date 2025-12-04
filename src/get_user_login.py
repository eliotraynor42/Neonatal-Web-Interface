# =================================== #
# Validates user login and redirects
# traffic accordingly
#
# By Eliot Raynor 12/01/25
# =================================== #

from hashlib import sha256
import sqlite3

def get_user_login(user, password, login_mode):
    print("Hello World")

    return 3, "" # TEMP

    # Find user in database and retrieve login value
    conn = sqlite3.connect("patient_database.sql") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    db = conn.cursor()
    db.execute('SELECT secure, id FROM %s WHERE username=%s' %(login_mode, user))
    try:
        correct_code = db.fetchall()[0][0]
        user_id = db.fetchall()[0][1]
    except:
        # Reload login page w/ error: wrong username
        return 0, ""
    conn.close()

    # Check if the login is valid
    login_val = user.encode('utf-8') + password.encode('utf-8')
    attempt_code = sha256(login_val).hexdigest()

    if correct_code == attempt_code:
        # Load user home page
        if login_mode == "doctor":
            return 1, user_id
        else:
            return 2, user_id
    else:
        # Reload login page w/ error: wrong password
        return 3, ""