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

@app.route('/createAccount')
def createAccount():
    return ''

@app.route('/createChain')
def createChain():
    return ''

@app.route('/getChain')
def getChain():
    return ''

app.run(host='0.0.0.0')
