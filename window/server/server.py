import logging
import mimetypes

from flask import Flask, current_app
from utils.resources import get_resources

from .config import config
from .controller import error, interface, ipc, main
from .helper.constant import constant
from .storage.model.bookmark import Bookmark
from .storage.model.read import Read
from .storage.model.settings import Setting


def create_app():
    # mimetype config
    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("text/css", ".css")

    # server instances
    server = Flask(__name__)
    server.config.from_object(config.Config)

    # storage
    constant.DB.init_app(server)

    # Logger
    logging.basicConfig(
        filename=get_resources("log/app.log"),
        level=logging.DEBUG,
        format="[%(name)s] [%(asctime)s] %(levelname)s : %(message)s",
    )

    # ipc blueprint
    server.register_blueprint(interface.interface_handler)
    server.register_blueprint(error.error_handler)
    server.register_blueprint(main.main_handler)
    server.register_blueprint(ipc.ipc_handler)

    return server
