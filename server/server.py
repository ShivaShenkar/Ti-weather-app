import sys
from flask import Flask, send_from_directory
import webbrowser
import threading
import os
from config import UI_PATH


def get_ui_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'ui')
    return UI_PATH


app = Flask(__name__)


@app.route("/")
def home():
    ui_path = get_ui_path()
    return send_from_directory(ui_path, "index.html")


@app.route("/<path:path>")
def static_files(path):
    ui_path = get_ui_path()
    file_path = os.path.join(ui_path, path)
    if os.path.isfile(file_path):
        return send_from_directory(ui_path, path)
    return send_from_directory(ui_path, "index.html")


def open_browser():
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    threading.Timer(5, open_browser).start()
    app.run(port=8080)
