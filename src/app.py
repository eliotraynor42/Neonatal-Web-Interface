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
from get_doctor_notif import get_doctor_notif
from get_patient import get_patient
from get_user_login import get_user_login
from graph_data import graph_data
from get_data import get_data
from submit_health import submit_patient_data
from get_patient_list import get_patient_list

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
        return redirect(url_for('doctor_home', user_doc=user_id))
    else:
        return redirect('/?err=2')


# Redirect to patient page
@app.route('/patient_home', methods=['GET', 'POST'])
def patient_home():
    # Get user info
    user_id = request.args.get('user')
    patient_info = get_patient(user_id)
    data = [f'{a}: {b}' for a, b in patient_info.items()]
    kept_data = data[:3]

    # Get all user info
    patient_data = get_data(user_id)[0]
    all_data = [f'{a}: {b}' for a, b in patient_data.items()]
    
    # Get message history
    message_history = get_comm_doc(user_id)[::-1]
    messages = []
    for m in message_history:
        messages.append({'message': m['message'], 'date': m['date'], 'from': m['id_doctor']})
    
    # Return Page
    return render_template('patient_home.html', user=user_id, user_info=kept_data, user_info2=all_data, messages=messages)


# Graph Data Form Submission
@app.route('/graph_data', methods=['POST'])
def graph_data_vals():
    user_id = request.form.get('user')
    graph_type = request.form.get('graphtype')
    x, y = graph_data(user_id, graph_type)
    return jsonify({'x': x, 'y': y})


# Conversation Form Submission
@app.route('/convo', methods=['POST'])
def conversation_add():
    # SEND MESSAGE OUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    user_id = request.form('user')
    message = request.form('comm_text')
    date = request.form.get('date_comm')
    # convo_add(user_id)
    return jsonify({'date': date})


# Health Tracker Form Submission
@app.route('/submit_health', methods=['POST'])
def submit_health():
    # Get Data
    vals = request.form
    reference = ['weight_kg', 'length_cm', 'head_circumference_cm', 'temperature_c', 'heart_rate_bpm', 
                 'respiratory_rate_bpm', 'oxygen_saturation', 'feeding_frequency_per_day', 
                 'urination_count_per_day', 'stool_count_per_day']
    submit_data = [None]*10

    # Interpret Data and Send
    for key in vals.keys():
        try:
            ind = reference.index(key)
            submit_data[ind] = vals.get(key)
        except ValueError:
            continue
    warnings = submit_patient_data(100, submit_data)
    time = str(datetime.datetime.now().time())[:8]

    return jsonify({'message': 'Data Submitted at %s' %(time), 'warnings': warnings})


# Redirect to doctor page
@app.route('/doctor_home', methods=['GET', 'POST'])
def doctor_home():
    user_id = request.args.get('user_doc')

    # Get doctor notifs
    message_history = get_doctor_notif(user_id)[::-1]
    messages = []
    for m in message_history:
        messages.append({'message': m['message'], 'date': m['date'], 'from': m['id_patient']})
    
    # Get patient list
    patient_list = get_patient_list(user_id)
    patients = []
    for p in patient_list:
        patients.append({'id': p['id'], 'name': p['name']})

    return render_template('doctor_home.html', user_doc=user_id, messages=messages, patients=patients)


# Redirect to doctor patient view page
# Redirect to patient page
@app.route('/observe_patient', methods=['GET', 'POST'])
def observe_patient():
    # Get user info
    user_id = request.form.get('user_doc')
    patient_id = request.form.get('patient_id')
    patient_info = get_patient(patient_id)
    data = [f'{a}: {b}' for a, b in patient_info.items()]
    kept_data = data[:3]
    
    # Get message history
    message_history = get_comm_doc(patient_id)[::-1]
    messages = []
    for m in message_history:
        messages.append({'message': m['message'], 'date': m['date'], 'from': m['id_doctor']})

    # Get all user info
    patient_data = get_data(user_id)[0]
    all_data = [f'{a}: {b}' for a, b in patient_data.items()]

    return render_template('doctor_page.html', user=patient_id, user_doc=user_id, user_info=kept_data, user_info2=all_data, messages=messages)


# Solution for opening the browser from https://stackoverflow.com/questions/54235347/open-browser-automatically-when-python-code-is-executed/54235461#54235461
def open_browser():
    # webbrowser.open_new("http://127.0.0.1:5000")
    return


# Run Flask Listener
if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == "true":
        open_browser()
    app.run(host='127.0.0.1', port=5000, debug=True)