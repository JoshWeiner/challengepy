import sqlite3   #enable control of an sqlite database

DB_FILE="pennclubs.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

'''BASE FUNCTIONS'''

def findInfo(tableName,filterValue,colToFilt,fetchOne = False, search= False):
    if search:
        filterValue = '%' + filterValue + '%'
        eq = 'LIKE'
    else:
        eq = '='
    command = "SELECT * FROM  '{0}'  WHERE {1} {3} '{2}'".format(tableName,colToFilt,filterValue, eq)
    c.execute(command)

    listInfo = []
    if fetchOne:
        info = c.fetchone()
    else:
        info = c.fetchall()
    if info:
        for col in info:
            listInfo.append(col)
    return listInfo

def modify(tableName, colToMod, newVal, filterCol, filterValue):
    # print(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterCol, filterValue))
    c.execute(("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'").format(tableName, colToMod, newVal, filterCol, filterValue))
    db.commit()

def delete(tableName, filterCol, filterValue):
    print(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterCol, filterValue))
    c.execute(("DELETE FROM {0} WHERE {1} = '{2}'").format(tableName, filterCol, filterValue))
    db.commit()

'''SPECIFIC FUNCTIONS'''
def registerUser(username, password):
    insert('users', [username, password, '', ''])

def getUser(username):
    command = "SELECT UserID, Username, Favorites FROM users WHERE {0} = '{1}'".format("Username", username)
    c.execute(command)
    return c.fetchall()

def add_club(name, desc, tags):
    if len(findInfo('clubs', name, 'club_name')) == 0:
        command = "INSERT INTO clubs (club_name, tags, description) VALUES(?, ?, ?);"
        c.execute(command, (name, tags, desc))
        db.commit()


def getData(username):
    # command = "SELECT Hotdogs, Grandmas, Shops FROM users WHERE username='{0}'".format(username)
    # c.execute(command)
    return(c.fetchall())

def retrieve_club(id):
    command = "SELECT club_name, tags, description, favorites FROM clubs WHERE {0}='{1}'".format("ClubID", id)
    c.execute(command)
    return(c.fetchone())

def retrieve_clubs():
    command = "SELECT * FROM clubs"
    c.execute(command)
    return(c.fetchall())

def club_json():
    clubs = Club.query().all()
    return clubs
