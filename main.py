from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_session import Session
from users import User
import json

import accountcontrol as ac

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
    return render_template('login.html')

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
    return user

@app.route('/createChain')
def createChain():
    return ''

@app.route('/getChain')
def getChain():
    return ''

app.run(host='0.0.0.0')
