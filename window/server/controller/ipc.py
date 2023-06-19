from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request as req

from server.middleware import verify_csrf
from server.middleware import verify_ua

import requests

ipc_handler = Blueprint("ipc_ep", __name__, url_prefix="/ipc")

CORS(ipc_handler)


@ipc_handler.route("/init")
# @verify_csrf
# @verify_ua
def init():
    try:
        daily = requests.get(
            "https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&originalLanguage[]=ja&availableTranslatedLanguage[]=en&limit=3&offset=0"
        )

        if daily.status_code == 200:
            return jsonify({"daily_data": daily.json()})

        else:
            return jsonify({"error": True, "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"error": True, "location": "exception"})


@ipc_handler.route("/manga_list")
# @verify_csrf
# @verify_ua
def manga_lists():
    try:
        page = req.args.get("page", None)
        if page:
            limit = 9
            offset = (int(page) - 1) * int(limit)
            manga_list = requests.get(
                f"https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&originalLanguage[]=ja&availableTranslatedLanguage[]=en&limit={limit}&offset={offset}",
            )

            if manga_list.status_code == 200:
                return jsonify({"daily_mangalists": manga_list.json()})

            else:
                return jsonify({"error": True, "httpError": True})

        manga_list = requests.get(
            "https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&originalLanguage[]=ja&availableTranslatedLanguage[]=en&limit=9&offset=0",
        )

        if manga_list.status_code == 200:
            return jsonify({"daily_mangalists": manga_list.json()})

        else:
            return jsonify({"error": True, "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"error": True, "location": "exception"})


@ipc_handler.route("/get_detail/<manga>")
# @verify_csrf
# @verify_ua
def get_manga_detail(manga):
    try:
        detail = requests.get(
            f"https://api.mangadex.org/manga/{manga}?includes[]=cover_art&?includes[]=manga"
        )

        manga = requests.get(
            f"https://api.mangadex.org/manga/{manga}/aggregate?translatedLanguage[]=en"
        )
        manga = manga.json()
        mangaData = []

        for volume in manga.get("volumes"):
            chapter = manga.get("volumes").get(volume).get("chapters")
            for chapter_number in chapter:
                mangaData.append(
                    {
                        "chapter_id": chapter.get(chapter_number).get("id"),
                        "chapter": chapter.get(chapter_number).get("chapter"),
                    }
                )

        if detail.status_code == 200:
            return jsonify({"detail_data": detail.json(), "manga_data": mangaData})

        else:
            return jsonify({"error": True, "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"error": True, "location": "exception"})


@ipc_handler.route("/read_chapter/<chapter>")
# @verify_csrf
# @verify_ua
def read_chapter(chapter):
    try:
        chapter_data = requests.get(
            f"https://api.mangadex.org/at-home/server/{chapter}"
        )
        if chapter_data.status_code == 200:
            chapter = chapter_data.json()
            base_url = chapter.get("baseUrl")
            chapter_hash = chapter.get("chapter").get("hash")
            chapter_img_path = chapter.get("chapter").get("data")
            chapter_img = []
            for index, chapter_filename in enumerate(chapter_img_path):
                chapter_img.append(
                    {
                        "url": f"{base_url}/data/{chapter_hash}/{chapter_filename}",
                        "chapterNumber": int(index + 1),
                        "index": int(index),
                    }
                )
            return jsonify(chapter_img)

        else:
            return jsonify({"error": True, "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"error": True, "location": "exception"})


@ipc_handler.route("/search")
# @verify_csrf
# @verify_ua
def search():
    try:
        search_title = req.args.get("search", None)
        if search_title:
            search_manga = requests.get(
                f"https://api.mangadex.org/manga?title={search_title}&originalLanguage[]=ja&includes[]=cover_art&availableTranslatedLanguage[]=en&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&limit=9&offset=0"
            )

            if search_manga.status_code == 200:
                return jsonify({"search_result": search_manga.json()})

            else:
                return jsonify({"error": True, "httpError": True})
        else:
            return jsonify({"result": None})
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"error": True, "location": "exception"})


@ipc_handler.route("/testing")
# @verify_csrf
# @verify_ua
def testing():
    return jsonify({"testing": True})
