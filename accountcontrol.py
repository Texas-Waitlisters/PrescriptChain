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