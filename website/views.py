from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/rankings")
def rankings():
    return render_template("rankings.html", user=current_user)

@views.route("/favorites")
@login_required
def favorites():
    return render_template("favorites.html", user=current_user)

@views.route("/news")
def news():
    return render_template("news.html", user=current_user)


