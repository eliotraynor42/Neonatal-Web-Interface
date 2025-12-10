# =================================== #
# Builds a sample database
#
# By Alexandra Nickel 
# =================================== #

#==========Setup Libraries and Sqlite==========#
# Class Libaries Import
import sys,os; sys.path.append(os.environ['BMESAHMETDIR']);
import bmes;

#Other Libraries
import sqlite3 #Database Connection
import datetime #Needed to generate random dates
import random #Needed to generate data
import string #Needed for password generation
from hashlib import sha256 #Needed for password generation



def DB_maker():

    # open a database connection
    dbfile= bmes.userdownloaddir() + '/NWI_DB.db'; #Makes the files
    conn = sqlite3.connect(dbfile); #Gets the DB connection
    cur=conn.cursor()

    #==========Variable Setup==========#

    ## Variable Ranges:
    b_wt_range=[6,9]; #Birth Weight (kg) Range: https://www.medicalnewstoday.com/articles/325630#what-to-expect
    b_ln_range=[47,53]; #Birth Length (cm) Range: https://www.medicalnewstoday.com/articles/324728
    b_hd_range=[32,36]; #Birth Head Circumference (cm) Range: https://www.babycenter.com/baby/baby-development/baby-head-circumference_40009394
    temp_range=[37,38]; #Infant Temperature (c) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    hr_range=[110,160]; #Infant Heart Rate (bpm) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    rr_range=[30,60]; #Infant Respiratory Rate (bpm) Range: https://health.clevelandclinic.org/pediatric-vital-signs
    o2_range=[88,92]; #Infant Oxygen Saturation Range: https://jamanetwork.com/journals/jamapediatrics/article-abstract/515871
    ffr_range=[6,12]; #Infant Feeding Frequency (Per Day) Range: https://www.parents.com/baby/feeding/baby-feeding-chart-how-much-and-when-to-feed-infants-the-first-year/
    u_range=[6,10]; #Infant Urination Frequency (Per Day) Range: https://www.parents.com/breastfeeding-and-wet-diapers-whats-normal-431621#:~:text=Urination%20After%20the%20First%20Week,to%20three%20hours%2C%20is%20fine.
    st_range=[1,8]; #Infant Stool Freguency (Per Day) Range: https://www.childrenscolorado.org/just-ask-childrens/articles/baby-poop-guide/
    gender=["f","m"]; #Infant Gender

    #Doctor Data:
    first=['Beverly','Dana','Meredith','Jemma','Jane']
    last=['Crusher','Scully','Grey','Simmons','Doe']
    doctor_usernames=['b_crush','dana123','meredith_G','simmons_A0956307','demo']
    hospitals=['Enterprise Hospital','X Hospital','Grey Sloan Memorial Hospital','Shield Hospital','Not A Fake Hospital']

    #Comms Messages:
    messages=["She has spit up 3 times today. Is that normal?","She cried today, should I be worried about collic?","She has a rash on her leg, should I bring her in?"]

    #==========Clean Slate==========#
    conn.execute('DROP TABLE IF EXISTS patients;')
    conn.execute('DROP TABLE IF EXISTS patient_visit_data;')
    conn.execute('DROP TABLE IF EXISTS doctors;')
    conn.execute('DROP TABLE IF EXISTS comms')

    #==========Creating Tables==========#

    #Patients
    conn.execute("""CREATE TABLE patients (
                id INTEGER PRIMARY KEY,
                username VARCHAR(30),
                password VARCHAR(30),
                name VARCHAR(30),
                gender VARCHAR(30),
                birth DATE,
                birth_weight_kg FLOAT,
                birth_length_cm FLOAT,
                birth_head_circumference_cm FLOAT,
                id_doctor INTEGER
                );""")

    #Patient Visit Data
    conn.execute("""CREATE TABLE patient_visit_data (
                id INTEGER PRIMARY KEY,
                id_patient INTEGER,
                date DATE,
                age_days INTEGER,
                weight_kg FLOAT,
                length_cm FLOAT,
                head_circumference_cm FLOAT,
                temperature_c FLOAT,
                heart_rate_bpm INTEGER,
                respiratory_rate_bpm INTEGER,
                oxygen_saturation INTEGER,
                feeding_frequency_per_day INTEGER,
                urination_count_per_day INTEGER,
                stool_count_per_day INTEGER
                );""")

    #Doctors
    conn.execute("""CREATE TABLE doctors
                ( id INTEGER PRIMARY KEY,
                username VARCHAR(30),
                password VARCHAR(30),
                last_name VARCHAR(30),
                first_name VARCHAR(30),
                hospital VARCHAR(30) );""");

    #Comms
    conn.execute("""CREATE TABLE comms (
                id INTEGER PRIMARY KEY,
                id_doctor INTEGER,
                id_patient INTEGER,
                date DATE,
                message VARCHAR(100)
                )""")

    #==========Insert Data Setup==========#

    #Birth Data Holders:
    names=[] #Holder for names
    birthdays=[] #Holder for birthdays
    b_weights=[] #Holder for birth weights
    b_lengths=[] #Holder for birth lengths
    b_heads=[] #Holder for birth head circumference
    id_doctor=[] #Holder for doctor IDs.

    #Downloads a list of random names
    temp_names=bmes.downloadurl('https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/fea1da1a3c4ce5c8e470f679a8e1bc741281a609/first-names.txt');
    with open(temp_names,"r") as temp:
        temp2_names=temp.read().splitlines() #Stores the names on seperate lines

    #Makes the password generator:
    pick_chars=string.ascii_letters+string.digits

    # Sets variables that will need to be referenced in creation
    for i in range(100): #Set the data that will need to be referenced during the making of the patients table
        ran_int=random.randint(0,len(temp2_names)-1); #Gets a random index of a name from the list
        names.append(temp2_names[ran_int]); #Adds the name to the names
        birthdays.append(datetime.date(2025,random.randint(1,5),random.randint(1,28))); #Generates Birthdays
        b_weights.append(round(random.uniform(b_wt_range[0],b_wt_range[1]),2)); #Generates Birth Weights
        b_lengths.append(round(random.uniform(b_ln_range[0],b_ln_range[1]),2)); #Generates Birth Lengths
        b_heads.append(round(random.uniform(b_hd_range[0],b_hd_range[1]),2)); #Generates Birth Head Cicumferences

    last_visit=birthdays[:] #Sets the initation variable for dates

    #==========Generate and Insert Patient Visit Data==========#

    #Generate Random Data for Patient Visit Data Table
    for i in range(5000):
        patient_id=random.randint(0,len(names)-1); #Calls a random patient id for this entry
        last_visit[patient_id]+= datetime.timedelta(days=2); #Adds 2 days sinse the last visit
        age_days=(last_visit[patient_id]-birthdays[patient_id]).days; #Gets the age at the visit
        weight_kg=b_weights[patient_id]+age_days*(30+random.uniform(-2,2))/1000; #Generates a fake weight (kg) from visit: https://www.mayoclinic.org/healthy-lifestyle/infant-and-toddler-health/expert-answers/infant-growth/faq-20058037
        length_cm=b_lengths[patient_id]+age_days*(2.5+random.uniform(-0.05,0.05))/30; #Generates a length (cm) for the visit: (ref same as above)
        head_circumference_cm=b_heads[patient_id]+age_days*(2.5+random.uniform(-0.02,0.02))/30; #Generates a head circumference 
        temperature_c=round(random.uniform(temp_range[0],temp_range[1]),2) #Generates a temperature (c)
        heart_rate_bpm=random.randint(hr_range[0],hr_range[1]); #Generates a heart rate (bpm)
        respiratory_rate_bpm=random.randint(rr_range[0],rr_range[1]); #Generates a respiratory rate (bpm) 
        oxygen_saturation=random.randint(o2_range[0],o2_range[1]); #Generates an oxygen saturation (%)
        feeding_frequency_per_day=random.randint(ffr_range[0],ffr_range[1]); #Generates a feeding frequncy (per day)
        urination_count_per_day=random.randint(u_range[0],u_range[1]); #Generates a urination frequency (per day)
        stool_count_per_day=random.randint(st_range[0],st_range[1]); #Generates a stool frequency (per day)
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
                    feeding_frequency_per_day,
                    urination_count_per_day,
                    stool_count_per_day
                    ) VALUES (
                    {patient_id+1},
                    '{last_visit[patient_id]}',
                    {age_days},
                    {weight_kg},
                    {length_cm},
                    {head_circumference_cm},
                    {temperature_c},
                    {heart_rate_bpm},
                    {respiratory_rate_bpm},
                    {oxygen_saturation},
                    {feeding_frequency_per_day},
                    {urination_count_per_day},
                    {stool_count_per_day}
                    );""")

    #==========Insert Generate and Insert Patients Data
    for i in range(len(names)):
        username=f"{names[i]}_{random.randint(100,999)}"; #Generates a random username using the patient's name
        temp_pass=""
        for j in range(10):
            temp_pass=temp_pass.join(random.choice(pick_chars)) #Generates a random password of length 10
        login_val=username.encode('utf-8')+temp_pass.encode('utf-8')
        password=sha256(login_val).hexdigest() #Writes an encoded password
        conn.execute(f"""INSERT INTO patients (
                    username,
                    password,
                    name,
                    gender,
                    birth,
                    birth_weight_kg,
                    birth_length_cm,
                    birth_head_circumference_cm,
                    id_doctor
                    ) VALUES (
                    '{username}',
                    '{password}',
                    '{names[i]}',
                    '{gender[random.randint(0,1)]}',
                    '{birthdays[i]}',
                    {b_weights[i]},
                    {b_lengths[i]},
                    {b_heads[i]},
                    {random.randint(1,4)}
                    );""")
        
    #==========Insert Doctor Data==========#
    for i in range(5):
        doctor_temp_pass=""
        for j in range(10):
            doctor_temp_pass=doctor_temp_pass.join(random.choice(pick_chars)) #Generates a random password of length 10
        doctor_login_val=doctor_usernames[i].encode('utf-8')+doctor_temp_pass.encode('utf-8')
        doctor_password=sha256(doctor_login_val).hexdigest() #Writes an encoded password
        conn.execute(f"""INSERT INTO doctors (
                    username,
                    password,
                    last_name,
                    first_name,
                    hospital
                    ) VALUES (
                    '{doctor_usernames[i]}',
                    '{doctor_password}',
                    '{last[i]}',
                    '{first[i]}',
                    '{hospitals[i]}'
                    );""")

    #==========Insert Comms Data==========#
    for i in range(3):
        conn.execute(f"""INSERT INTO comms (
                    id_doctor,
                    id_patient,
                    date,
                    message
                    ) VALUES (
                    5,
                    100,
                    '{datetime.date.today()}',
                    '{messages[i]}'
                    )""")

    #==========Update To Run Demo==========#
    for j in range(10):
            temp_pass=temp_pass.join(random.choice(pick_chars)) #Generates a random password of length 10
    login_val="demo".encode('utf-8')+temp_pass.encode('utf-8')
    password=sha256(login_val).hexdigest() #Writes an encoded password

    conn.execute(f"UPDATE patients SET id_doctor=5, username='demo', password='{password}', gender='f' WHERE id=100")
        
    conn.commit()