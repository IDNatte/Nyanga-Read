from flask import request
from functools import wraps
from webview import token as wv_token

from server.error import UAError
from server.error import CSRFError


import os

PYWEBVIEW_UA = "pywebview-client/1.0 pywebview-ui/3.0.0"
ui_dev = os.environ.get("UI_APP_DEV", default=None)


def verify_csrf(function):
    """
    verify csrf token
    """

    @wraps(function)
    def verify_csrf_token(*args, **kwargs):
        try:
            token_header = request.headers["PCSRFWV-Token"]

            if token_header == wv_token:
                return function(*args, **kwargs)

            elif token_header != wv_token:
                raise CSRFError("CSRFHeaderInvalid", "CSRF Header Invalid", 401)

        except KeyError:
            if KeyError:
                raise CSRFError("CSRFHeaderMissing", "CSRF Header Missing", 401)

    return verify_csrf_token


def verify_ua(function):
    """
    verify user agent
    """

    @wraps(function)
    def verify_user_agent(*args, **kwargs):
        try:
            headers = request.headers["User-Agent"]
            if headers == PYWEBVIEW_UA:
                return function(*args, **kwargs)

            else:
                raise UAError("UANotAccepted", "User Agent not accepted", 401)
        except:
            raise UAError("UANotAccepted", "User Agent not accepted", 401)

    return verify_user_agent
