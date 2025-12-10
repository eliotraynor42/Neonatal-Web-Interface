# =================================== #
# Returns data from health tracker to database
# 
# By Alexandra Nickel 12/08/25
# =================================== #

#==========Import Libraries==========#
import sqlite3
import datetime
from bmes_ahmet_loader import *

#===========Submit Patient Function==========#
def submit_patient_data(patient_id,vals):
    # Connect to the database
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    db = conn.cursor()

    #Reference variables for calling database
    reference = ['weight_kg', 'length_cm', 'head_circumference_cm', 'temperature_c', 'heart_rate_bpm', 
                    'respiratory_rate_bpm', 'oxygen_saturation', 'feeding_frequency_per_day', 
                    'urination_count_per_day', 'stool_count_per_day']
    
    data=conn.execute(f"SELECT * FROM patients WHERE patients.id={patient_id};").fetchone()

    #Gets the new age in days
    birthdate=datetime.date.fromisoformat(data[5]) #Takes the birth date and turns from text into a format a date object
    today=datetime.date.today() #Gets todays date
    new_age=(today-birthdate).days #Gets the age in days of the patient


   #==========Update Patient Data==========#
    call="INSERT INTO patient_visit_data(id_patient, age_days," #First part of the call
    for i in range(len(reference)-1): #Function makes the iteative part of the call
        call +=reference[i] + ", "
    
    call +=reference[9] +") VALUES (" +str(patient_id) +", " +str(new_age) +", "
    for i in range(len(vals)-1):
        call +=str(vals[i]) +" ,"
    
    call += str(vals[9]) +");"

    conn.execute(call)
    conn.close()