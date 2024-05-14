from functools import wraps

from flask import request
from server.error.error import UAError
from server.helper.constant.constant import APP_DEV, EXTENSION_CLIENT, PYWEBVIEW_UA


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

            if headers == EXTENSION_CLIENT:
                return function(*args, **kwargs)

            if headers != EXTENSION_CLIENT or headers != PYWEBVIEW_UA:
                raise UAError("UANotAccepted", "User Agent not accepted", 401)
        except Exception as _:
            raise UAError("UANotAccepted", "User Agent not accepted", 401)

    return verify_user_agent
