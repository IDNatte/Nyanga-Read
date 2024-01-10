from flask_cors import CORS
from flask import Blueprint
from flask import jsonify

# from server.middleware.verificator.csrf import verify_csrf
from server.middleware.verificator.agent import verify_ua
from server.storage.model.bookmark import Bookmark

# from webview import token as wv_token

interface_handler = Blueprint("interface", __name__, url_prefix="/extension")

CORS(interface_handler)


# @interface_handler.route("/get_csrf")
# @verify_ua
# def extension_get_csrf():
#     return jsonify({"token": wv_token})


@interface_handler.route("/my_manga")
@verify_ua
def my_manga():
    my_manga_lists = Bookmark.query.order_by(Bookmark.bookmarked_at.desc()).all()
    c = [data.manga for data in my_manga_lists]
    return jsonify({"some": "mangaLists", "data": c})
