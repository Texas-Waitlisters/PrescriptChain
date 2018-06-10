import pymysql
from users import User

dbServerName    = "localhost"
dbUser          = "root"
dbPassword      = "ilikecode"
dbName          = "users"
charSet         = "utf8mb4"
cursorType      = pymysql.cursors.DictCursor

def login(username, password):
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "SELECT * FROM users WHERE username=\""+username+"\" AND password = \""+password+"\""
            # countquery = "SELECT COUNT(*) FROM USERS WHERE username = "+username+" " \
            #         "AND password = "+password+""
            cursor.execute(query)
            # cursor.execute(countquery)
            rows = cursor.fetchall()
            count = cursor.rowcount
            print(rows[0])
            if (count == 0):
                return None
            elif (count > 0):
                rows[0]['logged_in'] = True
                print(rows[0])
                return rows[0]

            return


    #     zero rows return none
    # 1 or more return object with first row made into user class object

    finally:
        connectionObject.close()

def createaccount(info):

    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "INSERT INTO users (username, password, last, first, company, email, type) VALUES (\""+info['username']+"\",\""+info['password']+"\",\""+info['last']+"\",\""+info['first']+"\",\""+info['company']+"\",\""+info['email']+"\",\""+info['type']+"\")"
            x = cursor.execute(query)
            return x
    finally:
        connectionObject.close()

def readchain(info):
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "SELECT * FROM patients WHERE first=\""+info['first']+"\"" AND last=\""+info['last']+"\""
            cursor.execute(query)
            rows = cursor.fetchall()
            if(cursor.rowcount==0):
                return False;
            return rows[0];
    finally:
        connectionObject.close()


def writechain(info):
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "INSERT INTO patients (first, last, chain_id) VALUES (\""+info['first']+"\",\""+info['last']+"\",\""+info['chain_id']+"\"");
            x = cursor.execute(query)
            return x
    finally:
        connectionObject.close()

def readprescription(info):
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "SELECT * FROM meds WHERE patient_id=\""+info['patient_id']+"\" AND meds=\""+info['meds']+"\""
            cursor.execute(query)
            rows = cursor.fetchall()
            if(cursor.rowcount==0):
                return False;
            return rows[0];
    finally:
        connectionObject.close()

def gethighest():
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "SELECT IDENT_CURRENT('meds')");
            x = cursor.execute(query)
            return cursor.fetchall()[0]+1
    finally:
        connectionObject.close()

def writeprescription(info):
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cursorType)
    try:
        with connectionObject.cursor() as cursor:
            query = "INSERT INTO meds (patient_id, meds) VALUES (\""+info['patient_id']+"\",\""+info['hash']+"\"");
            x = cursor.execute(query)
            return x
    finally:
        connectionObject.close()
