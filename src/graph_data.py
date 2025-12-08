# =================================== #
# Returns data from database to build
# graphs
#
# By Eliot Raynor 12/07/25
# =================================== #

import sqlite3

def graph_data(id, graphtype=""):
    # Return if graphtype is empty
    if graphtype == "" or graphtype == None:
        return [0], [0]

    id = 1 # TEMPORARY FOR DEBUGGING

    # Connect to the database
    conn = sqlite3.connect("NWI_DB.db")
    db = conn.cursor()

    # Search for x and y values
    db.execute('SELECT date, %s FROM patient_visit_data WHERE id_patient=%s' %(graphtype, id))
    vals = db.fetchall()
    x_vals = []
    y_vals = []
    for point in vals:
        x_vals.append(point[0])
        y_vals.append(point[1])

    # Close connection and return
    conn.close()
    return x_vals, y_vals