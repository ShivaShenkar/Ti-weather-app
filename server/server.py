from flask import Flask, send_from_directory
import webbrowser
import threading
import os

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.normpath(os.path.join(SERVER_DIR, "..", "client"))
CLIENT_BUILD_PATH = os.path.join(CLIENT_DIR,"dist","weather-app","browser")


# Debug: Print the resolved path (you can remove this later)
print(f"Server directory: {SERVER_DIR}\n")
print(f"Angular path resolved to: {CLIENT_BUILD_PATH }\n")
print(f"Path exists: {os.path.exists(CLIENT_BUILD_PATH )}\n")


client_app = Flask(__name__, static_folder=CLIENT_BUILD_PATH )

@client_app.route("/")
def home():
    return send_from_directory(CLIENT_BUILD_PATH , "index.html")




@client_app.route("/<path:path>")
def static_files(path):
   # Check if the file exists, otherwise serve index.html for Angular routes
    file_path = os.path.join(CLIENT_BUILD_PATH , path)
    if os.path.isfile(file_path):
        return send_from_directory(CLIENT_BUILD_PATH , path)
    else:
        # For Angular routes (SPA), serve index.html
        return send_from_directory(CLIENT_BUILD_PATH , "index.html")





def open_browser():
    webbrowser.open("http://localhost:8080")



if __name__ == "__main__":
    threading.Timer(5, open_browser).start()
    client_app.run(port=8080)

