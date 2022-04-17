from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data.film import Film
from data.db_session import db_sess
from data import db_session


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('year', required=True)
parser.add_argument('country', required=True)
parser.add_argument('genre', required=True)
parser.add_argument('slogan', required=True)
parser.add_argument('director', required=True)
parser.add_argument('scenario', required=True)
parser.add_argument('producer', required=True)
parser.add_argument('operator', required=True)
parser.add_argument('composer', required=True)
parser.add_argument('designer', required=True)
parser.add_argument('montage', required=True)
parser.add_argument('budget', required=True)
parser.add_argument('fees_in_the_world', required=True)
parser.add_argument('audience', required=True)
parser.add_argument('fees_in_russia', required=True)
parser.add_argument('world_premiere', required=True)
parser.add_argument('age', required=True)
parser.add_argument('time', required=True)
parser.add_argument('short_description', required=True)
parser.add_argument('long_description', required=True)


def abort_if_film_not_found(film_id):
    session = db_session.create_session()
    film = session.query(Film).get(film_id)
    if not film:
        abort(404, message=f"Film {film_id} not found")


class FilmResource(Resource):
    def get(self, film_id):
        abort_if_film_not_found(film_id)
        session = db_session.create_session()
        film = session.query(Film).get(film_id)
        return jsonify({'film': film.to_dict(
            only=(
                'title',
                'year',
                'country',
                'genre',
                'slogan',
                'director',
                'scenario',
                'producer',
                'operator',
                'composer',
                'designer',
                'montage',
                'budget',
                'fees_in_the_world',
                'audience',
                'fees_in_russia',
                'world_premiere',
                'age',
                'time',
                'short_description',
                'long_description',
            )
        )})

    def delete(self, film_id):
        abort_if_film_not_found(film_id)
        session = db_session.create_session()
        film = session.query(Film).get(film_id)
        session.delete(film)
        session.commit()
        return jsonify({'success': 'OK'})


class FilmListResource(Resource):
    def get(self):
        session = db_session.create_session()
        film = session.query(Film).all()
        return jsonify({'film': [item.to_dict() for item in film]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        film = Film(
            title=args['title'],
            poster=args['poster'],
            trailer=args['trailer'],
            year=args['year'],
            country=args['country'],
            genre=args['genre'],
            slogan=args['slogan'],
            director=args['director'],
            scenario=args['scenario'],
            producer=args['producer'],
            operator=args['operator'],
            composer=args['composer'],
            designer=args['designer'],
            montage=args['montage'],
            budget=args['budget'],
            fees_in_the_world=args['fees_in_the_world'],
            audience=args['audience'],
            fees_in_russia=args['fees_in_russia'],
            world_premiere=args['world_premiere'],
            age=args['age'],
            time=args['time'],
            short_description=args['short_description'],
            long_description=args['long_description'],
        )
        session.add(film)
        session.commit()
        return jsonify({'success': 'OK'})