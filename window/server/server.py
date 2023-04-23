from utils import get_resources
from flask import Flask
import logging

from .controller import main
from .controller import error
from .controller import ipc

import mimetypes


def create_app():
    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("text/css", ".css")
    server = Flask(__name__)
    server.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

    logging.basicConfig(
        filename=get_resources("log/app.log"),
        level=logging.DEBUG,
        format="[%(name)s] [%(asctime)s] %(levelname)s : %(message)s",
    )

    server.register_blueprint(main.main_handler)
    server.register_blueprint(error.error_handler)
    server.register_blueprint(ipc.ipc_handler)

    return server
