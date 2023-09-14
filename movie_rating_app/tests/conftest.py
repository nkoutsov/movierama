import pytest

from movie_rating_app import create_app, db
from movie_rating_app.models.movie import Movie
from movie_rating_app.models.user import User
from werkzeug.security import generate_password_hash



@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    db_url = "sqlite:///:memory:"
    # create the app with common test config
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": db_url})

    # create the database and load test data
    with app.app_context():
        load_data()

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


def load_data():
    user = User("test", generate_password_hash("test"))
    other_user = User("other-test", generate_password_hash("test"))

    movie1 = Movie("movie1", "description1", user)
    movie2 = Movie("movie2", "description2", other_user)

    db.session.add_all([user, other_user, movie1, movie2])
    db.session.commit()