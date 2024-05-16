import concurrent

import requests
from flask import Blueprint, jsonify
from flask import request as req
from flask_cors import CORS
from server.helper.constant.constant import APP_EXT
from server.middleware.verificator.agent import verify_ua
from server.storage.model.bookmark import Bookmark
from utils.parallel_request import parallelize_req
from utils.temp_attribute import NyangaTemporaryAttr

interface_handler = Blueprint("interface", __name__, url_prefix="/extension")

CORS(interface_handler)


@interface_handler.route("/status")
@verify_ua
def extension_access():
    # print(f"{}")

    # if APP_EXT == "extension":
    #     return jsonify({"is_extension": True})

    return jsonify(
        {"open_manga": True, "manga_id": NyangaTemporaryAttr.get_openmanga_id()}
    )


@interface_handler.route("/search_manga")
@verify_ua
def search_manga():
    manga_title = req.args.get("title", None)
    print(f"{NyangaTemporaryAttr.get_openmanga_id()}")

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


# @TODO make opener for manga from ulauncher in here (how ?)
@interface_handler.route("/openmanga/<mangaid>")
@verify_ua
def openmanga(mangaid):
    return jsonify({"hello": "world"})
