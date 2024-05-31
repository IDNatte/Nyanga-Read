from flask import Blueprint
from flask import jsonify

from flask_cors import CORS

from nyanga.window.server.error.error import CSRFError
from nyanga.window.server.error.error import UAError

error_handler = Blueprint("error", __name__)

CORS(error_handler)


@error_handler.app_errorhandler(CSRFError)
@error_handler.app_errorhandler(UAError)
def app_error_handler(error):
    return (
        jsonify(
            {"status": error.name, "code": error.code, "detail": error.description}
        ),
        error.code,
    )
