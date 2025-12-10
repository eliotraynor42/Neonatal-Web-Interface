# =================================== #
# Returns data from health tracker to database
# 
# By Alexandra Nickel 12/08/25
# =================================== #
import sqlite3
from datetime import datetime,date
from bmes_ahmet_loader import *

def submit_patient_data(patient_id,vals):
    # Connect to the database
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    db = conn.cursor()


    reference = ['weight_kg', 'length_cm', 'head_circumference_cm', 'temperature_c', 'heart_rate_bpm', 
                    'respiratory_rate_bpm', 'oxygen_saturation', 'feeding_frequency_per_day', 
                    'urination_count_per_day', 'stool_count_per_day']
    
    data=conn.execute(f"SELECT * FROM patients WHERE patients.id={patient_id};").fetchone()

      # I want the 5th column of the database not the ID column
    birthdate=datetime.strptime(data[5],"%Y/%m/%d").date() #Takes the birth date and turns it into a format python can use
    today=date.today() #Gets todays date
    new_age=(today-birthdate).days #Gets the age in days of the patient


   #Add data to Patient Visit data
    call="INSERT INTO patient_visit_data(id_patient, age_days,"
    for i in range(len(reference)-1):
        call +=reference[i] + ", "
    
    call +=reference[9] +") VALUES (" +str(patient_id) +", " +str(new_age) +", "
    for i in range(len(vals)-1):
        call +=str(vals[i]) +" ,"
    
    call += str(vals[9]) +");"

    conn.execute(call)
    conn.close()