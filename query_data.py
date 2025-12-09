#Python Function associated With the Patient Selection
#Used to find patient data for a specific patient

def query_data(call):
    import sqlite3; #Gets the DataBase Library
    conn=sqlite3.connect('Sample_DB_PyTest.sqlite') #Creates Variable for connection
    cur = conn.cursor() #Creates call for working with database
    cur.execute(call)
    results=cur.fetchall()
    cur.close()
    return results


import sys #Gives Access to System Arguments

if __name__=="__main__": #Runs if being run directly by another program
    import json; #Get Json this will make php have an easier time with the output
    call=sys.argv[1] #Takes in the call from php
    call=call.strip("'")
    print(json.dumps(query_data(call))); #Using json will put the output in a useable type for php