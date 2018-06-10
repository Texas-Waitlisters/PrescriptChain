from flask import Flask, jsonify, request, render_template
from users import user
import accountcontrol as ac

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)
Session['user'] = user()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    rs = ac.login(username, password)
    if(rs != null):
        Session['user'] = rs
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

