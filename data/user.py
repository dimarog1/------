import sqlalchemy
from sqlalchemy import orm, Integer, ForeignKey

from .db_session import SqlAlchemyBase
from flask_security import RoleMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column


class RolesUsers(SqlAlchemyBase):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(SqlAlchemyBase, RoleMixin):
    __tablename__ = 'role'

    id = Column(sqlalchemy.Integer(), primary_key=True)
    name = Column(sqlalchemy.String(80), unique=True)
    description = Column(sqlalchemy.String(255))


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = Column(sqlalchemy.Integer, primary_key=True)
    email = Column(sqlalchemy.String(255), unique=True)
    nickname = Column(sqlalchemy.String(255))
    password = Column(sqlalchemy.String(255))
    active = Column(sqlalchemy.Boolean())
    confirmed_at = Column(sqlalchemy.DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))