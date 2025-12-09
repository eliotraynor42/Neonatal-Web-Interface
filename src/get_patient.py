# Author: Alex Vogel

# Returns patient information for the Doctor View Patient webpage.

import sqlite3
import sys
import json

def get_patient(patient_id):
    conn = sqlite3.connect("NWI_DB.db")
    cur = conn.cursor()

    # Selection statement to obtain patient information from the database.
    sql = """
        SELECT name, birth, id, gender, birth_weight_kg, birth_length_cm, birth_head_circumference_cm, id_doctor
        FROM patients
        WHERE id = ?
    """
    
    # Run the SQL query and get the result.
    cur.execute(sql, (patient_id))
    row = cur.fetchone()
    conn.close()
    
    # Return the patient data as a dictionary if found.
    if row:
        patient = {
            "Name": row[0],
            "Birthday": row[1],
            "ID": row[2],
            "Gender": row[3],
            "Birth_Weight": row[4],
            "Birth_Length": row[5],
            "Birth_Head_Circum": row[6],
            "Doctor": row[7],
        }
        return patient

#Next the function return needs to be turned into a command‑line script that can be called from 
#a PHP script. Since PHP does not understand Python dict data types, the Python return needs
#to be converted into a JSON which is a standardized format that can be decoded
#with PHP for a html script. 
if __name__ == "__main__":
    #checks whether the file is being run as a script
    patient_id = sys.argv[1]
    result = get_patient(patient_id)
    print(json.dumps(result))
    #shell_exec() in PHP can capture the printed text as a string. 