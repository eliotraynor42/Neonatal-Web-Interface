#Author: Alex Vogel

#Returns all new notifications for a specific doctor.
#This would be used in the Question portal for the Doctor
#to show unread notifications for the doctor.

import sqlite3
import sys
import json

def get_doctor_notif(doctor_id):
    conn = sqlite3.connect("patient_database.db")
    cur = conn.cursor()

    # Selection statement to obtain new notifications for this doctor.
    sql = """
        SELECT notif_id, doctor_id, message, date, is_read
        FROM doctor_notifications
        WHERE doctor_id = ? AND is_read = 0
        ORDER BY date DESC
    """
    
    # Run the SQL query and get the results.
    cur.execute(sql, (doctor_id,))
    rows = cur.fetchall()
    conn.close()
    
    # Building dictionary from retrieved data.
    notifications = [
        {
            "notif_id": r[0],
            "doctor_id": r[1],
            "message": r[2],
            "date": r[3],
            "is_read": r[4],
        }
        for r in rows
    ]

    return {"notifications": notifications}

#Next the function return needs to be turned into a command‑line script that can be called from 
#a PHP script. Since PHP does not understand Python dict data types, the Python return needs
#to be converted into a JSON which is a standardized format that can be decoded
#with PHP for a html script. 
if __name__ == "__main__":
    #checks whether the file is being run as a script
    doctor_id = sys.argv[1]
    result = get_doctor_notif(doctor_id)
    print(json.dumps(result))
    #shell_exec() in PHP can capture the printed text as a string. 