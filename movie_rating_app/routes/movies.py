from operator import attrgetter
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from movie_rating_app.routes.auth import login_required
from movie_rating_app.models.movie import Movie
from movie_rating_app.controller.access_movies import *
from movie_rating_app.controller.access_movie_reactions import *
from movie_rating_app.controller.acess_user import *

bp = Blueprint("movies", __name__)


@bp.route("/")
def index(movies=None):
    user = g.user
    movies = movies or get_all_movies()
    sort_field = request.args.get('sort', 'date_of_publication')

    # Sort the list of items based on the chosen field
    sorted_movies = sorted(movies, key=attrgetter(sort_field), reverse=True)

    return render_template("index.html", movies=sorted_movies, current_user=user)


@bp.route("/user/<string:username>")
def movies_from_user(username):
    user = g.user
    movies = get_all_movies_for_user(username)
    return render_template("index.html", movies=movies, current_user=user)


@bp.route("/like/<int:id>")
@login_required
def toggle_like_movie(id):
    user = g.user
    movie = get_movie(id)

    reaction = get_user_reaction_for_movie(user, movie)
    if reaction is None:
        reaction = MovieReaction(user, movie, liked=True)
        store_movie_reaction(reaction)
    else:
        reaction.liked = not reaction.liked
        if reaction.liked:
            reaction.hated = False

        update_reaction(reaction)

    return redirect("/")


@bp.route("/hate/<int:id>")
@login_required
def toggle_hate_movie(id):
    user = g.user
    movie = get_movie(id)

    reaction = get_user_reaction_for_movie(user, movie)
    if reaction is None:
        reaction = MovieReaction(user, movie, hated=True)
        store_movie_reaction(reaction)
    else:
        reaction.hated = not reaction.hated
        if reaction.hated:
            reaction.liked = False
        update_reaction(reaction)
    return redirect("/")


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            movie = Movie(title, description, g.user)
            store_movie(movie)
            return redirect(url_for("movies.index"))

    return render_template("/create.html")
