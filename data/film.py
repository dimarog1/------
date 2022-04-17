import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Film(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0)
    poster = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    frame_1 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    frame_2 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    frame_3 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    trailer = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    slogan = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    director = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scenario = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    producer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    operator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    composer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    designer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    montage = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    budget = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    fees_in_the_world = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    audience = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fees_in_russia = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    world_premiere = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    short_description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    long_description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    review_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
