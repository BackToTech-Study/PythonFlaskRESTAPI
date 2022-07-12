import http

import jsonpickle
from flask import Blueprint, request


from api.models.random_value_transfer_object import RandomValueTransferObject
from api.services.random_value_repository import RandomValueRepository

value = Blueprint('value', __name__)


@value.route('/save', methods=['POST'])
def save(repository: RandomValueRepository):
    newVal = request.get_json()
    result = repository.save(RandomValueTransferObject(**newVal))
    return jsonpickle.encode(result, unpicklable=False), http.HTTPStatus.OK


@value.route('/get', methods=['GET'])
def getRecipes(repository: RandomValueRepository):
    parameterName = 'page'
    try:
        page = int(request.args.get(parameterName, default=1))
    except ValueError:
        return f'Invalid parameter {parameterName}', http.HTTPStatus.BAD_REQUEST

    parameterName = 'pageSize'
    try:
        pageSize = int(request.args.get(parameterName, default=10))
    except ValueError:
        return f'Invalid parameter {parameterName}', http.HTTPStatus.BAD_REQUEST

    result = repository.get_all(page, pageSize)
    return jsonpickle.encode(result, unpicklable=False), http.HTTPStatus.OK
