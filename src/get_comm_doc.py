#Author: Alex Vogel

#Returns all past communications between doctor and the specific patient.
#This would be done by retrieving data from the patient database and
#returning a data structure that can then by used by the Patient Communications 
#webpage. 

import sqlite3
import sys
import json

#Retrieving information from the database can be done through SQL queries by
#connecting to the database with the sqlite3 package. 
def get_comm_doc(id_patient):
    conn = sqlite3.connect("NWI_DB.db")
    cur = conn.cursor()

    #Selection statement to obtain communications from the patient database.
    sql = """
        SELECT id_doctor, id_patient, date, message
        FROM comms
        WHERE id_patient = ?
        ORDER BY date DESC
    """
    
    #Run the SQL query and get the results.
    cur.execute(sql, (id_patient))
    rows = cur.fetchall()
    conn.close()
    
    #Building dictionary from retrieved data. 
    communications = [
        {
            "id_doctor": r[0],
            "id_patient": r[1],
            "date": r[2],
            "message": r[3],
        }
        for r in rows
    ]

    return communications

print(get_comm_doc('0'))
    
#Next the function return needs to be turned into a command‑line script that can be called from 
#a PHP script. Since PHP does not understand Python dict data types, the Python return needs
#to be converted into a JSON which is a standardized format that can be decoded
#with PHP for a html script.  
# if __name__ == "__main__":
#     #checks whether the file is being run as a script
#     id_patient = sys.argv[1]
#     result = get_comm_doc(id_patient)
#     print(json.dumps(result))
#     #shell_exec() in PHP can capture the printed text as a string. 