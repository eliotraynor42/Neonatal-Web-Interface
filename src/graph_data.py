# =================================== #
# Returns data from database to build
# graphs
#
# By Eliot Raynor 12/07/25
# =================================== #

import sqlite3

def graph_data(id, graphtype):
    # Connect to the database
    conn = sqlite3.connect("patient_database.sql") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    db = conn.cursor()

    # Search for x and y values
    db.execute('SELECT date, %s FROM patients WHERE id=%s' %(graphtype, id))
    x_vals = db.fetchall()[0][0]
    y_vals = db.fetchall()[0][1]

    # Close connection and return
    conn.close()
    return x_vals, y_vals