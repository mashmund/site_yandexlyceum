import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.name"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    des = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    spher = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contact = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')


def __repr__(self):
    return self.job

