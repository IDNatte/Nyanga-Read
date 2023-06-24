from server.server import create_app

from utils.storage_initializer import db_settings_initializer

import threading
import webview
import utils
import sys
import os


def server_instance():
    try:
        # starting ipc server
        create_app().logger.info("starting server")

        # initialize database if not already created
        db_settings_initializer()

        # starting ipc
        create_app().run(host="localhost", port=5000)

    except Exception as error:
        create_app().logger.error(f"{error}")
        sys.exit(1)


def server_main():
    server_thread = threading.Thread(target=server_instance, daemon=True)
    server_thread.start()


def main():
    ui_dev = os.environ.get("UI_APP_DEV", default=None)
    app_dev = os.environ.get("APP_DEV", default=None)

    if ui_dev:
        server_main()

        webview.create_window(
            "😸 Nyanga Read",
            "http://localhost:5173",
            width=1280,
            height=850,
            min_size=(1280, 850),
        )
        webview.start(
            user_agent="pywebview-client/1.0 pywebview-ui/3.0.0",
            debug=True,
        )

    elif app_dev:
        server_main()

        webview.create_window(
            "😸 Nyanga Read",
            "http://localhost:5000",
            width=1280,
            height=850,
            min_size=(1280, 850),
        )
        webview.start(
            user_agent="pywebview-client/1.0 pywebview-ui/3.0.0",
            debug=True,
        )

    else:
        server_main()

        webview.create_window(
            "😸 Nyanga Read",
            "http://localhost:5000",
            width=1280,
            height=850,
            min_size=(1280, 850),
        )
        webview.start(user_agent="pywebview-client/1.0 pywebview-ui/3.0.0")


if __name__ == "__main__":
    main()
