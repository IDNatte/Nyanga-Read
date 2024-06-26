import concurrent

import requests
from flask import Blueprint, jsonify, redirect
from flask import request as req
from flask import url_for
from flask_cors import CORS
from nyanga.window.server.helper.constant import constant
from nyanga.window.server.middleware.verificator.agent import verify_ua
from nyanga.window.server.middleware.verificator.csrf import verify_csrf
from nyanga.window.server.storage.model.bookmark import Bookmark
from nyanga.window.server.storage.model.read import Read
from nyanga.window.server.storage.model.settings import Setting
from nyanga.window.utils.parallel_request import parallelize_req
from nyanga.window.utils.resources import get_resources

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

        bookmark_link = [
            f"https://api.mangadex.org/manga/{bookmark.to_dict().get('manga')}?includes[]=cover_art&includes[]=artist&includes[]=manga"
            for bookmark in bookmarks
        ]

        with concurrent.futures.ThreadPoolExecutor() as parallelizer:
            fu = [parallelizer.submit(parallelize_req, link) for link in bookmark_link]
            concurrent.futures.wait(fu)

        if daily.status_code == 200:
            return jsonify(
                {
                    "daily_manga": daily.json(),
                    "bookmark": {
                        "more": True if Bookmark.query.count() > 3 else False,
                        "bookmark_manga": [data.result().get("data") for data in fu],
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
        page = req.args.get("page", None)

        bookmarked = Bookmark.query.filter_by(manga=manga).one_or_none()

        latest_readed = (
            Read.query.filter_by(manga=manga).order_by(Read.readed_at.desc()).first()
        )

        language = (
            Setting.query.filter_by(setting_type="language").one_or_none().to_dict()
        )

        detail = requests.get(
            f"https://api.mangadex.org/manga/{manga}?includes[]=cover_art&includes[]=artist&includes[]=manga"
        )

        if page:
            limit = 100
            offset = (int(page) - 1) * int(limit)
            manga = requests.get(
                f"https://api.mangadex.org/manga/{manga}/feed?translatedLanguage[]={language.get('value')}&order[chapter]=desc&limit={limit}&offset={offset}"
            )

        else:
            manga = requests.get(
                f"https://api.mangadex.org/manga/{manga}/feed?translatedLanguage[]={language.get('value')}&order[chapter]=desc"
            )

        if detail.status_code == 200 and manga.status_code == 200:
            manga = manga.json()

            return jsonify(
                {
                    "max_page": (
                        (manga.get("total") // 100)
                        if manga.get("total") % 100 != 0
                        else None
                    ),
                    "paginated": True if len(manga.get("data")) >= 100 else False,
                    "last_read": latest_readed.to_dict() if latest_readed else None,
                    "detail_data": detail.json().get("data"),
                    "bookmarked": True if bookmarked is not None else False,
                    "manga_data": [
                        {
                            "chapter_id": chapter.get("id"),
                            "chapter": chapter.get("attributes").get("chapter"),
                            "title": chapter.get("attributes").get("title"),
                        }
                        for chapter in manga.get("data")
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
        bookmark_data = Bookmark.query.order_by(Bookmark.bookmarked_at.desc()).all()

        bookmark_link = [
            f"https://api.mangadex.org/manga/{bookmark.to_dict().get('manga')}?includes[]=cover_art&includes[]=artist&includes[]=manga"
            for bookmark in bookmark_data
        ]

        with concurrent.futures.ThreadPoolExecutor() as parallelizer:
            fu = [parallelizer.submit(parallelize_req, link) for link in bookmark_link]
            concurrent.futures.wait(fu)

        return jsonify({"bookmark": [data.result().get("data") for data in fu]})
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
@verify_csrf
@verify_ua
def settings():
    if req.method == "GET":
        settings = Setting.query.all()
        return jsonify(
            {
                "settings": [setting.to_dict() for setting in settings],
            }
        )

    if req.method == "PATCH":
        update_setting = req.get_json()
        if update_setting:
            settings_id = update_setting.get("setting", None)
            settings_value = update_setting.get("value", None)

            if settings_id and settings_value:
                update = Setting.query.get(settings_id)
                update.value = settings_value
                constant.DB.session.commit()
                return jsonify({"status": "changed", "message": "Settings changed"})
            else:
                return jsonify({"status": "unchanged", "message": "Settings unchanged"})

        else:
            return jsonify({"emptySettings": True})

    return redirect(url_for("main.index"))


@ipc_handler.route("/app")
@verify_csrf
@verify_ua
def app_info():
    try:
        with open(get_resources("docs/app/about.md"), "r") as about_app:
            about = about_app.read()

        return jsonify({"app_info": {"app_about": about}})

    except FileNotFoundError as _:
        return jsonify({"status": "error", "location": "exception"})
