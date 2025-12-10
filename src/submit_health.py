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
    conn.cursor()

    #Reference variables for calling database
    reference = ['weight_kg', 'length_cm', 'head_circumference_cm', 'temperature_c', 'heart_rate_bpm', 
                    'respiratory_rate_bpm', 'oxygen_saturation', 'feeding_frequency_per_day', 
                    'urination_count_per_day', 'stool_count_per_day']
    
    data=conn.execute(f"SELECT * FROM patients WHERE patients.id={patient_id};").fetchone()

    #Gets the new age in days
    birthdate=datetime.date.fromisoformat(data[5]) #Takes the birth date and turns from text into a format a date object
    today=datetime.date.today() #Gets todays date
    age_days=(today-birthdate).days #Gets the age in days of the patient


   #==========Update Patient Data==========#
    conn.execute(f"""INSERT INTO patient_visit_data (
                    id_patient,
                    date,
                    age_days,
                    weight_kg,
                    length_cm,
                    head_circumference_cm,
                    temperature_c,
                    heart_rate_bpm,
                    respiratory_rate_bpm,
                    oxygen_saturation,
                    primary_feeding_type,
                    feeding_frequency_per_day,
                    urination_count_per_day,
                    stool_count_per_day
                    ) VALUES (
                    {patient_id},
                    '{today}',
                    {age_days},
                    {vals[0]},
                    {vals[1]},
                    {vals[2]},
                    {vals[3]},
                    {vals[4]},
                    {vals[5]},
                    {vals[6]},
                    {vals[7]},
                    {vals[8]},
                    {vals[9]}
                    );""")
    conn.close()