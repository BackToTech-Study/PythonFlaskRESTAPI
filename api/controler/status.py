import http
from datetime import datetime

from flask import Blueprint

# Define the blueprint
# the url_prefix parameter is optional
status = Blueprint('status', __name__)


# When you bind a function with the help of the decorator,
# the blueprint will record the intention of registering the function on the application when it’s later registered.
@status.route('/now', methods=['GET'])
def echo():
    return str(datetime.now()), http.HTTPStatus.OK
