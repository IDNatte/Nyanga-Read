from flask import send_from_directory
from flask import Blueprint
from flask import jsonify

from webview import token as w_token
from flask_cors import CORS

from server.middleware import verify_csrf
from server.middleware import verify_ua
from utils import get_resources


main_handler = Blueprint("main", __name__, static_folder=get_resources("layout"))

CORS(main_handler)


@main_handler.before_app_request
@verify_ua
def before_request():
    pass


@main_handler.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pywebview-Csrf-Token"] = w_token
    return response


@main_handler.route("/init")
def init():
    return jsonify({"csrf_token": w_token})


@main_handler.route("/")
def index():
    return send_from_directory(main_handler.static_folder, "index.html")


@main_handler.route("/", defaults={"path": ""})
@main_handler.route("/<path:path>")
def catch_all(path):
    return send_from_directory(main_handler.static_folder, path)
