from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import werkzeug
from scraper import *
from .models import Favorite
from . import db
import json
import config

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/rankings", methods=['GET', 'POST'])
def rankings():
    global players
    global choice_map
    global pos
    if request.method == "GET":
        if not request.args:
            pass
        else:
            try: 
                if request.args["load-more"]:
                    loaded_all = True
                    players = loadAll(choice_map[pos])
                    return render_template("rankings.html", players=players, user=current_user, loaded=True, loaded_all=loaded_all)
            except werkzeug.exceptions.BadRequestKeyError:
                print('key error')
            print(request.args)
            pos = request.args['select-pos']
            if pos:
                choice_map = {
                    'QB': 'passing',
                    'RB': 'rushing',
                    'WR': 'recieving',
                    'DEF': 'interceptions'
                }

                if pos in choice_map:
                    players = scrapeStats(choice_map[pos])
                    loaded_all = False
                    return render_template("rankings.html", players=players, user=current_user, loaded=True, loaded_all=loaded_all)
            else:
                flash("Please select a category.", category='error')
            
    elif request.method == "POST":     
        playerString = request.form.get('add-fav')
        if playerString:
            if current_user.is_authenticated:
                ind = playerString.index(":")
                name = playerString[0:ind]
                ppg = float(playerString[ind+1:])

                duplicates = Favorite.query.filter_by(name=name, user_id=current_user.id)

                if duplicates.count() > 0:
                    flash('Already in your favorites.', category='error')
                    return render_template("rankings.html", players=players, user=current_user, loaded=True)

                new_fav = Favorite(name=name, ppg=ppg, user_id=current_user.id)

                try: 
                    db.session.add(new_fav)
                    db.session.commit()
                    flash("Successfully added to favorites.", category="success")
                    return render_template("rankings.html", players=players, user=current_user, loaded=True)
                except Exception:
                    flash("Error. Please Try again later", category='error')
            else:
                flash("Must login to add favorites.", category='error')
                return redirect(url_for('auth.login'))
        else:
            flash("An error has occured. Try again later.", category='error')

    return render_template("rankings.html", user=current_user, loaded=False)

@views.route("/favorites", methods=['GET', 'POST'])
def favorites():
    if not current_user.is_authenticated:
        config.lastPage = "views.favorites"
        flash("Must log in to access this page.", category='error')
        return redirect(url_for("auth.login"))
    favs = Favorite.query.filter_by(user_id=current_user.id)
    if favs.count() < 1:
        empty = True
    else:
        empty = False
    return render_template("favorites.html", user=current_user, favorites=favs, empty=empty)

@views.route('delete-fav', methods=['POST'])
def delete_fav():
    fav = json.loads(request.data)
    favId = fav['favId']
    fav = Favorite.query.get(favId)
    if fav:
        if fav.user_id == current_user.id:
            db.session.delete(fav)
            db.session.commit()
            print(fav)
            
    return jsonify({})

@views.route("/injuries")
def injuries():
    if not current_user.is_authenticated:
        config.lastPage = "views.favorites"
        flash("Must log in to access this page.", category='error')
        return redirect(url_for("auth.login"))
    injuries = False
    # injuries = scrapeInjuries()
    return render_template("injuries.html", injuries=injuries, user=current_user)

@views.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        fName = request.form.get('first-name')
        lName = request.form.get('last-name')
        feedback = request.form.get('questions-concerns')
        bugs = request.form.get('bugs')
        
        print(f"{fName + ' ' + lName}\nFeedback: {feedback}\nBugs: {bugs}")
    return render_template("contact.html", user=current_user)


