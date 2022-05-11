from flask import jsonify
from models import Movie, Movie_Schema


def get_movies_by_director(director_id=None):
    movies_schema = Movie_Schema(many=True)
    if director_id:
        movies = Movie.query.filter(Movie.director_id == director_id)
    else:
        movies = Movie.query.all()
    return jsonify(movies_schema.dump(movies))


def get_movies_by_genre(genre_id):
    movies_schema = Movie_Schema(many=True)
    movies = Movie.query.filter(Movie.genre_id == genre_id)
    return movies_schema.dump(movies)


def get_movies_by_both_parameters(director_id, genre_id):
    movies_schema = Movie_Schema(many=True)
    movies = Movie.query.filter(Movie.genre_id == genre_id).filter(Movie.director_id == director_id)
    return jsonify(movies_schema.dump(movies))
