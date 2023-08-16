from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from test import *
from .models import Favorite
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/rankings", methods=['GET', 'POST'])
def rankings():
    if request.method == "POST":
        pos = request.form.get('select-pos')
        if pos:
            choice_map = {
                'QB': "passing",
                'RB': 'rushing',
                'WR': 'recieving',
                'DEF': 'interceptions'
            }

            if pos in choice_map:
                players = scrape(choice_map[pos])
                return render_template("rankings.html", players=players, user=current_user)
            
        playerString = request.form.get('add-fav')
        if playerString:
            if current_user.is_authenticated:
                ind = playerString.index(":")
                name = playerString[0:ind]
                ppg = float(playerString[ind+1:])

                new_fav = Favorite(name=name, ppg=ppg, user_id=current_user.id)

                try: 
                    db.session.add(new_fav)
                    db.session.commit()
                    flash("Successfully added to favorites.", category="success")
                except Exception:
                    flash("Error. Please Try again later", category='error')
            else:
                flash("Must login to add favorites.", category='error')
                return redirect(url_for('auth.login'))
        else:
            flash("An error has occured. Try again later.", category='error')

    return render_template("rankings.html", user=current_user)

@views.route("/favorites", methods=['GET', 'POST'])
@login_required
def favorites():
    favs = Favorite.query.filter_by(user_id=current_user.id)
    # if request.method == "POST":
    #     name_to_del = request.form.get('del-fav')
    return render_template("favorites.html", user=current_user, favorites=favs)

@views.route('delete-fav', methods=['POST'])
def delete_fav():
    fav = json.loads(request.data)
    favId = fav['favId']
    fav = Favorite.query.get(favId)
    if fav:
        print(fav.user_id)
        print(current_user.id)
        if fav.user_id == current_user.id:
            db.session.delete(fav)
            db.session.commit()
            print(fav)
            
            
    return jsonify({})

@views.route("/news")
def news():
    return render_template("news.html", user=current_user)


