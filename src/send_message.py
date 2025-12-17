# =================================== #
# Returns data from health tracker to database
# 
# By Alexandra Nickel 12/08/25
# =================================== #

#==========Import Libraries==========#
import sqlite3
import datetime
from bmes_ahmet_loader import *

#===========Send Message Function==========#
def send_message(message):
    conn = sqlite3.connect(bmes.userdownloaddir() + "/NWI_DB.db")
    conn.cursor()

    conn.execute("INSERT INTO comms(message) VALUES ( ? )", (message,))
    conn.commit()
    conn.execute()