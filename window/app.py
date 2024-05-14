import argparse
import json
import logging
import os
import sys
import threading

import webview
from server.server import create_app
from utils.extension import get_manga, search_manga
from utils.resources import get_resources
from utils.storage_initializer import db_settings_initializer


class Nyanga:
    def __init__(self):
        self.app_env = os.environ.get("APP_ENV", default=None)
        self.server = self.__run_server()

        # logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # apps wide logger
        self.app_logger = logging.FileHandler(get_resources("log/app.log"))
        self.app_logger.setLevel(logging.DEBUG)
        self.app_logger.setFormatter(
            logging.Formatter("[%(module)s] [%(asctime)s] %(levelname)s : %(message)s")
        )

        self.logger.addHandler(self.app_logger)

        self.logger.info("starting application")

    def __server_instance(self):
        try:
            # starting ipc server
            create_app().logger.info("starting server")

            # initialize database if not already created
            db_settings_initializer()

            # starting ipc server logger
            create_app().run(host="localhost", port=5000)

        except Exception as error:
            self.logger.warning("stopping application !")
            sys.exit(1)

    def __run_server(self):
        server_thread = threading.Thread(target=self.__server_instance, daemon=True)
        server_thread.start()

    def __parser(self):
        parser = argparse.ArgumentParser(description="Nyanga Read 😸")

        parser.add_argument(
            "--extension",
            action="store_true",
            help="access nyanga read via extension",
        )

        parser.add_argument(
            "--context",
            choices=["my_manga", "search_manga"],
            help="give some context to nyanga what you want to do",
        )

        parser.add_argument(
            "--manga-name", help="what the manga title you want to search"
        )

        return {"client": parser.parse_args()}

    def __extension(self, context):
        match context.context:
            case "my_manga":
                sys.stdout.write(f"\n{json.dumps(get_manga())}\n\n")
            case "search_manga":
                sys.stdout.write(
                    f"\n{json.dumps(search_manga(context.manga_name))}\n\n"
                )
            case _:
                pass

    def __application(self):
        match self.app_env:
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

    def run(self):
        client = self.__parser().get("client")

        if not client.extension:
            self.__application()

        if client.extension:
            self.__extension(client)


if __name__ == "__main__":
    app = Nyanga()
    app.run()
