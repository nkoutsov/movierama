import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def close_db(e=None):
    db.session.remove()
    db.engine.dispose()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = 'postgres:5432'
    db_name = 'movies'

    # Construct the PostgreSQL database URL
    db_url = f'postgresql://{db_username}:{db_password}@{db_host}/{db_name}'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import auth, movies
    app.register_blueprint(auth.bp)
    app.register_blueprint(movies.bp)

    with app.app_context():
        from .models import user, movie
        db.create_all()

    app.add_url_rule('/', endpoint='index')
    
    return app
