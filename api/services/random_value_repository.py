from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject

from api.models.random_value import RandomValue
from api.models.random_value_collection import RandomValueCollection
from api.models.random_value_transfer_object import RandomValueTransferObject
from api.services.random_value_mapper import random_value_to_transfer_object, transfer_object_to_random_value


class RandomValueRepository:
    @inject
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def save(self, newValue: RandomValueTransferObject):
        dbo = transfer_object_to_random_value(newValue)
        self.__database.session.add(dbo)
        self.__database.session.commit()
        return random_value_to_transfer_object(dbo)

    def get_all(self, page: int, pageSize: int):
        totalNumberOfItems = RandomValue.query.count()
        collection = RandomValue.query.paginate(page, pageSize, error_out=False)
        return RandomValueCollection(list(map(lambda dbo: random_value_to_transfer_object(dbo), collection.items)), page, pageSize, totalNumberOfItems)
