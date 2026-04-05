import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR = os.path.join(ROOT_PATH,'server')
CLIENT_DIR = os.path.join(ROOT_PATH,'client')
CLIENT_BUILD_PATH = os.path.join(CLIENT_DIR,'dist','weather-app','browser')
EXE_PATH = os.path.join(SERVER_DIR,'dist','server.exe')
UI_PATH = os.path.join(ROOT_PATH,'ui')

__all__ = ['ROOT_PATH','SERVER_DIR','CLIENT_DIR','CLIENT_BUILD_PATH','UI_PATH','EXE_PATH']