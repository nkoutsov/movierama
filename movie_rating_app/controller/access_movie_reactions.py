from flask import jsonify
from movie_rating_app import db
from movie_rating_app.models.movie_reaction import MovieReaction

def get_reactions_for_movie(movie):
    reactions = db.session.execute(db.select(MovieReaction).where(MovieReaction.movie==movie)).scalars()
    return reactions

def store_movie_reaction(reaction):
    db.session.add(reaction)
    db.session.commit()

def get_user_reaction_for_movie(user, movie):
    reaction = db.session.execute(db.select(MovieReaction).filter_by(user=user, movie=movie)).scalar()
    return reaction

def update_reaction(reaction):
    db.session.commit()