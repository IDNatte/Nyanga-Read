from flask import Flask, send_from_directory
from utils import get_resources
import logging

server = Flask(__name__, static_folder=get_resources("layout"))

logging.basicConfig(
    filename=get_resources("log/app.log"),
    level=logging.DEBUG,
    format="[%(name)s] [%(asctime)s] %(levelname)s : %(message)s",
)


@server.route("/")
def index():
    return send_from_directory(server.static_folder, "index.html")


@server.route("/", defaults={"path": ""})
@server.route("/<path:path>")
def catch_all(path):
    return send_from_directory(server.static_folder, path)
