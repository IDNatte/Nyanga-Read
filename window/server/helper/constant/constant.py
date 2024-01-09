from flask_sqlalchemy import SQLAlchemy
import os

EXTENSION_CLIENT = "pyweview-client/0.1 pywebview-cl/0.0.1"
PYWEBVIEW_UA = "pywebview-client/1.0 pywebview-ui/3.0.0"
APP_DEV = os.environ.get("APP_DEV", default=None)
DB = SQLAlchemy()
