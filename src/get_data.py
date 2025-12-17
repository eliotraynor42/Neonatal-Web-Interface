# =================================== #
# Gets the newest data for a patient
#
# By Eliot Raynor 12/10/25
# =================================== #

import sqlite3
from bmes_ahmet_loader import *

def get_data(user_id):

    # Find user in database and retrieve values
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    db = conn.cursor()
    
    # Create a function to search for most recent value
    def newest_data(db, user_id, column):
        db.execute(
            f"SELECT {column} FROM patient_visit_data WHERE id_patient = ? AND {column} IS NOT NULL ORDER BY id DESC LIMIT 1",
            (user_id,)
        )
        row = db.fetchone()
        return row[0] if row else None

    # Create output
    patients = [
        {
            "ID": newest_data(db, user_id, "id_patient"),
            "Age": newest_data(db, user_id, "age_days"),
            "Weight": newest_data(db, user_id, "weight_kg"),
            "Length": newest_data(db, user_id, "length_cm"),
            "Head Circumference": newest_data(db, user_id, "head_circumference_cm"),
            "Temperature": newest_data(db, user_id, "temperature_c"),
            "Heart Rate": newest_data(db, user_id, "heart_rate_bpm"),
            "Respiratory Rate": newest_data(db, user_id, "respiratory_rate_bpm"),
            "Oxygen Saturation": newest_data(db, user_id, "oxygen_saturation"),
            "Primary Feeding Type": newest_data(db, user_id, "primary_feeding_type"),
            "Feeding Per Day": newest_data(db, user_id, "feeding_frequency_per_day"),
            "Urination Per Day": newest_data(db, user_id, "urination_count_per_day"),
            "Stool Per Day": newest_data(db, user_id, "stool_count_per_day"),
            "Immunizations Needed": newest_data(db, user_id, "immunizations_needed"),
            "Reflexes": newest_data(db, user_id, "reflexes_normal"),
            "Risk": newest_data(db, user_id, "risk_Level")
        }
    ]
    conn.close()
    return patients