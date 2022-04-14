from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data.review import Review
from data.db_session import db_sess
from data import db_session


parser = reqparse.RequestParser()
parser.add_argument('user', required=True)
parser.add_argument('film', required=True)
parser.add_argument('text', required=True)
parser.add_argument('mark', required=True)


def abort_if_review_not_found(review_id):
    session = db_session.create_session()
    review = session.query(Review).get(review_id)
    if not review:
        abort(404, message=f"Review {review_id} not found")


class ReviewResource(Resource):
    def get(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Review).get(review_id)
        return jsonify({'review': review.to_dict()})

    def delete(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Review).get(review_id)
        session.delete(review)
        session.commit()
        return jsonify({'success': 'OK'})


class ReviewListResource(Resource):
    def get(self):
        session = db_session.create_session()
        review = session.query(Review).all()
        return jsonify({'review': [item.to_dict() for item in review]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        review = Review(
            user=args['user'],
            film=args['film'],
            text=args['text'],
            mark=args['mark'],
        )
        session.add(review)
        session.commit()
        return jsonify({'success': 'OK'})