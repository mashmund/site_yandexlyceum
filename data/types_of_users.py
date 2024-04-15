import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Types(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'types_of_users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                            primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('Type', backref='types_of_users')
