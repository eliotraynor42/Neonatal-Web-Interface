# Author: Alex Vogel

# Returns patient information for the Doctor View Patient webpage.

import sqlite3
import sys
import json

def get_patient(patient_id):
    conn = sqlite3.connect("patient_database.db")
    cur = conn.cursor()

    temp = {"patient_id": patient_id,
            "name": "john doe",
            "dob": "01/11/12"}
    return temp

    # Selection statement to obtain patient information from the database.
    sql = """
        SELECT patient_id, name, dob, age, length, length_percentile, weight, 
               weight_percentile, head_circumference, head_circumference_percentile, 
               diet, allergies, medications, immunizations, current_issues, other_notes
        FROM patients
        WHERE patient_id = ?
    """
    
    # Run the SQL query and get the result.
    cur.execute(sql, (patient_id,))
    row = cur.fetchone()
    conn.close()
    
    # Return the patient data as a dictionary if found.
    if row:
        patient = {
            "patient_id": row[0],
            "name": row[1],
            "dob": row[2],
            "age": row[3],
            "length": row[4],
            "length_percentile": row[5],
            "weight": row[6],
            "weight_percentile": row[7],
            "head_circumference": row[8],
            "head_circumference_percentile": row[9],
            "diet": row[10],
            "allergies": row[11],
            "medications": row[12],
            "immunizations": row[13],
            "current_issues": row[14],
            "other_notes": row[15],
        }
        return {"patient": patient}

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