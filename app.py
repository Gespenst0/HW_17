from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models import Movie, Movie_Schema, Director, Director_Schema, Genre, Genre_Schema
from utils import get_movies_by_genre, get_movies_by_director, get_movies_by_both_parameters

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


api = Api(app)
movies_ns = api.namespace('movies')
genres_ns = api.namespace('genres')
directors_ns = api.namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        director_schema = Director_Schema(many=True)
        directors = Director.query.all()
        if not directors:
            return "", 404
        return jsonify(director_schema.dump(directors))


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director_schema = Director_Schema()
        director = Director.query.get(did)
        if not director:
            return "", 404
        return jsonify(director_schema.dump(director))


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genre_schema = Genre_Schema(many=True)
        genres = Genre.query.all()
        if not genres:
            return "", 404
        return jsonify(genre_schema.dump(genres))


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        genre_schema = Genre_Schema()
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        movies = get_movies_by_genre(gid)
        list_titles = []
        for movie in movies:
            list_titles.append(movie["title"])
        if len(list_titles) == 0:
            list_titles = "Movies not found"
        result = genre_schema.dump(genre)
        result["Titles"] = list_titles
        return jsonify(result)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id and genre_id:
            return get_movies_by_both_parameters(director_id, genre_id)
        elif director_id:
            return get_movies_by_director(director_id)
        elif genre_id:
            return jsonify(get_movies_by_genre(genre_id))
        else:
            return get_movies_by_director(director_id)


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie_schema = Movie_Schema()
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        return jsonify(movie_schema.dump(movie))

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def patch(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        req_json = request.json
        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
