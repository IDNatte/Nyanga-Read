import os

from flask_sqlalchemy import SQLAlchemy

EXTENSION_CLIENT = "pyweview-client/0.1 pywebview-ext/0.0.1"
PYWEBVIEW_UA = "pywebview-client/1.0 pywebview-ui/3.0.0"
APP_ENV = os.environ.get("APP_ENV", default=None)
APP_EXT = os.environ.get("APP_EXT", default=None)
DB = SQLAlchemy()
