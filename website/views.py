from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from test import *
from .models import Favorite
from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/rankings", methods=['GET', 'POST'])
def rankings():
    if request.method == "POST":
        print(request.form)
        pos = request.form.get('select-pos')
        if pos:
            choice_map = {
                'QB': "passing",
                'RB': 'rushing',
                'WR': 'recieving',
                'Defense': 'Defense'
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

                db.session.add(new_fav)
                db.session.commit()
                print("worked")
            else:
                flash("Must login to add favorites.", category='error')
                return redirect(url_for('auth.login'))
        else:
            flash("An error has occured. Try again later.", category='error')

    return render_template("rankings.html", user=current_user)

@views.route("/favorites")
@login_required
def favorites():
    return render_template("favorites.html", user=current_user)

@views.route("/news")
def news():
    return render_template("news.html", user=current_user)


