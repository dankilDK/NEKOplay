import sqlalchemy
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    discord_id = sqlalchemy.Column(sqlalchemy.String)
    cf_handle = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorite1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorite2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorite3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorite4 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorite5 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
