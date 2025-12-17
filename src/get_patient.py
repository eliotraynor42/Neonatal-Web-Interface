# Author: Alex Vogel

# Returns patient information for the Doctor View Patient webpage.

import sqlite3
import sys
import json
from bmes_ahmet_loader import *

def get_patient(patient_id):
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    cur = conn.cursor()

    # Selection statement to obtain patient information from the database.
    sql = """
        SELECT name, birth, id, gender, birth_weight_kg, birth_length_cm, birth_head_circumference_cm, id_doctor
        FROM patients
        WHERE id = ?
    """
    
    # Run the SQL query and get the result.
    cur.execute(sql, (patient_id,))
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

# The following has been removed from the final instance
# if __name__ == "__main__":
#     #checks whether the file is being run as a script
#     patient_id = sys.argv[1]
#     result = get_patient(patient_id)
#     print(json.dumps(result))
#     #shell_exec() in PHP can capture the printed text as a string. 