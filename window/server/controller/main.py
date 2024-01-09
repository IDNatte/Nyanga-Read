from flask import send_from_directory
from flask import render_template
from flask import Blueprint

from webview import token as w_token
from flask_cors import CORS

from server.middleware.verificator.agent import verify_ua
from server.storage.model.settings import Setting
from utils.resources import get_resources


main_handler = Blueprint(
    "main",
    __name__,
    static_folder=get_resources("layout"),
    template_folder=get_resources("layout"),
)

CORS(main_handler)


@main_handler.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-store"
    response.headers["Expires"] = "0"
    return response


@main_handler.route("/")
@verify_ua
def index():
    language = Setting.query.filter_by(setting_type="language").one_or_none()
    return render_template("index.html", token=w_token, lang=language.value)


@main_handler.route("/", defaults={"path": ""})
@main_handler.route("/<path:path>")
@verify_ua
def catch_all(path):
    return send_from_directory(main_handler.static_folder, path)
