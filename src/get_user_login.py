# =================================== #
# Validates user login and redirects
# traffic accordingly
#
# By Eliot Raynor 12/01/25
# =================================== #

from hashlib import sha256
import sqlite3

def get_user_login(user, password, login_mode):

    # Find user in database and retrieve login value
    conn = sqlite3.connect("NWI_DB.db")
    db = conn.cursor()
    db.execute('SELECT password, id FROM %s WHERE username="%s"' %(login_mode, user))
    try:
        try_user = db.fetchall()[0]
        correct_code = try_user[0]
        user_id = try_user[1]
    except:
        # Reload login page w/ error: wrong username
        return 0, ""
    conn.close()

    # Check if the login is valid
    login_val = user.encode('utf-8') + password.encode('utf-8')
    attempt_code = sha256(login_val).hexdigest()

    if correct_code == attempt_code:
        # Load user home page
        if login_mode == "patients":
            return 1, user_id
        else:
            return 2, user_id
    else:
        # Reload login page w/ error: wrong password
        return 3, ""