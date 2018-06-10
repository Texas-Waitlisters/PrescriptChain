from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_session import Session
from users import User
import json
import factom

import db as ac

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'redis'
app.config.from_object(__name__)
app.secret_key = '12345'
Session(app)
@app.route('/')
def index():
    session.secret_key = '67890'
    user = session['user']
    if(user != None and user['logged_in']):
        print(user['username'])
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    rs = ac.login(username, password)
    print(rs)
    print(type(rs))
    if(rs != None):
        session['user'] = rs
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session['user'] = None
    return redirect(url_for('index'))

@app.route('/createAccount', methods=['POST'])
def createAccount(): 
    username = request.form['usernamesignup']
    password = request.form['passwordsignup']
    last = request.form['lastsignup']
    first = request.form['firstsignup']
    company = request.form['companysignup']
    email = request.form['emailsignup']
    acc_type = "0"
    user = {'username':username,'password':password,'last':last,'first':first,'company':company, 'email':email,'type':acc_type}
    print(ac.createaccount(user))
    return redirect(url_for('index'))

# Add prescription to blockchain
@app.route('/createChain', methods=['POST'])
def createChain():
    result = ac.readchain(request.form)
    print(result)
    if result == False:
        data = ([str((ac.gethighest() + 1))], request.form['meds'])
        output = factom.create_new_chain(*data)
        data_entry = {"first" : request.form['firstx'], "last": request.form['lastx'], "chain": output['chain_id']}
        ac.writechain(data_entry)
    else:
        data = (result['chain'], [str(ac.gethighest() + 1)], request.form['meds'])
        output = factom.add_to_chain(*data)
    data_entry = {"prescription_id" : (ac.gethighest() + 1), "hash" : output["entry_hash"], "patient_id" : result['id']}
    ac.writeprescription(data_entry)
    return redirect(url_for('index'))

# Read and validate prescription in blockchain
@app.route('/getChain', methods=['POST'])
def getChain():
    data_entry = {"firstx" : request.form['PatientsFirst'], "lastx": request.form['PatientsLast']}
    result = ac.readchain(data_entry)
    if result == False:
        return "Patient not found in records"
    chain_id = result['chain']
    _hash = ac.readprescription({"prescription_id": request.form["Prescription"], "patient_id": str(result['id'])})
    if _hash == False:
        return "Prescription not found in records"
    prescription = factom.get_entry(chain_id, _hash['hash'])
    if prescription:
        return str(prescription) 
    return "Prescription not found"

app.run(host='0.0.0.0')
