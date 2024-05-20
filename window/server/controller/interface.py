import concurrent

import requests
from flask import Blueprint, jsonify
from flask import request as req
from flask_cors import CORS
from server.middleware.verificator.agent import verify_ua
from server.storage.model.bookmark import Bookmark
from utils.parallel_request import parallelize_req
from utils.temp_attribute import NyangaTemporaryAttr

interface_handler = Blueprint("interface", __name__, url_prefix="/extension")

CORS(interface_handler)


INIT_REQUEST = True


@interface_handler.route("/status")
@verify_ua
def extension_access():
    global INIT_REQUEST

    if INIT_REQUEST:
        INIT_REQUEST = False
        return jsonify(
            {
                "open_by_extension": (
                    True
                    if NyangaTemporaryAttr.get_openmanga_id()
                    or NyangaTemporaryAttr.get_openbookmark()
                    else False
                ),
                "manga_id": NyangaTemporaryAttr.get_openmanga_id(),
                "goto_bookmark": (
                    True if NyangaTemporaryAttr.get_openbookmark() else False
                ),
            }
        )

    return jsonify(
        {"open_by_extension": False, "manga_id": None, "goto_bookmark": None}
    )


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


# @interface_handler.route("/my_manga")
# @verify_ua
# def my_manga():
#     my_manga_lists = Bookmark.query.order_by(Bookmark.bookmarked_at.desc()).all()

#     bookmark_link = [
#         f"https://api.mangadex.org/manga/{bookmark.to_dict().get('manga')}?includes[]=cover_art&includes[]=artist&includes[]=manga"
#         for bookmark in my_manga_lists
#     ]

#     with concurrent.futures.ThreadPoolExecutor() as parallelizer:
#         fu = [parallelizer.submit(parallelize_req, link) for link in bookmark_link]
#         concurrent.futures.wait(fu)

#     return jsonify([data.result().get("data") for data in fu])
