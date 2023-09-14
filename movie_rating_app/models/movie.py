import datetime
from movie_rating_app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_of_publication = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Define the relationship to the User model
    user = db.relationship('User', backref='movies')

    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.user = user
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user": self.user_id,
            "date_of_publication": self.date_of_publication
        }
    
    @hybrid_property
    def likes_count(self):
        return len([reaction for reaction in self.movie_reactions if reaction.liked])
    
    @hybrid_property
    def hates_count(self):
        return len([reaction for reaction in self.movie_reactions if reaction.hated])