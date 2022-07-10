import sqlalchemy

from database import database


class RandomValue(database.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.now())
    value = sqlalchemy.Column(sqlalchemy.Integer)