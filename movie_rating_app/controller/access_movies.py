from flask import jsonify
from movie_rating_app import db
from movie_rating_app.models.movie import Movie
from movie_rating_app.models.user import User
from movie_rating_app.models.movie_reaction import MovieReaction

def get_all_movies():
    movies = db.session.execute(db.select(Movie).order_by(Movie.date_of_publication.desc())).scalars()
    return movies

def get_movie(id):
    movie = db.get_or_404(Movie, id)
    return movie

def store_movie(movie):
    db.session.add(movie)
    db.session.commit()


def get_all_movies_for_user(username):
    query = (
        db.select(Movie)
        .join(Movie.user)
        .filter(User.username == username)
        .order_by(Movie.date_of_publication)
    )
    return db.session.execute(query).scalars()