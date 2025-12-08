# Author: Alex Vogel

# Returns patient information for the Doctor View Patient webpage.

import sqlite3
import sys
import json

#Retrieving information from the database can be done through SQL queries by
#connecting to the database with the sqlite3 package. 
def get_patient(id_patient):
    conn = sqlite3.connect("patient_database.db")
    cur = conn.cursor()

    # Selection statement to obtain baby information from the database.
    sql = """
        SELECT id_patient, name, gender, gestational_age_weeks,
               birth_weight_kg, birth_length_cm, birth_head_circumference_cm,
               date, age_days, weight_kg, length_cm, head_circumference_cm,
               temperature_c, heart_rate_bpm, respiratory_rate_bpm,
               oxygen_saturation, feeding_type, feeding_frequency_per_day,
               urine_output_count, stool_count, jaundice_level_mg_dl,
               apgar_score, immunizations_done, reflexes_normal, risk_level
        FROM Neonatal_Sample_Dataset
        WHERE id_patient = ?
    """

    # Run the SQL query and get the result.
    cur.execute(sql, (id_patient,))
    row = cur.fetchone()
    conn.close()

    # Return the baby data as a dictionary if found.
    if row:
        baby = {
            "id_patient": row[0],
            "name": row[1],
            "gender": row[2],
            "gestational_age_weeks": row[3],
            "birth_weight_kg": row[4],
            "birth_length_cm": row[5],
            "birth_head_circumference_cm": row[6],
            "date": row[7],
            "age_days": row[8],
            "weight_kg": row[9],
            "length_cm": row[10],
            "head_circumference_cm": row[11],
            "temperature_c": row[12],
            "heart_rate_bpm": row[13],
            "respiratory_rate_bpm": row[14],
            "oxygen_saturation": row[15],
            "feeding_type": row[16],
            "feeding_frequency_per_day": row[17],
            "urine_output_count": row[18],
            "stool_count": row[19],
            "jaundice_level_mg_dl": row[20],
            "apgar_score": row[21],
            "immunizations_done": row[22],
            "reflexes_normal": row[23],
            "risk_level": row[24],
        }
        return {"baby": baby}

#Next the function return needs to be turned into a command‑line script that can be called from 
#a PHP script. Since PHP does not understand Python dict data types, the Python return needs
#to be converted into a JSON which is a standardized format that can be decoded
#with PHP for a html script. 
if __name__ == "__main__":
    #checks whether the file is being run as a script
    id_patient = sys.argv[1]
    result = get_patient(id_patient)
    print(json.dumps(result))
    #shell_exec() in PHP can capture the printed text as a string. 