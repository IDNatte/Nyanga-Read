import argparse
import json
import logging
import os
import sys
import threading

import webview
from server.server import create_app
from utils.arg_parser import NyangaArgParser
from utils.extension import get_manga, search_manga
from utils.resources import get_resources
from utils.storage_initializer import db_settings_initializer
from utils.temp_attribute import NyangaTemporaryAttr


class Nyanga:
    def __init__(self):
        self.app_env = os.environ.get("APP_ENV", default=None)
        self.server = self.__run_server()
        self.parser = NyangaArgParser(description="Nyanga Read 😸")
        self.__open_extension = None

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
            # self.logger.info("starting server")

            # initialize database if not already created
            db_settings_initializer()

            # starting ipc server logger
            create_app().run(host="localhost", port=5000)

        except Exception as error:
            create_app().logger.info("stopping server")
            sys.exit(1)

    def __run_server(self):
        server_thread = threading.Thread(target=self.__server_instance, daemon=True)
        server_thread.start()

    def __parser(self):

        self.parser.add_argument(
            "--extension",
            action="store_true",
            help="access nyanga read via extension",
        )

        self.parser.add_argument(
            "--context",
            choices=["my_manga", "search_manga", "open_manga"],
            help="give some context to nyanga what you want to do",
        )

        self.parser.add_argument(
            "--manga-name",
            help="what the manga title you want to search (coupled with --context search_manga command)",
        )

        self.parser.add_argument(
            "--manga-id",
            help="what manga id that want to be opened (coupled with --context open_manga command)",
        )

        return {"client": self.parser.parse_args()}

    def __extension(self, context):
        match context.context:
            case "my_manga":
                sys.stdout.write(f"\n{json.dumps(get_manga())}\n\n")
            case "search_manga":
                if context.manga_name is None:
                    self.parser.error(
                        "search_manga is not provided with --manga-name <manga name>"
                    )

                sys.stdout.write(
                    f"\n{json.dumps(search_manga(context.manga_name))}\n\n"
                )

            case "open_manga":
                if context.manga_id is None:
                    self.parser.error(
                        "open_manga is not provided with --manga-id <manga ID>"
                    )

                NyangaTemporaryAttr.set_openmanga_id(context.manga_id)
                self.__open_extension = True

            case _:
                self.parser.error("no --context profided")

    def __webview(self, url="http://localhost:5000", debug=False):
        webview.create_window(
            "😸 Nyanga Read",
            url,
            width=1280,
            height=850,
            min_size=(1280, 850),
        )
        webview.start(
            user_agent="pywebview-client/1.0 pywebview-ui/3.0.0",
            debug=debug,
        )

    def __application(self):
        match self.app_env:
            case "dev":
                self.__webview(url="http://localhost:5173", debug=True)

            case "preview":
                self.__webview(url="http://localhost:5000", debug=True)

            case _:
                self.__webview(url="http://localhost:5173", debug=True)

    def run(self):
        client = self.__parser().get("client")

        if client.extension:
            self.__extension(client)
            if self.__open_extension:
                self.__application()

        if not client.extension:
            self.__application()


if __name__ == "__main__":
    app = Nyanga()
    app.run()
