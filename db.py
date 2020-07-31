import MySQLdb

options = open(r".\dboptions.txt", "r")
url = options.readline()
user = options.readline()
dbpw = options.readline()
db = options.readline()
options.close()
url = str(url[6:len(url)])
user = str(user[6:len(user)])
dbpw = str(dbpw[6:len(dbpw)])
db = str(db[6:len(db)])

# Function doesn't actually get used in current iteration of database commands


def showOneResult(id):
    if (id == '0'):
        print("Invalid ID #")
        return 0
    try:
        db_connection = MySQLdb.connect(url, user, dbpw, db)
    except:
        print("Can't connect to database")
        return 0
    # print("Show result connected")

    cursor = db_connection.cursor()

    sql = "SELECT * FROM fighters WHERE id = %s"
    cursor.execute(sql, id)
    m = cursor.fetchone()

    try:
        print("The fighter is", m)
    except:
        print("No fighter with id " + id)
    db_connection.close()

# returns ID number for fighter with name in list, else returns 0 if no fighter in list


def queryId(name):
    try:
        db_connection = MySQLdb.connect(url, user, dbpw, db)
    except:
        print("Can't connect to database", flush=True)
        return 0
    # print("Query ID connected")

    cursor = db_connection.cursor()

    sql = "SELECT id FROM fighters WHERE fighter = %s"
    cursor.execute(sql, (name,))
    m = cursor.fetchone()
    db_connection.close()

    try:
        # print("The id is",m[0])
        return str(m[0])
    except:
        return '0'

# inserts fighter into table with 0 wins and 0 fights, queries current table for rows to receive unique id


def insertFighter(name):
    try:
        db_connection = MySQLdb.connect(url, user, dbpw, db)
    except:
        print("Can't connect to database", flush=True)
        return 0
    # print("Insert fighter connected")

    cursor = db_connection.cursor()

    sql = "SELECT COUNT(id) FROM fighters;"
    cursor.execute(sql)
    m = cursor.fetchone()

    sql = "INSERT INTO fighters VALUES (%s, %s, 0, 0);"
    cursor.execute(sql, (m[0]+1, name))
    db_connection.commit()
    db_connection.close()

    return str(m[0]+1)

# updates fighter (based on id) fights and wins both +1


def fighterWin(id):
    try:
        db_connection = MySQLdb.connect(url, user, dbpw, db)
    except:
        print("Can't connect to database", flush=True)
        return 0
    # print("Fighter won connected")

    cursor = db_connection.cursor()

    sql = "SELECT fights, wins FROM fighters WHERE id = %s;"
    cursor.execute(sql, (str(id),))
    m = cursor.fetchone()

    sql = "UPDATE fighters SET fights = %s, wins = %s WHERE id = %s;"
    cursor.execute(sql, (m[0]+1, m[1]+1, str(id)))
    db_connection.commit()
    db_connection.close()

# updates fighter (based on id) fights by +1


def fighterLose(id):
    try:
        db_connection = MySQLdb.connect(url, user, dbpw, db)
    except:
        print("Can't connect to database", flush=True)
        return 0
    # print("Fighter lost connected")

    cursor = db_connection.cursor()

    sql = "SELECT fights FROM fighters WHERE id = %s;"
    cursor.execute(sql, (str(id),))
    m = cursor.fetchone()

    sql = "UPDATE fighters SET fights = %s WHERE id = %s;"
    cursor.execute(sql, (m[0]+1, str(id)))
    db_connection.commit()
    db_connection.close()

# calculates win rate between 2 fighters based on id, returns positive for player 1 favor, negative for player 2 favor


def calcWinRate(id, id2):
    try:
        db_connection = MySQLdb.connect(url, user, dbpw, db)
    except:
        print("Can't connect to database", flush=True)
        return 0
    # print("Win rate connected", flush=True)

    cursor = db_connection.cursor()

    sql = "SELECT wins, fights FROM fighters WHERE id = %s;"
    cursor.execute(sql, (str(id),))
    p1 = cursor.fetchone()
    cursor.execute(sql, (str(id2),))
    p2 = cursor.fetchone()
    db_connection.close()

    try:
        rate1 = p1[0]/p1[1]
        rate2 = p2[0]/p2[1]
    except:
        return 0.00

    return rate1-rate2

# Function Call For Connecting To Our Database
# p1 = insertFighter('Machelle')
# print(p1)
# fighterWin('1')
# fighterLose('1')
# id = queryId('Storm')
# print(id)
# showOneResult(str(queryId('Storm')))
# showOneResult('1')
# calcWinRate('2', '1')
