from flask import jsonify
from movie_rating_app import db
from movie_rating_app.models.user import User


def get_user(id):
    user = db.get_or_404(User, id)
    return user

def get_user_by_username(username):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
    return user

def store_user(user):
    db.session.add(user)
    db.session.commit()