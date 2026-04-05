import subprocess
import sys
import os
from config import *
import shutil


def ensure_modules_installed():
    try:
        import PyInstaller  # noqa
        import flask  # noqa
    except ImportError:
        print("Installing modules...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r","requirements.txt"])


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


def move_to_ui():
    print(f"Moving build from {CLIENT_BUILD_PATH} to {UI_PATH}")
    if not os.path.exists(CLIENT_BUILD_PATH):
        raise OSError(f"Build folder does not exist: {CLIENT_BUILD_PATH}")
    if os.path.exists(UI_PATH):
        shutil.rmtree(UI_PATH)
    shutil.copytree(CLIENT_BUILD_PATH, UI_PATH)
    print("Build moved to ui folder successfully!")


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
    ensure_modules_installed()
    # PyInstaller --add-data format: "source;destination" on Windows, "source:destination" on Unix
    # Use relative path from SERVER_DIR to UI_PATH
    add_data_arg = f"../ui{os.pathsep}ui"
    
    
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
    ensure_modules_installed()
    ensure_angular_build()
    build_exe()
    run_exe()

