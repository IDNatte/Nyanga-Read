from flask import Flask, send_from_directory
import os

gui_dir = os.path.join(os.path.dirname(__file__), "../layout")
server = Flask(__name__, static_folder=gui_dir)


# Serve the index.html file as the entry point to the SPA
@server.route("/")
def serve_spa():
    print(gui_dir)
    return send_from_directory(server.static_folder, "index.html")


# Serve the static files of the SPA with the correct MIME types
@server.route("/<path:path>")
def serve_static(path):
    return send_from_directory(server.static_folder, path)
