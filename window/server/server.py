from utils.resources import get_resources
from flask import current_app
from flask import Flask

from .helper.constant import constant
from .config import config

from .storage.model.bookmark import Bookmark
from .storage.model.settings import Setting
from .storage.model.read import Read

from .controller import interface
from .controller import error
from .controller import main
from .controller import ipc

import mimetypes
import logging


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
