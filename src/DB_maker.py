# =================================== #
# Builds a sample database
#
# By Alexandra Nickel 
# =================================== #


# Class Libaries Import
import sys,os; sys.path.append(os.environ['BMESAHMETDIR']);
import bmes;

#Other Libraries
import sqlite3 #Database Connection
import datetime #Needed to generate random dates
import random #Needed to generate data


# open a database connection
dbfile= bmes.userdownloaddir() + '/NWI_DB.db'; #Makes the files
conn = sqlite3.connect(dbfile); #Gets the DB connection
cur=conn.cursor


## Variables and Constants for table; generation:

#Downloads a list of random names
temp_names=bmes.downloadurl('https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/fea1da1a3c4ce5c8e470f679a8e1bc741281a609/first-names.txt');
with open(temp_names,"r") as temp:
    temp2_names=temp.read().splitlines() #Stores the names on seperate lines

names=[]

 #Gets a random list of 100 names
for i in range(100):
    ran_int=random.randint(0,len(temp2_names)-1)
    names.append(temp2_names[ran_int])

#Integer Variable Ranges:
birthdays=[]
for i in range(100):
    birthdays.append(datetime.date(2025,random.randint(1,12),random.randint(1,28)))

print(birthdays)



## Creating the database:

#Patients
conn.execute("""CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            username VARCHAR(30),
            password VARCHAR(30),
            name VARCHAR(30),
            gender VARCHAR(30),
            birth DATE,
            birth_weight_kg FLOAT,
            birth_length_cm FLOAT,
            birth_head_circumference_cm FLOAT,
            id_doctor INTEGER,
            last_age INTEGER,
            last_weight FLOAT,
            last_length FLOAT,
            last_head FLOAT,
            last_temp FLOAT,
            last_heart INTEGER,
            last_respiratory INTEGER,
            last_o2 INTEGER,
            last_primary VARCHAR(30),
            last_feeding INTEGER,
            last_urination INTEGER,
            last_stool INTEGER,
            last_immunizations VARCHAR(30),
            last_reflexes VARCHAR(10),
            last_risk VARCHAR(30));""");

#Creates Patient Visit Data Table
conn.execute("""CREATE TABLE IF NOT EXISTS patient_visit_data (
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
            primary_feeding_type VARCHAR(30),
            feeding_frequency_per_day INTEGER,
            urination_count_per_day INTEGER,
            stool_count_per_day INTEGER,
            immunizations_needed VARCHAR(30),
            reflexes_normal VARCHAR(10),
            risk_level VARCHAR(30));""");

#Create Doctor Table
conn.execute("""CREATE TABLE IF NOT EXISTS doctors
            ( id INTEGER PRIMARY KEY,
            username VARCHAR(30),
            password VARCHAR(30),
            last_name VARCHAR(30),
            first_name VARCHAR(30),
            hospital VARCHAR(30) );""");


min=[1.5, 10.2]
max=10.2

dec=round(random.uniform(min[0],min[1]),4);
print(dec)