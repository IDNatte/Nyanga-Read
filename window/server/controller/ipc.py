from flask_cors import CORS
from flask import Blueprint
from flask import jsonify


from server.middleware import verify_csrf
from server.middleware import verify_ua

ipc_handler = Blueprint("ipc_ep", __name__, url_prefix="/ipc")

CORS(ipc_handler)


@ipc_handler.route("/testing")
@verify_ua
@verify_csrf
def testing():
    return jsonify({"testing": True})
