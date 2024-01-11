from flask import request as req
from flask import Blueprint
from flask import jsonify

from flask_cors import CORS

from server.middleware.verificator.agent import verify_ua
from server.storage.model.bookmark import Bookmark
from utils.parallel_request import parallelize_req

import concurrent
import requests

interface_handler = Blueprint("interface", __name__, url_prefix="/extension")

CORS(interface_handler)


@interface_handler.route("/search_manga")
@verify_ua
def search_manga():
    manga_title = req.args.get("title", None)

    try:
        fetcher = requests.get(
            f"https://api.mangadex.org/manga?title={manga_title}&originalLanguage[]=ja&includes[]=cover_art&availableTranslatedLanguage[]=en&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&limit=10&offset=0"
        )

        if fetcher.status_code == 200:
            return jsonify(fetcher.json().get("data"))

        else:
            return jsonify({"status": "error", "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"status": "error", "location": "exception"})


@interface_handler.route("/my_manga")
@verify_ua
def my_manga():
    my_manga_lists = Bookmark.query.order_by(Bookmark.bookmarked_at.desc()).all()

    bookmark_link = [
        f"https://api.mangadex.org/manga/{bookmark.to_dict().get('manga')}?includes[]=cover_art&includes[]=artist&includes[]=manga"
        for bookmark in my_manga_lists
    ]

    with concurrent.futures.ThreadPoolExecutor() as parallelizer:
        fu = [parallelizer.submit(parallelize_req, link) for link in bookmark_link]
        concurrent.futures.wait(fu)

    return jsonify([data.result().get("data") for data in fu])
