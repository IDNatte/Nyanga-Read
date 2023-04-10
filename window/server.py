from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="../layout")


# Serve the index.html file as the entry point to the SPA
@app.route("/")
def serve_spa():
    return send_from_directory(app.static_folder, "index.html")


# Serve the static files of the SPA with the correct MIME types
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    app.run(debug=True)
