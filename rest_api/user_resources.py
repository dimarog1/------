from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data.user import User
from data.db_session import db_sess
from data import db_session


parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('nickname', required=True)
parser.add_argument('roles', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict() for item in user]})