from movie_rating_app import db

class MovieReaction(db.Model):
    __tablename__ = 'movie_reactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    liked = db.Column(db.Boolean)
    hated = db.Column(db.Boolean)


    # Define relationships to User and Movie models
    user = db.relationship('User', backref='movie_reactions')
    movie = db.relationship('Movie', backref='movie_reactions')

    def __init__(self, user, movie, liked=False, hated=False):
        self.user = user
        self.movie = movie
        self.liked = liked
        self.hated = hated