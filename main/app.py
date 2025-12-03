# =================================== #
# Sets up the flask system to map HTML
# outputs to python files
#
# By Eliot Raynor 12/02/25
# =================================== #

# Import Flask and python scripts
from flask import Flask, redirect, render_template, request
from get_user_login import get_user_login

# Setup Flask
app = Flask(__name__)

# Set the default page
@app.route('/NWI/')
def home():
    return render_template('login_portal.html')

# Set the login script
@app.route('/NWI/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    mode = request.form['loginmode']
    success, user_id = get_user_login(user, password, mode)
    if success == 0:
        return redirect('/NWI/?err=1')
    elif success == 1:
        return redirect('/NWI/patient_home?user=%s' %(user_id))
    elif success == 2:
        return redirect('/NWI/doctor_home?user=%s' %(user_id))
    else:
        return redirect('/NWI/?err=2')

# Set the patient scripts
# app.add_url_rule('/login_portal')

# Run Flask Listener
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)