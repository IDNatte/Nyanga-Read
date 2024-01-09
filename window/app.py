from sqlalchemy import desc
from server.server import create_app

from utils.storage_initializer import db_settings_initializer

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
    parser = argparse.ArgumentParser(description="Nyanga Read 😸")
    app_dev = os.environ.get("APP_DEV", default=None)

    parser.add_argument(
        "--extension",
        action="store_true",
        help="access nyanga read via extension",
    )

    parser.add_argument(
        "--context",
        choices=["get_csrf", "search_manga"],
        help="give some context to nyanga what you want to do",
    )

    client = parser.parse_args()

    if not client.extension:
        match app_dev:
            case "dev":
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

            case "preview":
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

            case _:
                server_main()

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
        match ext_context:
            case "get_csrf":
                print("get some csrf")
            case "search_manga":
                print("get some manga")

            case _:
                pass


if __name__ == "__main__":
    main()
