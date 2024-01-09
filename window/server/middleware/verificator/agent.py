from functools import wraps
from flask import request

from server.helper.constant.constant import EXTENSION_CLIENT
from server.helper.constant.constant import PYWEBVIEW_UA
from server.helper.constant.constant import APP_DEV
from server.error.error import UAError


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

            else:
                raise UAError("UANotAccepted", "User Agent not accepted", 401)
        except:
            raise UAError("UANotAccepted", "User Agent not accepted", 401)

    return verify_user_agent
