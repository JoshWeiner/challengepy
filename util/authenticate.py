import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import Base, User
from index import db_session

def register_user(username, password, repassword):
    '''
    Attempts to register a user and enter it in the users table.
    Returns a tuple containing a boolean indicating success
    and a message to flash to the user.
    '''
    if username == '' or password == '' or repassword == '':
        return (False, "Please fill in all fields.")
    elif password != repassword:
        return (False, "Passwords do not match!")

    with sqlite3.connect("pennclubs.db") as db:
        if user_exists(username):
            return (False, "Username {} already exists.".format(username))
        else:
            pw_hash = generate_password_hash(password)
            new_user = User(username=username, password=pw_hash)
            db_session.add(new_user)
            db_session.commit()
    return (True, "Successfully registered {}".format(username))

def user_exists(username):
    '''
    Returns whether a user with the given username exists
    '''
    with sqlite3.connect("pennclubs.db") as db:
        u = db_session.query(User).filter_by(username=username).first()

        return u != None

def login_user(username, password):
    '''
    Attempts to log in a user by checking the users table.
    Returns a tuple containing a boolean indicating success
    and a message to flash to the user.
    '''
    if username == '' or password == '':
        return (False, "Username or password missing!")

    with sqlite3.connect("pennclubs.db") as db:
        u = db_session.query(User).filter_by(username=username).first()
        if u != None and check_password_hash(u.password, password):
            return (True, "Successfully logged in!")
    return (False, "Incorrect username or password.")

def is_loggedin(session):
    '''
    Given a session, returns the username of the user if the user is logged in.
    Otherwise, returns False.
    '''
    if session.get('loggedin') is None:
        return False
    return session.get('loggedin')

def get_userid(session):
    name = is_loggedin(session)
    with sqlite3.connect("pennclubs.db") as db:
        id = db_session.query(User).filter_by(username=name).first().id
        return id
