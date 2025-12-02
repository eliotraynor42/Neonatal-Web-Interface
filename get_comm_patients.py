# Author: Alex Vogel

# Returns all past communications for a specific doctor.
# This would be used in the Doctor Communications webpage to show 
# all conversations the doctor has had with any patient.

import sqlite3
import sys
import json

def get_comm_patients(doctor_id):
    conn = sqlite3.connect("patient_database.db")
    cur = conn.cursor()

    # Selection statement to obtain all communications for this doctor.
    sql = """
        SELECT comm_id, doctor_id, patient_id, date, message
        FROM patient_communications
        WHERE doctor_id = ?
        ORDER BY date DESC
    """
    
    # Run the SQL query and get the results.
    cur.execute(sql, (doctor_id,))
    rows = cur.fetchall()
    conn.close()
    
    # Building dictionary from retrieved data.
    communications = [
        {
            "comm_id": r[0],
            "doctor_id": r[1],
            "patient_id": r[2],
            "date": r[3],
            "message": r[4],
        }
        for r in rows
    ]

    return {"communications": communications}

#Next the function return needs to be turned into a command‑line script that can be called from 
#a PHP script. Since PHP does not understand Python dict data types, the Python return needs
#to be converted into a JSON which is a standardized format that can be decoded
#with PHP for a html script. 
if __name__ == "__main__":
    #checks whether the file is being run as a script
    doctor_id = sys.argv[1]
    result = get_comm_patients(doctor_id)
    print(json.dumps(result))
    #shell_exec() in PHP can capture the printed text as a string. 