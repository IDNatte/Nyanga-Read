from flask_cors import CORS
from flask import Blueprint
from flask import jsonify

from server.middleware.verificator.csrf import verify_csrf
from server.middleware.verificator.agent import verify_ua

from webview import token as wv_token

interface_handler = Blueprint("interface", __name__, url_prefix="/extension")

CORS(interface_handler)


@interface_handler.route("/get_csrf")
@verify_ua
def extension_get_csrf():
    return jsonify({"token": wv_token})


@interface_handler.route("/coba_csrf")
@verify_csrf
@verify_ua
def search_manga():
    return jsonify({"accsess": "accepted"})
