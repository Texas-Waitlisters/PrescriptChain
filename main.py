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
        print(user['first'])
        return render_template('index.html')
    return render_template('login.html')

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
    username = request.form['username']
    password = request.form['password']
    last = request.form['last']
    first = request.form['first']
    company = request.form['company']
    email = request.form['email']
    acc_type = request.form['type']
    user = {'username':username,'password':password,'last':last,'first':first,'company':company, 'email':email,'type':acc_type}
    createaccount(user)
    return redirect(url_for('index'))

# Add prescription to blockchain
@app.route('/createChain', methods=['POST'])
def createChain():
    result = ac.readchain(request.form)
    if result == False:
        data = ((ac.gethighest() + 1), request.form['prescription'])
        output = factom.create_new_chain(*data)
        data_entry = {"first" : requests.form['first'], "last": requests.form['last'], "chain_id": output['chain_id']}
        ac.writechain(data_entry)
    else:
        data = (result['chain_id'], (ac.gethighest() + 1), request.form['prescription'])
        output = factom.add_to_blockchain(*data)
    data_entry = {"prescription_id" : (ac.gethighest() + 1), "hash" : output["entry_hash"]}
    ac.writeprescription(data_entry)

# Read and validate prescription in blockchain
@app.route('/getChain', methods=['POST'])
def getChain():
    result = ac.readchain(request.form)
    if result == False:
        return "Patient not found in records"
    chain_id = result['chain_id']
    _hash = ac.readprescription({"prescription_id": request.form["prescription_id"]})["hash"]
    if _hash == False:
        return "Prescription not found in records"
    prescription = factom.get_entry(chain_id, _hash)
    if prescription:
        return prescription

app.run(host='0.0.0.0')
