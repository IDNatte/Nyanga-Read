from functools import wraps

from flask import request
from server.error.error import CSRFError
from server.helper.constant.constant import APP_ENV
from webview import token as wv_token


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

            elif APP_ENV == "dev":
                return function(*args, **kwargs)

            else:
                raise CSRFError("CSRFHeaderInvalid", "CSRF Header Invalid", 401)

        except KeyError:
            if KeyError:
                raise CSRFError("CSRFHeaderMissing", "CSRF Header Missing", 401)

    return verify_csrf_token
