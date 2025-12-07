# =================================== #
# Sets up the flask system to map HTML
# outputs to python files
#
# By Eliot Raynor 12/02/25
# =================================== #

# Import Flask and python scripts
from flask import Flask, redirect, render_template, request, url_for
import os, webbrowser
from get_comm_doc import get_comm_doc
from get_comm_patients import get_comm_patients
from get_doctor_notif import get_doctor_notif
from get_patient import get_patient
from get_user_login import get_user_login
from graph_data import graph_data
# from get_data import get_data
# from submit_data import submit_data
# from list_patients import list_patients

# Setup Flask
app = Flask(__name__)

# Set the default page
@app.route('/')
def home():
    return render_template('login_portal.html')

# Set the login script
@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    mode = request.form['loginmode']
    success, user_id = get_user_login(user, password, mode)

    # Redirect based on login success
    if success == 0:
        return redirect('/?err=1')
    elif success == 1:
        return redirect(url_for('patient_home', user=user_id))
    elif success == 2:
        return redirect(url_for('doctor_home', user=user_id))
    else:
        return redirect('/?err=2')

# Redirect to patient page
@app.route('/patient_home')
def patient_home():
    user_id = request.args.get('user')
    patient_info = get_patient(user_id)
    data = []
    for i in list(patient_info.items()):
        data.append(str(i[0]) + ": " + str(i[1]))
    return render_template('patient_home.html', user_info=data)

# Redirect to doctor page
@app.route('/doctor_home')
def doctor_home():
    user_id = request.args.get('user')
    return render_template('doctor_home.html', user=user_id)

# app.add_url_rule('/login_portal')

# Solution for opening the browser from https://stackoverflow.com/questions/54235347/open-browser-automatically-when-python-code-is-executed/54235461#54235461
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")
    return

# Run Flask Listener
if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        open_browser()
    app.run(host="127.0.0.1", port=5000, debug=True)