from flask import send_from_directory
from flask import render_template
from flask import Blueprint

from webview import token as w_token
from flask_cors import CORS

from server.middleware import verify_ua
from utils import get_resources


main_handler = Blueprint(
    "main",
    __name__,
    static_folder=get_resources("layout"),
    template_folder=get_resources("layout"),
)

CORS(main_handler)


@main_handler.before_request
@verify_ua
def before_request():
    pass


@main_handler.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@main_handler.route("/")
def index():
    return render_template("index.html", token=w_token)


@main_handler.route("/", defaults={"path": ""})
@main_handler.route("/<path:path>")
def catch_all(path):
    return send_from_directory(main_handler.static_folder, path)
