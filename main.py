from flask import Flask, jsonify, request, render_template, session
from flask_session import Session
from users import User
import json

#import accountControl as ac

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'redis'
app.config.from_object(__name__)
app.secret_key = '12345'
Session(app)
@app.route('/')
def index():
    session.secret_key = '67890'
    session['user'] = vars(User())
    user = type('User', (), session['user'])
    print(session['user'])
    print(user)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    #rs = ac.login(username, password)
    #if(rs != null):
    #    Session['user'] = rs
    return render_template('login.html')
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
