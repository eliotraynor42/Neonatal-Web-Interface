# =================================== #
# Sets up the flask system to map HTML
# outputs to python files
#
# By Eliot Raynor 12/02/25
# =================================== #

# Import Flask and python scripts
from flask import Flask, redirect, render_template, request, url_for, jsonify
import os, webbrowser
import datetime
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
@app.route('/patient_home', methods=['GET', 'POST'])
def patient_home():
    # Get user info
    user_id = request.args.get('user')
    patient_info = get_patient(user_id)
    data = [f'{a}: {b}' for a, b in patient_info.items()]
    
    # Get message history
    message_history = get_comm_doc(user_id)
    messages = [m['message'] for m in message_history]
        
    # Return Page
    return render_template('patient_home.html', user=user_id, user_info=data, messages=messages)


# Patient Form Submission
# Update Graph Data
@app.route('/graph_data', methods=['POST'])
def graph_data_vals():
    user_id = request.form.get('user')
    graph_type = request.form.get('graphtype')
    x, y = graph_data(user_id, graph_type)
    return jsonify({'x': x, 'y': y})

# Conversation
@app.route('/convo', methods=['POST'])
def conversation_add():
    # ADD A WAY TO SAVE THE NEW CONVERSATION TO THE DATABASE
    date = request.form.get('date')
    return jsonify({'date': date})

# Health Tracker
@app.route('/submit_health', methods=['POST'])
def submit_health():
    user_id = request.form.get('user')
    # ADD A WAY TO SAVE THE NEW DATA TO THE DATABASE
    warnings = []#["baby in danger", "ahdhsjahlfhjask", "meksnajkdhfjkajkshjkh", "messagemgessage"]
    time = str(datetime.datetime.now().time())[:8]
    return jsonify({'message': 'Data Submitted %s' %(time), 'warnings': warnings})


# Redirect to doctor page
@app.route('/doctor_home')
def doctor_home():
    user_id = request.args.get('user')
    return render_template('doctor_home.html', user=user_id)


# Redirect to doctor patient view page
# Redirect to patient page
@app.route('/observe_patient', methods=['POST'])
def observe_patient():
    user_id = request.args.get('user')
    patient_id = request.args.get('patient_id')
    return render_template('doctor_page.html', user=user_id, patient=patient_id)


# Solution for opening the browser from https://stackoverflow.com/questions/54235347/open-browser-automatically-when-python-code-is-executed/54235461#54235461
def open_browser():
    # webbrowser.open_new("http://127.0.0.1:5000")
    return


# Run Flask Listener
if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == "true":
        open_browser()
    app.run(host='127.0.0.1', port=5000, debug=True)