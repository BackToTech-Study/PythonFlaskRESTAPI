from api.models.random_value import RandomValue
from api.models.random_value_transfer_object import RandomValueTransferObject


def random_value_to_transfer_object(dbo):
    transferObject = RandomValueTransferObject()
    transferObject.date = dbo.date
    transferObject.value = dbo.value
    return transferObject


def transfer_object_to_random_value(transferObject):
    dbo = RandomValue()
    dbo.date = transferObject.date
    dbo.value = transferObject.value
    return dbo
