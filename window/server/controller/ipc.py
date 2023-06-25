from flask import request as req
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import jsonify

from flask_cors import CORS

from server.middleware import verify_csrf
from server.middleware import verify_ua

from server.helper.constant import constant

from server.storage.model.bookmark import Bookmark
from server.storage.model.settings import Setting
from server.storage.model.read import Read

import requests

ipc_handler = Blueprint("ipc_ep", __name__, url_prefix="/ipc")

CORS(ipc_handler)


@ipc_handler.route("/init")
@verify_csrf
@verify_ua
def init():
    try:
        default_language = (
            Setting.query.filter_by(setting_type="language").one_or_none().to_dict()
        )

        default_content = (
            Setting.query.filter_by(setting_type="content").one_or_none().to_dict()
        )

        bookmarks = (
            Bookmark.query.order_by(Bookmark.bookmarked_at.desc()).limit(3).all()
        )

        daily = requests.get(
            f"https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&originalLanguage[]=ja&availableTranslatedLanguage[]={default_language.get('value')}&limit=3&offset=0&contentRating[]={default_content.get('value')}"
        )

        if daily.status_code == 200:
            return jsonify(
                {
                    "daily_manga": daily.json(),
                    "bookmark": {
                        "more": True if Bookmark.query.count() > 3 else False,
                        "bookmark_manga": [
                            requests.get(
                                f"https://api.mangadex.org/manga/{bookmark.to_dict().get('manga')}?includes[]=cover_art&includes[]=artist&includes[]=manga"
                            )
                            .json()
                            .get("data")
                            for bookmark in bookmarks
                        ],
                    },
                }
            )

        else:
            return jsonify({"status": "error", "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"status": "error", "location": "exception"})


@ipc_handler.route("/manga_list")
@verify_csrf
@verify_ua
def manga_lists():
    try:
        default_language = (
            Setting.query.filter_by(setting_type="language").one_or_none().to_dict()
        )

        default_content = (
            Setting.query.filter_by(setting_type="content").one_or_none().to_dict()
        )

        page = req.args.get("page", None)
        if page:
            limit = 9
            offset = (int(page) - 1) * int(limit)
            manga_list = requests.get(
                f"https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&originalLanguage[]=ja&availableTranslatedLanguage[]={default_language.get('value')}&contentRating[]={default_content.get('value')}&limit={limit}&offset={offset}",
            )

            if manga_list.status_code == 200:
                return jsonify({"daily_mangalists": manga_list.json()})

            else:
                return jsonify({"status": "error", "httpError": True})

        manga_list = requests.get(
            f"https://api.mangadex.org/manga?includes[]=cover_art&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&originalLanguage[]=ja&availableTranslatedLanguage[]={default_language.get('value')}&contentRating[]={default_content.get('value')}&limit=9&offset=0",
        )

        if manga_list.status_code == 200:
            return jsonify({"daily_mangalists": manga_list.json()})

        else:
            return jsonify({"status": "error", "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"status": "error", "location": "exception"})


@ipc_handler.route("/get_detail/<manga>")
@verify_csrf
@verify_ua
def get_manga_detail(manga):
    try:
        bookmarked = Bookmark.query.filter_by(manga=manga).one_or_none()

        latest_readed = (
            Read.query.filter_by(manga=manga).order_by(Read.readed_at.desc()).first()
        )

        default_language = (
            Setting.query.filter_by(setting_type="language").one_or_none().to_dict()
        )

        detail = requests.get(
            f"https://api.mangadex.org/manga/{manga}?includes[]=cover_art&includes[]=artist&includes[]=manga"
        )

        manga = requests.get(
            f"https://api.mangadex.org/manga/{manga}/aggregate?translatedLanguage[]={default_language.get('value')}"
        )

        manga = manga.json()

        if detail.status_code == 200:
            return jsonify(
                {
                    "last_read": latest_readed.to_dict() if latest_readed else None,
                    "detail_data": detail.json(),
                    "bookmarked": True if bookmarked is not None else False,
                    "manga_data": [
                        {
                            "chapter_id": manga.get("volumes")
                            .get(volume)
                            .get("chapters")
                            .get(chapter_number)
                            .get("id"),
                            "chapter": manga.get("volumes")
                            .get(volume)
                            .get("chapters")
                            .get(chapter_number)
                            .get("chapter"),
                        }
                        for volume in manga.get("volumes")
                        for chapter_number in manga.get("volumes")
                        .get(volume)
                        .get("chapters")
                    ],
                }
            )

        else:
            return jsonify({"status": "error", "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"status": "error", "location": "exception"})


@ipc_handler.route("/read_chapter/<chapter>")
@verify_csrf
@verify_ua
def read_chapter(chapter):
    try:
        chapter_data = requests.get(
            f"https://api.mangadex.org/at-home/server/{chapter}"
        )

        chapter_meta = requests.get(
            f"https://api.mangadex.org/chapter/{chapter}?includes[]=manga"
        )

        if chapter_data.status_code == 200 and chapter_meta.status_code == 200:
            # get chapter detail
            chapter_detail = chapter_meta.json().get("data")
            chapter_detail_manga = next(
                filter(
                    lambda x: x.get("type") == "manga",
                    chapter_detail.get("relationships"),
                )
            ).get("id")
            chapter_detail_id = chapter_detail.get("id")
            chapter_detail_number = chapter_detail.get("attributes").get("chapter")

            # save_read_history
            save_read_history = Read(
                manga=chapter_detail_manga,
                chapter=chapter_detail_id,
                chapter_number=chapter_detail_number,
            )
            constant.DB.session.add(save_read_history)
            constant.DB.session.commit()

            # exchange chapter image
            chapter_image = chapter_data.json()
            base_url = chapter_image.get("baseUrl")
            chapter_hash = chapter_image.get("chapter").get("hash")
            chapter_img_path = chapter_image.get("chapter").get("data")
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
            return jsonify({"status": "error", "httpError": True})

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"status": "error", "location": "exception"})


@ipc_handler.route("/search")
@verify_csrf
@verify_ua
def search():
    try:
        search_title = req.args.get("search", None)

        default_language = (
            Setting.query.filter_by(setting_type="language").one_or_none().to_dict()
        )

        default_content = (
            Setting.query.filter_by(setting_type="content").one_or_none().to_dict()
        )

        if search_title:
            search_manga = requests.get(
                f"https://api.mangadex.org/manga?title={search_title}&originalLanguage[]=ja&includes[]=cover_art&availableTranslatedLanguage[]={default_language.get('value')}&contentRating[]={default_content.get('value')}&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&limit=9&offset=0"
            )

            if search_manga.status_code == 200:
                return jsonify({"search_result": search_manga.json()})

            else:
                return jsonify({"status": "error", "httpError": True})
        else:
            return jsonify({"result": None})
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.Timeout,
    ) as _:
        return jsonify({"status": "error", "location": "exception"})


@ipc_handler.route("/bookmark", methods=["GET", "POST", "DELETE"])
@verify_csrf
@verify_ua
def bookmark():
    if req.method == "GET":
        page = req.args.get("page", None)

        if page:
            pass
        bookmark_data = Bookmark.query.all()

        return jsonify(
            {
                "bookmark": [
                    requests.get(
                        f"https://api.mangadex.org/manga/{bookmark.to_dict().get('manga')}?includes[]=cover_art&includes[]=artist&includes[]=manga"
                    )
                    .json()
                    .get("data")
                    for bookmark in bookmark_data
                ]
            }
        )
    if req.method == "POST":
        payload = req.get_json()

        if payload is not None or payload:
            if payload.get("mangaId") != None:
                bookmark_save = Bookmark(manga=payload.get("mangaId"))
                constant.DB.session.add(bookmark_save)
                constant.DB.session.commit()

                return {"status": "bookmarked", "message": "Bookmark Saved !"}

            else:
                return jsonify(
                    {
                        "status": "error",
                        "mangaIdError": True,
                        "message": "Something wen't error",
                    }
                )

        else:
            return jsonify(
                {
                    "status": "error",
                    "bodyError": True,
                    "message": "Something wen't error",
                }
            )

    if req.method == "DELETE":
        payload = req.get_json()

        if payload is not None or payload:
            if payload.get("mangaId") != None:
                bookmark_remove = Bookmark.query.filter_by(
                    manga=payload.get("mangaId")
                ).one_or_none()

                constant.DB.session.delete(bookmark_remove)
                constant.DB.session.commit()

                return {"status": "unbookmarked", "message": "Bookmark removed !"}

            else:
                return jsonify(
                    {
                        "status": "error",
                        "mangaIdError": True,
                        "message": "Something wen't error",
                    }
                )

        else:
            return jsonify(
                {
                    "status": "error",
                    "bodyError": True,
                    "message": "Something wen't error",
                }
            )

    return redirect(url_for("main.index"))


@ipc_handler.route("/settings", methods=["GET", "PATCH", "DELETE"])
# @verify_csrf
# @verify_ua
def settings():
    if req.method == "GET":
        settings = Setting.query.all()
        return jsonify(
            {
                "settings": [setting.to_dict() for setting in settings],
            }
        )

    if req.method == "PATCH":
        update_settings = req.args.get("settings", None)
        if update_settings:
            settings_value = req.args.get("value", None)
            if settings_value:
                update = Setting.query.get(int(update_settings))
                update.value = settings_value
                constant.DB.session.commit()
                return jsonify({"status": "changed"})
            return jsonify({"status": "noChanges"})

        return jsonify({"emptySettings": True})

    return redirect(url_for("main.index"))


@ipc_handler.route("/testing")
def testing():
    print("coba")

    return jsonify({"testing": True})
