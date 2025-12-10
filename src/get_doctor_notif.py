#Author: Alex Vogel

#Returns all new notifications for a specific doctor that have not been read.
#This would be used in the Question portal for the Doctor
#to show unread notifications for the doctor.

import sqlite3
import sys
import json
from bmes_ahmet_loader import *

#Retrieving information from the database can be done through SQL queries by
#connecting to the database with the sqlite3 package. 
def get_doctor_notif(id_doctor):
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    cur = conn.cursor()

    # Selection statement to obtain new notifications for this doctor.
    sql = """
        SELECT id_doctor, message, date, id_patient
        FROM comms
        WHERE id_doctor = ?
        ORDER BY date DESC
    """
    
    # Run the SQL query and get the results.
    cur.execute(sql, (id_doctor))
    rows = cur.fetchall()
    conn.close()
    
    # Building dictionary from retrieved data.
    notifications = [
        {
            "id_doctor": r[0],
            "message": r[1],
            "date": r[2],
            "id_patient": r[3],
        }
        for r in rows
    ]

    return notifications

print(get_doctor_notif("1"))

#Next the function return needs to be turned into a command‑line script that can be called from 
#a PHP script. Since PHP does not understand Python dict data types, the Python return needs
#to be converted into a JSON which is a standardized format that can be decoded
#with PHP for a html script. 
# if __name__ == "__main__":
#     #checks whether the file is being run as a script
#     id_doctor = sys.argv[1]
#     result = get_doctor_notif(id_doctor)
#     print(json.dumps(result))
#     #shell_exec() in PHP can capture the printed text as a string. 