from server.server import create_app

from utils.storage_initializer import db_settings_initializer
from utils.extension import get_manga, get_csrf

import threading
import argparse
import webview
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
    # run server first
    server_main()

    # argument parser
    parser = argparse.ArgumentParser(description="Nyanga Read 😸")
    app_dev = os.environ.get("APP_DEV", default=None)

    parser.add_argument(
        "--extension",
        action="store_true",
        help="access nyanga read via extension",
    )

    # parser.add_argument(
    #     "--get-csrf",
    #     action="store_true",
    #     help="get csrf token from system",
    # )

    # parser.add_argument(
    #     "--csrf-token",
    #     help="if csrf already obtained, you can set it before using --context",
    # )

    parser.add_argument(
        "--context",
        choices=["my_manga", "search_manga"],
        help="give some context to nyanga what you want to do",
    )

    client = parser.parse_args()
    if not client.extension:
        match app_dev:
            case "dev":
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

            case "preview":
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

            case _:
                webview.create_window(
                    "😸 Nyanga Read",
                    "http://localhost:5000",
                    width=1280,
                    height=850,
                    min_size=(1280, 850),
                )
                webview.start(user_agent="pywebview-client/1.0 pywebview-ui/3.0.0")

    if client.extension:
        ext_context = client.context
        # if ext_get_csrf:
        #     print(get_csrf())

        # if ext_context == 'get_csrf':

        match ext_context:
            case "my_manga":
                print(get_csrf())
            case "search_manga":
                print("get some manga")

            case _:
                pass


if __name__ == "__main__":
    main()
