import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from flask_security import RoleMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(SqlAlchemyBase, RoleMixin):
    __tablename__ = 'role'

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(80), unique=True)
    description = sqlalchemy.Column(sqlalchemy.String(255))


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True)
    password = sqlalchemy.Column(sqlalchemy.String(255))
    active = sqlalchemy.Column(sqlalchemy.Boolean())
    confirmed_at = sqlalchemy.Column(sqlalchemy.DateTime())
    roles = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('role.id'))
    orm.relation('role')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)