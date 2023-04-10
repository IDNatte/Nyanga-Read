import threading
import webview
import os

from utils.get_resources import resource_path
from api.api import Api
from server import server

ENV = os.environ.get("APP_DEV", default=None)


def is_dev():
    if ENV:
        return "http://localhost:5173"

    if not ENV:
        return resource_path("layout/index.html")


def init_server():
    server.run(host="localhost")


renderer = is_dev()
api = Api()

if __name__ == "__main__":
    thread = threading.Thread(target=init_server)
    thread.daemon = True
    thread.start()

    webview.create_window(
        "Nyanga Read",
        "http://localhost:5000",
        js_api=api,
        width=1280,
        height=700,
        min_size=(1280, 800),
    )

    if ENV:
        # webview.start(private_mode=False, debug=True)
        webview.start(private_mode=False, debug=True)

    if not ENV:
        webview.start(private_mode=False)
