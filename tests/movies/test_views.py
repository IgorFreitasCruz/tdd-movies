import json

import pytest

from movies.models import Movie
from .conftest import add_movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 3

    resp = client.post(
        "/api/movies/",
        {
            "title": "Vanila Sky",
            "genre": "thriller",
            "year": "2001"
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "Vanila Sky"

    movies = Movie.objects.all()
    assert len(movies) == 4


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 3

    resp = client.post(
        "/api/movies/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 3


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 3

    resp = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 3


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "The Big Lebowski"


def test_get_single_movie_incorrect_id(client):
    resp = client.get(f"/api/movies/foo/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="Fargo", genre="action", year="2003")
    movie_two = add_movie("No Country for Old Men", "sci-fi", "2014")
    resp = client.get(f"/api/movies/")
    print(resp.data, flush=True)
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title