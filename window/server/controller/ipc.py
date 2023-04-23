from flask import Blueprint
from flask_cors import CORS
from flask import jsonify


from server.middleware import verify_csrf
from server.middleware import verify_ua

ipc_handler = Blueprint("ipc_ep", __name__, url_prefix="/ipc")

CORS(ipc_handler)


@ipc_handler.before_request
@verify_csrf
@verify_ua
def csrf_checker():
    """
    accomodating every incoming request csrf verification header with middleware
    """
    pass


@ipc_handler.route("/testing")
def testing():
    return jsonify({"testing": True})
