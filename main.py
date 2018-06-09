from flask import Flask, jsonify, request, render_template
from users import user
import accountControl as ac

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

@app.route('/createAccount')
def createAccount():
    return ''

@app.route('/createChain')
def createChain():
    return ''

@app.route('/getChain')
def getChain():
    return ''

