import json
import sqlite3
import urllib
import ssl
import time
import os
import sys
import collections

from flask import Flask, render_template, request, session, redirect, url_for, flash, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from urllib.request import urlopen
from models import Base, User, Club, Tag
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = "joshuaweinerpennlabs"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pennclubs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# from models import db
db.init_app(app)
engine = create_engine('sqlite:///pennclubs.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
from util import authenticate


try:
    f = open('pennclubs.db')
    f.close()
except FileNotFoundError:
    Base.metadata.create_all(engine)
    html = get_clubs_html()
    s = soupify(html)
    soups = get_clubs(s)
    for soup in soups:
        name = get_club_name(soup)
        desc = get_club_description(soup)
        tags = get_club_tags(soup)
        favorites = 0
        t = []
        club = Club(club_name=name, description=desc)
        db_session.add(club)
        db_session.commit()
        for tag in tags:
            t_new = Tag(tag=tag,
            club_id = db_session.query(Club).filter_by(club_name=name).first().id)
            db_session.add(t_new)
            db_session.commit()

@app.route('/')
def main():
    is_loggedin = False
    username = None
    if authenticate.is_loggedin(session):
        is_loggedin = True
        username = session['loggedin']
    clubs = json.loads(api_clubs())
    return render_template('clubs.html', clubs = clubs, loggedin=is_loggedin, username=username)

@app.route('/club_form', methods = ["GET"])
def club_form():
    is_loggedin = False
    username = None
    if authenticate.is_loggedin(session):
        is_loggedin = True
        username = session['loggedin']
        return render_template('createclub.html', loggedin=is_loggedin, username=username)
    else:
        flash("You must be logged in to use this feature!", "danger")

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=["GET", "POST"])
def api_clubs():
    if request.method == "POST":
        name = request.json['name']
        description = request.json['description']
        tags = request.json['tags']
        print(name, description, tags)
        club = Club(club_name=name, description=description)
        db_session.add(club)
        db_session.commit()
        for tag in tags:
            t_new = Tag(tag=tag,
            club_id = db_session.query(Club).filter_by(club_name=name).first().id)
            db_session.add(t_new)
            db_session.commit()
        flash("Added club " + name + " to the database.", "success")
        return jsonify(dict(redirect='/'))
    else:
        clubs = db_session.query(Club).all()
        club_list = []
        for club in clubs:
            # print(club)
            d = collections.OrderedDict()
            d['id'] = club.id
            d['club_name'] = club.club_name
            tags = club.tags
            ts = []
            for t in tags:
                tg = str(t.tag)
                ts.append(tg)
            d['tags'] = ts
            d['description'] = club.description
            # d['favorites'] = club[4]
            club_list.append(d)
        j = json.dumps(club_list)
        return j

@app.route("/api/user/<username>", methods=["GET"])
def get_user(username):
    user = db_session.query(User).filter_by(username=username).first()
    d = collections.OrderedDict()
    d['id'] = user.id
    d['username'] = user.username
    favorites = user.favorites
    fs = []
    for fave in favorites:
        fs.append(fave.club_name)
    d['favorites'] = fs
    j = jsonify(d)
    return j

@app.route("/api/favorite", methods=["POST"])
def favorite():
    if authenticate.is_loggedin(session):
        is_loggedin = True
        username = session['loggedin']
        user = db_session.query(User).filter_by(username=username).first()
        favorites = user.favorites
        club_id = request.json['club_id']
        if str(club_id) not in favorites:
            favorites.append(str(club_id))
            for f in favorites:
                faves += f + ","
            faves = faves[:-1]
            db_func.modify('users', 'favorites', faves, 'username', username)
            club = db_func.retrieve_club(club_id)
            fs = club[3] #club favorites
            fs += 1
            db_func.modify('clubs', 'favorites', fs, "ClubID", club_id)
            return jsonify(True)
        else:
            return jsonify(False)
    return "false"


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if authenticate.is_loggedin(session):
            is_loggedin = True
            username = session['loggedin']
            flash("You are already logged in!", "danger")
            return redirect(url_for('main'))
        else:
            return render_template("register.html")
    else:
        success, message = authenticate.register_user(
                request.form['username'],
                request.form['password'],
                request.form['passwordConfirmation'])
        if success:
            flash(message, "success")
            return redirect(url_for('login'))
        else:
            flash(message, "danger")
            return redirect(url_for('register'))
    return render_template("register.html")

@app.route('/login' , methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if authenticate.is_loggedin(session):
            is_loggedin = True
            username = session['loggedin']
            flash("You are already logged in!", "danger")
            return redirect(url_for('main'))
        else:
            return render_template("login.html")
    else:
        success, message = authenticate.login_user(
            request.form['username'],
            request.form['password']
        )
        if success:
            flash(message, "success")
            session['loggedin']=request.form['username']
            return redirect(url_for('main'))
        else:
            flash(message, "danger")
            return redirect(url_for('login'))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if authenticate.is_loggedin(session):
        session.pop('loggedin')
        flash("Successfully logged out.", "success")
    else:
        flash("You are not logged in!", "danger")
    return redirect(url_for('main'))

if __name__ == '__main__':

    app.run()
