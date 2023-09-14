from movie_rating_app import db
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }
    
    def __init__(self, username, password):
        self.username = username
        self.password_hash = password
    
    @hybrid_property
    def liked_movies(self):
        return [reaction.movie for reaction in self.movie_reactions if reaction.liked]
    
    @hybrid_property
    def hated_movies(self):
        return [reaction.movie for reaction in self.movie_reactions if reaction.hated]
