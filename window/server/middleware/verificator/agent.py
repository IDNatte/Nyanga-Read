from functools import wraps

from flask import request
from server.error.error import UAError
from server.helper.constant.constant import APP_ENV, EXTENSION_CLIENT, PYWEBVIEW_UA


def verify_ua(function):
    """
    verify user agent
    """

    @wraps(function)
    def verify_user_agent(*args, **kwargs):
        try:
            headers = request.headers["User-Agent"]
            if headers == PYWEBVIEW_UA or headers == EXTENSION_CLIENT:
                return function(*args, **kwargs)

            elif APP_ENV == "dev":
                return function(*args, **kwargs)

            else:
                raise UAError("UANotAccepted", "User Agent not accepted", 401)

        except Exception as _:
            raise UAError("UANotAccepted", "User Agent not accepted", 401)

    return verify_user_agent
