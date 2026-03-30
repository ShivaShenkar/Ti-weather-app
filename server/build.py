import subprocess
import sys
import os

# Get the directory where build.py is located
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
EXE_PATH = os.path.join(SERVER_DIR, "dist", "server.exe")
CLIENT_DIR = os.path.normpath(os.path.join(SERVER_DIR, "..", "client"))
CLIENT_BUILD_PATH = os.path.join(CLIENT_DIR,"dist","weather-app","browser")


def ensure_pyinstaller():
    try:
        import PyInstaller  # noqa
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def ensure_angular_build():
    if os.path.exists(CLIENT_BUILD_PATH):
        while True:
            response= input(f"Angular build exists\nDo you want to rebuild it? (y/n) ")
            if response.lower() == "y":
                break
            elif response.lower()=='n':
                print("Building canceled.")
                return
            else:
                print("invalid prompt, try again \n")


    print("Building Angular...")
    # Resolve the client directory path
    print(f"Client directory: {CLIENT_DIR}")

    subprocess.check_call(
    ["npx", "ng", "build", "--configuration", "production"],
    cwd=CLIENT_DIR,
    shell=True)
    
    print("Angular built.")

def build_exe():

    
    if os.path.exists(EXE_PATH):
        while True:
            response= input(f"EXE file already exists\nDo you want to rebuild it? (y/n) ")
            if response.lower() == "y":
                break
            elif response.lower()=='n':
                print("Building canceled.")
                return
            else:
                print("invalid prompt, try again \n")

    
    print("Building EXE...")
    ensure_pyinstaller()
    # PyInstaller --add-data format: "source;destination" on Windows, "source:destination" on Unix
    # Use relative path from SERVER_DIR to CLIENT_BUILD_PATH
    relative_path = os.path.relpath(CLIENT_BUILD_PATH, SERVER_DIR)
    add_data_arg = f"../client/dist/weather-app/browser{os.pathsep}client/dist/weather-app/browser"
    
    
    try:
        subprocess.check_call([
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--add-data",
            add_data_arg,
            "server.py"
        ], cwd=SERVER_DIR)
        print("EXE file is built.")
    except subprocess.CalledProcessError as e:
        print(f"Error building EXE: {e}")
        raise

def run_exe():

    print(f"Running EXE: {EXE_PATH}")
    if not os.path.exists(EXE_PATH):
        print(f"EXE not found: {EXE_PATH}")
        return
    subprocess.Popen([EXE_PATH], shell=True)

    print("Server started. Press Ctrl+C to stop.")

if __name__ == "__main__":
    ensure_angular_build()
    build_exe()
    run_exe()

