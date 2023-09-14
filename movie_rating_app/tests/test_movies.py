import pytest

from movie_rating_app import db
from movie_rating_app.models.movie import Movie


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"movie1" in response.data
    assert b"movie2" in response.data
    assert b"New" in response.data

    assert b"<form method=\"GET\" action=\"/like/1\">" not in response.data # cannot like his movie
    assert b"<form method=\"GET\" action=\"/like/2\">" in response.data


def test_movies_from_user(client, auth):
    auth.login(username="other-test")
    response = client.get("/user/test")
    assert b"movie1" in response.data
    assert b"movie2" not in response.data


@pytest.mark.parametrize("path", ("/create", "/like/1", "/hate/1"))
def test_login_required(client, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"


def test_like(client, auth, app):
    auth.login()
    response = client.get("/like/2")
    assert response.status_code == 302 # redirect

    with app.app_context():
        movie2 = db.session.execute(db.select(Movie).filter_by(title="movie2")).scalar_one()
        likes = movie2.likes_count
        assert likes == 1


def test_hate(client, auth, app):
    auth.login()
    response = client.get("/hate/2")
    assert response.status_code == 302 # redirect

    with app.app_context():
        movie2 = db.session.execute(db.select(Movie).filter_by(title="movie2")).scalar_one()
        hates = movie2.hates_count
        assert hates == 1


def test_toggle_like_hate(client, auth, app):
    auth.login()
    response = client.get("/hate/2")
    assert response.status_code == 302 # redirect

    with app.app_context():
        movie2 = db.session.execute(db.select(Movie).filter_by(title="movie2")).scalar_one()
        hates = movie2.hates_count
        likes = movie2.likes_count

        assert hates == 1
        assert likes == 0    
    
    response = client.get("/like/2")
    assert response.status_code == 302 # redirect

    with app.app_context():
        movie2 = db.session.execute(db.select(Movie).filter_by(title="movie2")).scalar_one()
        likes = movie2.likes_count
        hates = movie2.hates_count

        assert likes == 1
        assert hates == 0


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "description": ""})

    with app.app_context():
        count = Movie.query.count()
        assert count == 3




