from flask_cors import CORS
from flask import Blueprint
from flask import jsonify

from server.middleware import verify_csrf
from server.middleware import verify_ua

import requests

ipc_handler = Blueprint("ipc_ep", __name__, url_prefix="/ipc")

CORS(ipc_handler)


@ipc_handler.route("/init")
@verify_csrf
@verify_ua
def init():
    try:
        daily = requests.get(
            "https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&limit=3&originalLanguage[]=ja"
        )

        if daily.status_code == 200:
            return jsonify({"daily_data": daily.json()})

        else:
            return jsonify({"error": True, "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as e:
        print(e)
        return jsonify({"error": True, "location": "exception"})


@ipc_handler.route("/testing")
@verify_csrf
@verify_ua
def testing():
    return jsonify({"testing": True})
