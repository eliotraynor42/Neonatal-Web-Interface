# =================================== #
# Gets all patients for doctor
#
# By Eliot Raynor 12/10/25
# =================================== #

import sqlite3
from bmes_ahmet_loader import *

def get_patient_list(user_id):

    # Find user in database and retrieve values
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    db = conn.cursor()
    db.execute('SELECT id, name FROM patients WHERE id_doctor="%s"' %(user_id))
    rows = db.fetchall()
    
    # Create output
    patients = [
        {
            "id": r[0],
            "name": r[1],
        }
        for r in rows
    ]
    conn.close()
    return patients