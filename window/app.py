from server import server
import webview

import threading
import sys
import os


def server_instance():
    try:
        server.logger.info("starting server")
        server.run(host="localhost", port=5000)

    except Exception as error:
        server.logger.error(f"{error}")
        sys.exit(1)


def server_main():
    server_thread = threading.Thread(target=server_instance, daemon=True)
    server_thread.start()


if __name__ == "__main__":
    env = os.environ.get("UI_APP_DEV", default=None)
    if env:
        webview.create_window("Nyanga Read", "http://localhost:5173")
        webview.start(private_mode=False, debug=True)

    else:
        server_main()

        webview.create_window("Nyanga Read", "http://localhost:5000")
        webview.start(private_mode=False)
