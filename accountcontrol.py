import pymysql

dbServerName    = "localhost"
dbUser          = "user"
dbPassword      = ""
dbName          = "test"
charSet         = "utf8mb4"
cusrorType      = pymysql.cursors.DictCursor

def login(username, password):
    connectionObject = pymysql.connect(host = dbServerName,
                                 user = dbUser,
                                 password = dbPassword,
                                 db = dbName,
                                 charset = charSet,
                                 cursorclass = cusrorType)
    try:
        with connectionObject.cursor() as cursor:
        query = "SELECT * FROM USERS WHERE username = "+username+" " \
                "AND password = "+password+""
        # countquery = "SELECT COUNT(*) FROM USERS WHERE username = "+username+" " \
        #         "AND password = "+password+""
        cursor.execute(query)
        # cursor.execute(countquery)
        rows = cursor.fetchall()
        count = cursor.rowcount

        if (count == 0)
            return None
        elif (count > 0)
            rows.index(1)
            return


    #     zero rows return none
    # 1 or more return object with first row made into user class object

    finally:
        connectionObject.close()

def createaccount():
