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
def submit_patient_data(user_input):
    # Connect to the database
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    conn.cursor()

    #Reference variables for calling database
    reference = ['weight_kg', 'length_cm', 'head_circumference_cm', 'temperature_c', 'heart_rate_bpm', 
                    'respiratory_rate_bpm', 'oxygen_saturation', 'feeding_frequency_per_day', 
                    'urination_count_per_day', 'stool_count_per_day']
    reference_types=[float,float,float,float,int,int,int,int,int,int] #Corresponds to each reference for the kind of variable it is
    vals=[user_input[0]] #Gets the patient id which will never be a null value
    possible_null=['',None] #An array of the posible null values that could trip up sql

    #=========Baby Normal Values==================#
    temp_range=[37,38]; #Infant Temperature (c) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    hr_range=[110,160]; #Infant Heart Rate (bpm) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    rr_range=[30,60]; #Infant Respiratory Rate (bpm) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    o2_range=[88,92]; #Infant Oxygen Saturation Range: https://jamanetwork.com/journals/jamapediatrics/article-abstract/515871
    ffr_range=[6,12]; #Infant Feeding Frequency (Per Day) Range: https://www.parents.com/baby/feeding/baby-feeding-chart-how-much-and-when-to-feed-infants-the-first-year/
    u_range=[6,10]; #Infant Urination Frequency (Per Day) Range: https://www.parents.com/breastfeeding-and-wet-diapers-whats-normal-431621#:~:text=Urination%20After%20the%20First%20Week,to%20three%20hours%2C%20is%20fine.
    st_range=[1,8]; #Infant Stool Freguency (Per Day) Range: https://www.childrenscolorado.org/just-ask-childrens/articles/baby-poop-guide/
    normal_ranges=[tuple(temp_range),tuple(hr_range),tuple(rr_range),tuple(o2_range),tuple(ffr_range),tuple(u_range),tuple(st_range)]; #Infant Temperature (c) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    warnings=[]

    for i in range(len(reference)): #Don't need to check the first 1 cause that is the patient ID and, again, not going to be null
        if user_input[i+1] in possible_null: #Checks to see if it is empty
            vals.append(None) #Will make sure that the null value is properly added
        else:
            vals.append(reference_types[i](user_input[i+1]))
            if i >2: 
                if vals[i+1]<normal_ranges[i-3][0] or normal_ranges[i-3][1]<vals[i+1]: #Will run this for everything after
                    warnings=("Inputted Data is outside the normal range, please contact your doctor.")


    data=conn.execute(f"SELECT * FROM patients WHERE patients.id={vals[0]};").fetchone()
    

    #Gets the new age in days
    birthdate=datetime.date.fromisoformat(data[5]) #Takes the birth date and turns from text into a format a date object
    today=datetime.date.today() #Gets todays date
    age_days=(today-birthdate).days #Gets the age in days of the patient

     #==========Update Patient Data==========#
    # Debugging help from perplexity.ai, convo recorded in ai_conversations/debug_submit
    # conn.execute("INSERT OR IGNORE INTO patient_visit_data (weight_kg) VALUES (1)")
    try:
        conn.execute("""
            INSERT INTO patient_visit_data (
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
                stool_count_per_day,
                immunizations_needed,
                reflexes_normal,
                risk_Level
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
            """, [
                vals[0],                   # id_patient
                today.isoformat(),         # date
                age_days,                  # age_days
                vals[1],                   # weight_kg
                vals[2],                   # length_cm
                vals[3],                   # head_circumference_cm
                vals[4],                   # temperature_c
                vals[5],                   # heart_rate_bpm
                vals[6],                   # respiratory_rate_bpm
                vals[7],                   # oxygen_saturation
                None,                      # primary_feeding_type
                vals[8],                   # feeding_frequency_per_day
                vals[9],                   # urination_count_per_day
                vals[10],                  # stool_count_per_day
                None,                      # immunizations_needed
                None,                      # reflexes_normal
                None                       # risk_Level
            ])
        conn.commit()
    except sqlite3.Error as e:
        print("DB error:", e)
        raise

    # conn.commit()
    conn.close()
    return warnings