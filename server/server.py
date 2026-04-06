import sys
from flask import Flask, send_from_directory
import webbrowser
import threading
import os
from config import UI_PATH
import signal


def get_ui_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'ui')
    return UI_PATH

def shutdown_server():
    """Helper function for shutdown route"""
    print("Shutting down Flask server...")
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)

def open_browser():
    webbrowser.open("http://localhost:8080")


app = Flask(__name__,static_folder=UI_PATH)


@app.route("/")
def home():
    print('hello')
    ui_path = get_ui_path()
    return send_from_directory(ui_path, "index.html")



@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Shutdown the Flask app by mimicking CTRL+C"""
    shutdown_server()
    return "OK", 200

@app.route("/<path:path>")
def static_files(path):
    ui_path = get_ui_path()
    file_path = os.path.join(ui_path, path)

    print(f"Request: {path}")
    print(f"Full path: {file_path}")
    print(f"Exists: {os.path.isfile(file_path)}")

    
    if os.path.isfile(file_path):        
        return send_from_directory(ui_path, path)
    return send_from_directory(ui_path, "index.html")  





if __name__ == "__main__":
    print(get_ui_path())
    threading.Timer(5, open_browser).start()
    app.run(port=8080)