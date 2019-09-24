import json
import sqlite3
import urllib
import ssl
import time
import sys
import collections

from flask import Flask, render_template, request, session, redirect, url_for, flash, Response, jsonify
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from urllib.request import urlopen

from util import authenticate
import db_func

app = Flask(__name__)
app.secret_key = "joshuaweinerpennlabs"

authenticate.register_user("jen", "P3nnLabs!", "P3nnLabs!")
html = get_clubs_html()
s = soupify(html)
soups = get_clubs(s)
for soup in soups:
    name = get_club_name(soup)
    desc = get_club_description(soup)
    tags = get_club_tags(soup)
    favorites = 0
    t = ""
    for tag in tags:
        t += tag + ","
    t = t[:-1]
    db_func.add_club(name, desc, t)
    db_func.modify("clubs", "favorites", 0, "club_name", name)

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

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=["GET", "POST"])
def api_clubs():
    if request.method == "POST":
        name = request.json['name']
        description = request.json['description']
        tags = request.json['tags']
        print(name)
        t = ""
        for tag in tags:
            t += tag + ","
        t = t[:-1]
        db_func.add_club(name, description, t)
        db_func.modify("clubs", "favorites", 0, "club_name", name)
        flash("Added club " + name + " to the database.", "success")
        return jsonify(dict(redirect='/'))
    else:
        clubs = db_func.club_json()
        club_list = []
        for club in clubs:
            # print(club)
            d = collections.OrderedDict()
            d['id'] = club[0]
            d['club_name'] = club[1]
            d['tags'] = club[2].split(",")
            d['description'] = club[3]
            d['favorites'] = club[4]
            club_list.append(d)
        j = json.dumps(club_list)
        return j

@app.route("/api/user/<username>", methods=["GET"])
def get_user(username):
    user = db_func.getUser(username)
    for u in user:
        d = collections.OrderedDict()
        d['id'] = user[0][0]
        d['username'] = user[0][1]
        d['favorites'] = user[0][2]
        j = jsonify(d)
        return j

@app.route("/api/favorite", methods=["POST"])
def favorite():
    if authenticate.is_loggedin(session):
        is_loggedin = True
        username = session['loggedin']
        user = db_func.getUser(username)
        faves = user[0][2]
        favorites = []
        if faves != "":
            favorites = faves.split(",")
        club_id = request.json['club_id']
        faves = ""
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
            return jsonify(dict(redirect='/'))
        else:
            return jsonify(dict(redirect='/'))


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
    # app.debug = True
    app.run()
